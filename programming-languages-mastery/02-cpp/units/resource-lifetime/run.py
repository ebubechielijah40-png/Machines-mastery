"""Compile in isolated temporary directories; capture actual commands and outputs."""
from pathlib import Path
import json,platform,shutil,subprocess,sys,tempfile
base=Path(__file__).resolve().parent
compiler=shutil.which('g++')
if compiler is None:raise SystemExit('BLOCKED: g++ unavailable')
records=[]
for flags in [['-O0'],['-O2'],['-O1','-fsanitize=undefined','-fno-sanitize-recover=all']]:
    with tempfile.TemporaryDirectory() as directory:
        executable=Path(directory)/'resource'
        command=[compiler,'-std=c++17','-Wall','-Wextra','-Werror',*flags,str(base/'resource.cpp'),'-o',str(executable)]
        build=subprocess.run(command,text=True,capture_output=True)
        row={'compiler_flags':command[1:-3],'build_exit':build.returncode,'build_stdout':build.stdout,'build_stderr':build.stderr}
        if build.returncode:print(json.dumps(row));raise SystemExit(1)
        run=subprocess.run([str(executable)],text=True,capture_output=True)
        row.update(run_exit=run.returncode,stdout=run.stdout,stderr=run.stderr);records.append(row)
        if run.returncode:print(json.dumps(row));raise SystemExit(1)
print(json.dumps({'python':sys.version,'platform':platform.platform(),'compiler':subprocess.check_output([compiler,'--version'],text=True).splitlines()[0],'runs':records,'scope':'local C++17 teaching mechanism, not all lifetime/ABI/concurrency rules'},indent=2))
