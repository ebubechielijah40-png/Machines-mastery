"""Exercise evidence gates and non-destructive scaffolding using local fixtures."""
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fingerprint import fingerprint
from render import documents
from scaffold import scaffold
from validate import ROOT, safe_path, validate_catalog, validate_files


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads((ROOT/'registries/catalog.json').read_text())

    def setUp(self):
        self.data = copy.deepcopy(self.original)

    def assert_error(self, fragment):
        errors,_ = validate_catalog(self.data)
        self.assertTrue(any(fragment in e for e in errors),errors)

    def test_current_catalog_has_no_structural_errors(self):
        errors,warnings = validate_catalog(self.data)
        self.assertEqual(errors,[])
        self.assertIsInstance(warnings, list)

    def test_absent_book_reports_warning(self):
        self.data['books'][0].update(status='SOURCE NOT PRESENT', source_path=None,
            sha256=None, edition=None, inspection_evidence=None)
        self.data['chapters'] = []
        _, warnings = validate_catalog(self.data)
        self.assertTrue(any('SOURCE NOT PRESENT' in w for w in warnings))

    def test_duplicate_resource(self):
        self.data['resources'].append(copy.deepcopy(self.data['resources'][0]))
        self.assert_error('duplicate ID')

    def test_missing_metadata(self):
        del self.data['resources'][0]['license']
        self.assert_error('license')

    def test_malformed_reference_list(self):
        self.data['units'][0]['required']=[{}]
        self.assert_error('items must be strings')

    def test_malformed_optional_path(self):
        self.data['projects'][0]['path']=42
        self.assert_error('expected string or null')

    def test_missing_phase_resource(self):
        self.data['phases'][0]['resources']=[]
        self.assert_error('missing resources references')

    def test_unknown_resource_reference(self):
        self.data['units'][0]['resources']=['R-NONEXISTENT']
        self.assert_error('unknown resources reference')

    def test_prerequisite_cycle(self):
        self.data['units'][0]['required']=['U01']
        self.assert_error('prerequisite cycle')

    def test_result_before_execution(self):
        self.data['experiments'][0]['observed_result']='All rows matched.'
        self.assert_error('unexecuted experiment claims a result')

    def test_observation_requires_raw_evidence(self):
        e=self.data['experiments'][0]
        e.update(status='OBSERVED',observed_result='A mismatch was recorded.',source_ready=True)
        self.assert_error('missing evidence')

    def test_unrelated_file_is_not_raw_experiment_evidence(self):
        e=self.data['experiments'][0]
        e.update(status='OBSERVED',observed_result='fixture',source_ready=True,evidence=['AGENTS.md'])
        self.assert_error('requires non-private raw evidence')

    def test_completion_requires_gates(self):
        self.data['projects'][0]['status']='COMPLETE'
        self.assert_error('incomplete quality gate')

    def test_project_requires_original_attribution_reference(self):
        self.data['projects'][0]['original_resources']=[]
        self.assert_error('missing resources references')

    def test_chapter_requires_inspected_book(self):
        self.data['books'][0].update(status='SOURCE NOT PRESENT', source_path=None,
            sha256=None, edition=None, inspection_evidence=None)
        self.data['chapters'].append(dict(id='CH-TEST',resource_id='R-CODE',
            path='books/code-petzold/generated',locator='Test fixture only',status='DRAFT',source_ready=True))
        self.assert_error('chapter without inspected local source')

    def test_source_fingerprint_mismatch(self):
        self.data['books'][0].update(status='INSPECTED',source_path='AGENTS.md',
            edition='Test fixture only, not a book',inspection_evidence='AGENTS.md',sha256='0'*64)
        self.assert_error('source fingerprint mismatch')

    def test_learning_progress_requires_evidence(self):
        self.data['units'][0]['state']='MASTERED'
        self.assert_error('missing evidence')

    def test_learning_progress_requires_review(self):
        self.data['units'][0].update(state='STUDIED',evidence=['AGENTS.md'])
        self.assert_error('matching mastery review')

    def test_mastery_requires_delayed_recall_and_transfer(self):
        self.data['mastery'].append(dict(id='M-TEST',unit_id='U00',state='MASTERED',
            assessed_on='2026-09-26',assessor='test fixture',evidence=['AGENTS.md'],
            assistance='test fixture',gaps=[],next_review='2026-10-03',criteria={}))
        self.assert_error('MASTERED requires reviewed criteria')

    def test_knowledge_edge_requires_claim(self):
        self.data['knowledge_edges'].append(dict(id='K-TEST',
            **{'from':'test input','to':'test output'},relation='test relation',
            claim_ids=[],artifact='AGENTS.md',limitations='fixture'))
        self.assert_error('missing claims references')

    def test_renderer_is_deterministic(self):
        self.assertEqual(documents(self.data),documents(copy.deepcopy(self.data)))


class FileSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        for name in ['registries','templates','projects','books','experiments']:
            (self.root/name).mkdir()
        for name in ['registries/catalog.json','templates/project-documents.json','templates/experiment.md']:
            shutil.copyfile(ROOT/name,self.root/name)

    def tearDown(self):
        self.temp.cleanup()

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            safe_path(self.root,'../outside')

    def test_symlink_escape_rejected(self):
        (self.root/'escape').symlink_to(self.root.parent,target_is_directory=True)
        with self.assertRaises(ValueError):
            safe_path(self.root,'escape/anything')

    def test_fingerprint_matches_actual_bytes(self):
        p=self.root/'source.txt'
        p.write_bytes(b'fixture bytes\n')
        self.assertEqual(fingerprint(p)['sha256'],hashlib.sha256(b'fixture bytes\n').hexdigest())

    def test_project_scaffold_is_non_destructive(self):
        path=scaffold(self.root,'project','J-02')
        text=(self.root/path/'RESULTS.md').read_text()
        self.assertIn('NOT YET OBSERVED',text)
        self.assertFalse((self.root/path/'src').exists())
        before=(self.root/'registries/catalog.json').read_bytes()
        with self.assertRaises(ValueError):
            scaffold(self.root,'project','J-02')
        self.assertEqual(before,(self.root/'registries/catalog.json').read_bytes())
        self.assertEqual(text,(self.root/path/'RESULTS.md').read_text())

    def test_book_scaffold_never_invents_chapters(self):
        path=scaffold(self.root,'book','R-PYTHON','think-python')
        self.assertIn('SOURCE NOT PRESENT',(self.root/path/'generated/BOOK_MAP.md').read_text())
        self.assertFalse((self.root/path/'generated/chapters').exists())

    def test_experiment_scaffold_never_invents_results(self):
        path=scaffold(self.root,'experiment','E-999','test-contract','J-01')
        self.assertIn('NOT YET OBSERVED',(self.root/path/'README.md').read_text())
        data=json.loads((self.root/'registries/catalog.json').read_text())
        self.assertEqual(data['experiments'][-1]['evidence'],[])
        with self.assertRaises(ValueError):
            scaffold(self.root,'experiment','E-999','test-contract','J-01')

    def test_experiment_parent_required(self):
        with self.assertRaises(ValueError):
            scaffold(self.root,'experiment','E-999','test-contract','J-NONE')
        self.assertEqual(list((self.root/'experiments').iterdir()),[])

    def test_invalid_slug_writes_nothing(self):
        before=(self.root/'registries/catalog.json').read_bytes()
        with self.assertRaises(ValueError):
            scaffold(self.root,'book','R-PYTHON','../outside')
        self.assertEqual(before,(self.root/'registries/catalog.json').read_bytes())
        self.assertEqual(list((self.root/'books').iterdir()),[])

    def test_existing_user_destination_preserved(self):
        folder=self.root/'projects/unix-shell'
        folder.mkdir()
        (folder/'README.md').write_text('User work\n')
        with self.assertRaises(ValueError):
            scaffold(self.root,'project','J-02')
        self.assertEqual((folder/'README.md').read_text(),'User work\n')

    def test_broken_internal_link_detected(self):
        (self.root/'README.md').write_text('# Fixture\n\n[Missing](missing.md)\n')
        data=json.loads((self.root/'registries/catalog.json').read_text())
        self.assertTrue(any('broken or escaping internal link' in e for e in validate_files(self.root,data)))

    def test_private_and_source_material_not_scanned(self):
        for name in ['private','raw-private','books/test/source']:
            folder=self.root/name
            folder.mkdir(parents=True,exist_ok=True)
            (folder/'data.md').write_bytes(b'\xff\xfe')
        data=json.loads((self.root/'registries/catalog.json').read_text())
        # Invalid UTF-8 in excluded originals/private material must not be read.
        validate_files(self.root,data)


if __name__=='__main__':
    unittest.main()
