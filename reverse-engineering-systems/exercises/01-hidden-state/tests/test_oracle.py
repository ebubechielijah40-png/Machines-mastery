from pathlib import Path
import itertools
import subprocess
import sys
import unittest
B=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(B))
from reveal.machine import Machine
from reveal.replica import Replica


class OracleTests(unittest.TestCase):
    def test_independent_histories(self):
        for length in range(7):
            for commands in itertools.product(("up","down","peek","reset","bad"),repeat=length):
                a,b=Machine(),Replica()
                self.assertEqual([a.query(c) for c in commands],[b.query(c) for c in commands])

    def test_known_discriminating_trace(self):
        m=Machine()
        commands=["reset","up","up","up","up","bad","peek","down","down","down","down"]
        self.assertEqual([m.query(c) for c in commands],[0,1,2,3,3,"ERROR",3,2,1,0,0])

    def test_public_process_and_fresh_session(self):
        for _ in range(2):
            run=subprocess.run([sys.executable,str(B/"oracle.py")],input="up\nup\npeek\n",text=True,capture_output=True,check=True)
            self.assertEqual(run.stdout.splitlines(),["1","2","2"])


if __name__ == "__main__":
    unittest.main()
