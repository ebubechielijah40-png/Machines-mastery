"""Adversarial tiny repositories exercise missed failures and false certification."""
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_audit import audit


class QualityAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        p = self.root/path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def codes(self):
        return {x['code'] for x in audit(self.root)['findings']}

    def test_honest_scaffold_status_does_not_break_a_support_report(self):
        self.write('research/review.md', 'SCAFFOLDED. This report admits unfinished work.\n')
        self.assertNotIn('placeholder-instruction', self.codes())

    def test_broken_reference_link_and_bad_fragment_detected(self):
        self.write('01-topic/README.md', '[a][r]\n\n[r]: missing.md\n\n[b](other.md#missing)\n')
        self.write('01-topic/other.md', '# Present\n')
        self.assertTrue({'broken-link', 'unresolved-anchor'} <= self.codes())

    def test_syntax_parsing_never_executes_and_fragments_can_be_labelled(self):
        self.write('01-topic/code.py', "raise RuntimeError('must not execute')\n")
        self.write('01-topic/README.md', '```python\nx =\n```\n```python\n# fragment\nreturn x\n```\n')
        self.assertIn('invalid-python-example', self.codes())
        self.write('01-topic/bad.py', 'def x(:\n')
        self.assertIn('invalid-python', self.codes())

    def test_repeated_substantive_template_found_without_title_matching(self):
        paragraph = ' '.join(['generic instruction'] * 12)
        for i in range(4):
            self.write(f'{i+1:02}-topic/lesson.md', '# Unique title '+str(i)+'\n\n'+paragraph)
        self.assertEqual(len(audit(self.root)['repeated_paragraphs']), 1)
        self.assertIn('repeated-template', self.codes())

    def test_private_source_and_symlink_trees_excluded(self):
        for d in ['private', 'raw-private', 'source', '.git']:
            self.write(f'books/x/{d}/secret.md', '[bad](missing.md)')
        (self.root/'link').symlink_to(self.root/'books', target_is_directory=True)
        self.assertFalse(audit(self.root)['findings'])

    def test_project_plan_and_unverified_paper_are_not_implementations(self):
        self.write('projects-guided/p01-example/README.md', '# Build something\n')
        self.write('research-paper-reconstruction/domains/a/01_paper.md', '# Named paper\n')
        self.assertTrue({'project-no-local-implementation', 'project-no-local-tests', 'unverified-paper-dossier'} <= self.codes())

    def test_excellence_requires_all_evidence_types(self):
        self.write('registries/quality_evidence.json', json.dumps({'units': [
            {'path': '01-topic', 'classification': 'EXCELLENT', 'tests': ['absent.txt']}]}))
        self.assertIn('unsupported-excellence-claim', self.codes())

    def test_strong_evidence_links_cannot_silently_go_stale(self):
        self.write('proof.txt', 'Bounded review and test evidence.')
        unit = {'path': '01-topic', 'classification': 'STRONG'}
        for field in ['review', 'tests', 'sources', 'experiment', 'assessment']:
            unit[field] = ['proof.txt']
        self.write('registries/quality_evidence.json', json.dumps({'units': [unit]}))
        self.assertNotIn('unsupported-strong-claim', self.codes())
        unit['experiment'] = ['missing-experiment.md']
        self.write('registries/quality_evidence.json', json.dumps({'units': [unit]}))
        self.assertIn('unsupported-strong-claim', self.codes())

    def test_invalid_evidence_shape_cannot_crash_or_certify(self):
        for payload in [[], {'units':[None]}, {'units':'wrong'}]:
            self.write('registries/quality_evidence.json', json.dumps(payload))
            self.assertIn('invalid-quality-evidence', self.codes())
        self.write('registries/source_verification.json', json.dumps({'sources':[None]}))
        self.assertIn('invalid-verification-records', self.codes())

    def test_excellence_symlink_and_parent_escape_rejected(self):
        self.write('real.txt', 'evidence')
        (self.root/'linked.txt').symlink_to(self.root/'real.txt')
        unit={'path':'01-topic','classification':'EXCELLENT'}
        for field in ['review','tests','sources','experiment','assessment']:
            unit[field]=['linked.txt']
        self.write('registries/quality_evidence.json', json.dumps({'units':[unit]}))
        self.assertIn('unsupported-excellence-claim', self.codes())
        unit['review']=['../elsewhere.txt']
        self.write('registries/quality_evidence.json', json.dumps({'units':[unit]}))
        self.assertIn('unsupported-excellence-claim', self.codes())

    def test_compilation_detects_illegal_top_level_statements(self):
        self.write('01-topic/README.md', '```python\nreturn 3\n```\n')
        self.write('01-topic/bad.py', 'break\n')
        self.assertTrue({'invalid-python','invalid-python-example'} <= self.codes())

    def test_symlink_manifest_itself_is_not_read(self):
        self.write('real.json', '{not valid json')
        (self.root/'registries').mkdir()
        for name in ['source_verification.json','quality_evidence.json']:
            (self.root/'registries'/name).symlink_to(self.root/'real.json')
        self.assertTrue({'unsafe-verification-manifest','unsafe-quality-manifest'} <= self.codes())

    def test_contradictory_book_availability_is_not_accepted(self):
        catalog={'resources':[{'id':'B','local_availability':'INSPECTED — local file'}],
                 'books':[{'resource_id':'B','status':'SOURCE NOT PRESENT'}]}
        self.write('registries/catalog.json',json.dumps(catalog))
        self.assertIn('contradictory-source-availability', self.codes())
        catalog['resources'][0]['local_availability']='SOURCE NOT PRESENT — historical inspection only'
        self.write('registries/catalog.json',json.dumps(catalog))
        self.assertNotIn('contradictory-source-availability', self.codes())

    def test_completed_problem_requires_real_implementation(self):
        self.write('registries/catalog.json',json.dumps({'expansion_plan':{'completed_algorithm_topics':['arrays']}}))
        self.write('algorithmic-problem-solving/topics/arrays/problems/01/prompt.md','# Problem')
        self.assertIn('completed-problem-missing-implementation',self.codes())

    def shared_fixture(self):
        self.write('projects-guided/p01-example/README.md','# Shared build\n')
        self.write('01-topic/model.py','value = 1\n')
        self.write('01-topic/test_model.py','assert True\n')
        self.write('research/run.json','{"exit_code":0}')
        return {'readme':'projects-guided/p01-example/README.md',
                'scope':'One shared bounded mechanism; no domain classification.',
                'implementation':['01-topic/model.py'],
                'tests':['01-topic/test_model.py'],'verification':['research/run.json']}

    def test_explicit_shared_project_files_are_resolved_without_certification(self):
        binding=self.shared_fixture()
        self.write('registries/project_implementations.json',json.dumps({'projects':[binding]}))
        codes=self.codes()
        self.assertNotIn('project-no-local-implementation',codes)
        self.assertNotIn('project-no-local-tests',codes)
        self.assertIn('near-empty-instruction',codes)  # File references never certify teaching.

    def test_shared_binding_missing_or_unsafe_evidence_does_not_suppress_gap(self):
        binding=self.shared_fixture()
        for path in ['absent.py','../outside.py','private/model.py','linked.py']:
            self.write('private/model.py','secret = True\n')
            if not (self.root/'linked.py').exists():(self.root/'linked.py').symlink_to(self.root/'01-topic/model.py')
            binding['implementation']=[path]
            self.write('registries/project_implementations.json',json.dumps({'projects':[binding]}))
            self.assertTrue({'invalid-project-bindings','project-no-local-implementation','project-no-local-tests'} <= self.codes())

    def test_malformed_shared_manifest_and_noncode_binding_rejected(self):
        binding=self.shared_fixture()
        cases=[[],{'projects':[None]},{'projects':'wrong'},
               {'projects':[dict(binding,implementation=['research/run.json'])]},
               {'projects':[binding,binding]}]
        for payload in cases:
            self.write('registries/project_implementations.json',json.dumps(payload))
            self.assertIn('invalid-project-bindings',self.codes())

    def test_shared_manifest_symlink_is_not_read(self):
        self.write('real.json','{"projects":[]}')
        (self.root/'registries').mkdir()
        (self.root/'registries/project_implementations.json').symlink_to(self.root/'real.json')
        self.assertIn('unsafe-project-manifest',self.codes())


if __name__ == '__main__':
    unittest.main()
