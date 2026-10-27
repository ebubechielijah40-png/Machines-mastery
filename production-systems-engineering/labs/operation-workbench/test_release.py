import http.client
from pathlib import Path
import tempfile
import unittest
from release_drill import running,request,run_drill


class ReleaseTests(unittest.TestCase):
    def test_actual_release_rollback_backup_and_recovery(self):
        observed=run_drill()
        self.assertTrue(observed['stale_backup_refused'])
        self.assertEqual(observed['restored']['counter'],16)
        self.assertEqual([e['stage'] for e in observed['actual_events']],['initial','old_client_rejects_mutant','rollback_preserves_original_response'])

    def test_wire_schema_conflict_and_readiness(self):
        with tempfile.TemporaryDirectory() as directory:
            with running(Path(directory)/'db') as (_,port):
                self.assertEqual(request(port)[1]['operations'],0)
                self.assertEqual(request(port,'A',2)[0],200)
                self.assertEqual(request(port,'A',3)[0],409)
                for body in (b'{"request_id":"X","delta":true}',b'{"request_id":"X","delta":1,"delta":2}',b'{}',b'{'*513):
                    client=http.client.HTTPConnection('127.0.0.1',port,timeout=2)
                    try:
                        client.request('POST','/op',body)
                        response=client.getresponse();response.read()
                        self.assertEqual(response.status,400)
                    finally:client.close()
                self.assertEqual(request(port)[1]['operations'],1)


if __name__=='__main__':unittest.main()
