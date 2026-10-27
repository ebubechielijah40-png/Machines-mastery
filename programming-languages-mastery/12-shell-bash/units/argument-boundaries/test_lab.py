import tempfile,unittest
from lab import FORMS,observe,run_case

class ArgumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows=observe()['observations']
    def test_quoted_preserves_all_boundaries(self):
        self.assertEqual(self.rows['quoted_at'],['two words','','*.txt'])
        self.assertEqual(self.rows['quoted_array'],['two words','','*.txt'])
    def test_unquoted_splits_drops_empty_and_expands_glob(self):
        self.assertEqual(self.rows['unquoted_at'],['two','words','alpha.txt','two words.txt'])
    def test_star_joins_and_empty_at_stays_empty(self):
        self.assertEqual(self.rows['quoted_star'],['two words  *.txt'])
        self.assertEqual(self.rows['empty_at'],[])
    def test_data_is_not_reparsed_as_shell_syntax(self):
        self.assertEqual(self.rows['metacharacters'],['$(touch marker)','a; b','--leading-option'])
        self.assertFalse(self.rows['marker_exists'])
    def test_command_substitution_trims_trailing_newlines(self):
        self.assertEqual(self.rows['command_substitution'],['a'])
    def test_pipeline_exit_semantics(self):
        self.assertEqual(self.rows['pipeline_default'],0)
        self.assertEqual(self.rows['pipeline_pipefail'],1)
    def test_newline_and_empty_data_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            values=['line1\nline2','','a * ? [x]']
            self.assertEqual(run_case(FORMS['quoted_at'],values,directory),values)

if __name__=='__main__':unittest.main()
