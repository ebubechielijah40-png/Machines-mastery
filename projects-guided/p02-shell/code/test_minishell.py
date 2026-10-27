import os,pathlib,subprocess,sys,tempfile,time,unittest
from minishell import parse,run_pipeline,Shell
class ShellTests(unittest.TestCase):
 def test_quote_escape_and_operator_boundary(self):
  self.assertEqual(parse("prog 'two words' \"a|b\" x\\ y ''"),[['prog','two words','a|b','x y','']])
  self.assertEqual(parse('one a|two b'),[['one','a'],['two','b']])
  self.assertEqual(parse('  '),[])
 def test_bad_syntax_and_caps(self):
  for line in ['|a','a|','a||b',"a 'unfinished",'a\\',"'' arg",'x'*4097]:
   with self.assertRaises(ValueError):parse(line)
  with self.assertRaises(ValueError):parse('|'.join(['x']*9))
 def test_real_pipeline_and_eof(self):
  r=run_pipeline([[sys.executable,'-c','import sys; sys.stdout.buffer.write(sys.stdin.buffer.read().upper())'],[sys.executable,'-c','import sys; print(len(sys.stdin.buffer.read()))']],input_bytes=b'abcd')
  self.assertEqual(r.stdout,b'4\n');self.assertEqual(r.returncodes,(0,0))
 def test_metacharacters_are_data_and_exit_codes_are_retained(self):
  arg='; $(unexecuted) *'
  r=run_pipeline([[sys.executable,'-c','import sys;print(sys.argv[1]);sys.exit(7)',arg]])
  self.assertEqual(r.stdout,(arg+'\n').encode());self.assertEqual(r.returncodes,(7,))
 def test_large_output_does_not_deadlock_pipe_wait(self):
  r=run_pipeline([[sys.executable,'-c','import sys;sys.stdout.buffer.write(b"x"*200000)'],[sys.executable,'-c','import sys;print(len(sys.stdin.buffer.read()))']])
  self.assertEqual(r.stdout,b'200000\n')
 def test_failure_and_timeout_cleanup(self):
  with self.assertRaises(FileNotFoundError):run_pipeline([['/definitely/not/a/program']])
  with self.assertRaises(subprocess.TimeoutExpired):run_pipeline([[sys.executable,'-c','import time;time.sleep(10)']],timeout=.05)
  with self.assertRaises(ValueError):run_pipeline([[sys.executable,'-c','print("too much")']],max_output=2)
 def test_invalid_runtime_control_values(self):
  for timeout in [float('nan'),float('inf'),True,0]:
   with self.assertRaises(ValueError):run_pipeline([[sys.executable,'-c','pass']],timeout=timeout)
  with self.assertRaises(ValueError):run_pipeline('not a parsed pipeline')
 def test_cd_changes_shell_state_not_parent_process(self):
  before=os.getcwd()
  with tempfile.TemporaryDirectory() as td:
   child=pathlib.Path(td)/'child';child.mkdir();s=Shell(td);s.execute('cd child')
   self.assertEqual(s.cwd,child.resolve())
   r=s.execute('"'+sys.executable+'" -c "import os; print(os.getcwd())"')
   self.assertEqual(r.stdout.decode().strip(),str(child));self.assertEqual(os.getcwd(),before)
 def test_cli_exit_and_syntax_failure(self):
  entry=pathlib.Path(__file__).with_name('minishell.py')
  p=subprocess.run([sys.executable,str(entry),'-c',f'''"{sys.executable}" -c 'import sys; print("observed"); sys.exit(7)' '''],text=True,capture_output=True,timeout=4)
  self.assertEqual(p.returncode,7);self.assertEqual(p.stdout,'observed\n')
  bad=subprocess.run([sys.executable,str(entry),'-c','x |'],text=True,capture_output=True,timeout=4)
  self.assertEqual(bad.returncode,2);self.assertIn('empty command',bad.stderr)
if __name__=='__main__':unittest.main(verbosity=2)
