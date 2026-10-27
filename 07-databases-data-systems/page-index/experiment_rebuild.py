"""Observed full-prefix rebuild states at every small WAL cut; source is read-only."""
import json,tempfile
from pathlib import Path
from rebuild import rebuild_from_log,wal_module


def run():
    wal=wal_module()
    frames=[wal.encode_transaction(1,[('put','0','old'),('put','29','old')]),
            wal.encode_transaction(2,[('put','0','new'),('put','29','new')]),
            wal.encode_transaction(3,[('delete','0'),('put','-2','é')])]
    image=wal.FILE_MAGIC+b''.join(frames);groups={}
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'source.wal'
        for cut in range(len(wal.FILE_MAGIC),len(image)+1):
            source=image[:cut];path.write_bytes(source);tree,report=rebuild_from_log(path)
            assert path.read_bytes()==source
            key=str(report['transactions']);group=groups.setdefault(key,{'transactions':report['transactions'],'first_cut':cut,'last_cut':cut,'rows':[(k,v.hex()) for k,v in tree.range()]})
            group['last_cut']=cut
    return {'kind':'actual synthetic read-only WAL cut/rebuild execution','cuts_checked':len(image)-len(wal.FILE_MAGIC)+1,
            'groups':list(groups.values()),'limits':'No checkpoint replay skipping, source write, process crash, power failure or concurrent mutation.'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
