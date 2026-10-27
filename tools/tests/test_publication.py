"""Adversarial publication cases and an actual extract→git add integration."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

TOOLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TOOLS))
from check_publication import audit,content_findings,path_findings,verify_zip,MAX_BYTES
import package_release


class PublicationTests(unittest.TestCase):
    def test_private_generated_and_delivery_files_are_rejected(self):
        bad=['.git/config','.GIT/config','x/__pycache__/a.pyc','x/private/notes.txt','x/.venv/bin/python',
             'node_modules/x.js','keys/id.pem','release.bundle','release.zip',
             'RELEASE.json','SOURCE_SHA256SUMS.txt','books/x/source/book.pdf',
             '.env','.env.local','credentials.json']
        for name in bad:
            with self.subTest(name=name):self.assertTrue(path_findings([name]))
        self.assertFalse(path_findings(['.gitignore','.github/workflows/check.yml',
                                       'books/x/source/README.md','.env.example',
                                       'research/quality/2026-10-25/tests.txt','src/model.py']))

    def test_paths_are_portable_and_cannot_collide(self):
        for name in ('../outside','/absolute','a\\b','a/CON.txt','a/x.','a/a:b','a/new\nline'):
            with self.subTest(name=name):self.assertTrue(path_findings([name]))
        self.assertTrue(path_findings(['README.md','readme.md']))

    def test_possible_credentials_are_reported_without_the_value(self):
        for raw in (b'-----BEGIN '+b'PRIVATE KEY-----',b'gh' + b'p_' + b'x'*36):
            findings=content_findings('accidental.txt',b'line1\n'+raw)
            self.assertEqual(findings[0]['line'],2)
            self.assertNotIn(raw.decode(),json.dumps(findings))
        self.assertFalse(content_findings('fixture.py',b"demo_key=b'a'*32\n"))

    def test_binary_payloads_and_large_paths_fail(self):
        for raw in (b'\x7fELFtest',b'MZtest',b'SQLite format 3\x00'):
            self.assertEqual(content_findings('misnamed.txt',raw)[0]['code'],'generated-binary-content')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.git(root,'init','-q')
            path=root/'huge.txt'
            with path.open('wb') as stream:stream.truncate(MAX_BYTES)
            self.git(root,'add','huge.txt')
            self.assertEqual(audit(root)['findings'][0]['code'],'github-size-limit')

    @staticmethod
    def git(root,*args):
        return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.STDOUT)

    def test_tracked_files_only_and_symlinks_are_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.git(root,'init','-q')
            (root/'lesson.md').write_text('Original teaching.\n');self.git(root,'add','lesson.md')
            (root/'.env').write_text('LOCAL_ONLY=example\n')
            self.assertEqual(audit(root)['findings'],[])
            (root/'link.md').symlink_to(root/'lesson.md');self.git(root,'add','link.md')
            self.assertIn('symlink-or-escape',{x['code'] for x in audit(root)['findings']})

    def test_forced_ignored_report_cannot_silently_enter_the_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.git(root,'init','-q')
            (root/'.gitignore').write_text('local-output/\n')
            (root/'local-output').mkdir();(root/'local-output/run.txt').write_text('temporary\n')
            self.git(root,'add','.gitignore');self.git(root,'add','-f','local-output/run.txt')
            self.assertIn('ignored-file-tracked',{x['code'] for x in audit(root)['findings']})

    def test_archive_rejects_wrapper_sidecar_extra_and_wrong_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'source.zip';expected={'README.md':b'content\n'}
            for contents in ({'machines-mastery/README.md':b'content\n'},
                             {'README.md':b'content\n','RELEASE.json':b'{}'},
                             {'README.md':b'changed\n'}):
                with zipfile.ZipFile(path,'w') as z:
                    for name,raw in contents.items():z.writestr(name,raw)
                with self.assertRaises(ValueError):verify_zip(path,expected)

    def test_hidden_files_survive_and_real_git_add_needs_no_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);repo=base/'repo';repo.mkdir();self.git(repo,'init','-q','-b','review/test')
            files={'.gitignore':'__pycache__/\n*.bundle\n',
                   '.github/workflows/check.yml':'name: Checks\non: push\n',
                   'README.md':'Original teaching.\n',
                   'evidence/verification-final/results.json':json.dumps({'results':[{'name':'fixture','status':'PASS'}]}),
                   'evidence/content-gate.json':json.dumps({'exit_code':1,'findings':1})}
            for name,text in files.items():
                path=repo/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
            self.git(repo,'add','-A')
            self.git(repo,'-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','Fixture')
            head=self.git(repo,'rev-parse','HEAD').decode().strip();out=base/'delivery'
            argv=['package_release','--source-only','--label','2026-10-25',
                  '--report-root','evidence','--continuation-base',head,'--output-dir',str(out)]
            with patch.object(package_release,'ROOT',repo),patch.object(sys,'argv',argv),contextlib.redirect_stdout(io.StringIO()):
                package_release.main()
            archive=out/'Machines-mastery-development-2026-10-25.zip'
            expected={name:(repo/name).read_bytes() for name in files}
            self.assertEqual(verify_zip(archive,expected)['source_files'],len(files))
            fresh=base/'fresh';fresh.mkdir()
            with zipfile.ZipFile(archive) as z:z.extractall(fresh)
            self.git(fresh,'init','-q');self.git(fresh,'add','--all')
            staged=set(self.git(fresh,'ls-files','-z').decode().strip('\0').split('\0'))
            self.assertEqual(staged,set(files))
            self.assertEqual({p.name for p in out.iterdir()},
                             {'Machines-mastery-development-2026-10-25.zip',
                              'Machines-mastery-development-2026-10-25-zip.bundle',
                              'Machines-mastery-2026-10-25-zip-SHA256SUMS.txt',
                              'SOURCE_SHA256SUMS.txt','READ_ME_FIRST.txt','RELEASE.json'})
            clone=base/'clone'
            self.git(base,'clone','-q','--branch','review/test',str(out/'Machines-mastery-development-2026-10-25-zip.bundle'),str(clone))
            self.assertEqual(self.git(clone,'rev-parse','HEAD').decode().strip(),head)


if __name__=='__main__':unittest.main(verbosity=2)
