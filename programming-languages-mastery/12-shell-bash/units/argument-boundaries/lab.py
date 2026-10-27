"""Controlled Bash expansion observations. Only temporary local files are used."""
from pathlib import Path
import json,os,platform,shutil,subprocess,sys,tempfile

BASE=Path(__file__).resolve().parent
PREFIX='python=$1; helper=$2; shift 2; '
FORMS={
    'quoted_at':PREFIX+'"$python" "$helper" "$@"',
    'unquoted_at':PREFIX+'"$python" "$helper" $@',
    'quoted_star':PREFIX+'"$python" "$helper" "$*"',
    'quoted_array':'python=$1; helper=$2; items=("two words" "" "*.txt"); "$python" "$helper" "${items[@]}"',
    'command_substitution':'python=$1; helper=$2; value=$(printf "a\\n\\n"); "$python" "$helper" "$value"',
}

def run_case(script,values,directory):
    bash=shutil.which('bash')
    if bash is None:raise RuntimeError('BLOCKED: bash unavailable')
    # Environment removes inherited shell startup/options and controls glob ordering.
    environment={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'LC_ALL':'C'}
    result=subprocess.run([bash,'--noprofile','--norc','-c',script,'lab',sys.executable,str(BASE/'argv.py'),*values],cwd=directory,env=environment,text=True,capture_output=True,check=True)
    return json.loads(result.stdout)


def observe():
    with tempfile.TemporaryDirectory() as directory:
        for name in ('alpha.txt','two words.txt','other.bin'):(Path(directory)/name).write_text('local synthetic file')
        values=['two words','','*.txt']
        rows={name:run_case(script,values,directory) for name,script in FORMS.items()}
        rows['empty_at']=run_case(FORMS['quoted_at'],[],directory)
        rows['metacharacters']=run_case(FORMS['quoted_at'],['$(touch marker)','a; b','--leading-option'],directory)
        rows['marker_exists']=(Path(directory)/'marker').exists()
        bash=shutil.which('bash');environment={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'LC_ALL':'C'}
        for label,script in [('pipeline_default','false | true; printf "%s" "$?"'),('pipeline_pipefail','set -o pipefail; false | true; printf "%s" "$?"')]:
            result=subprocess.run([bash,'--noprofile','--norc','-c',script],cwd=directory,env=environment,text=True,capture_output=True,check=True)
            rows[label]=int(result.stdout)
        return {'environment':{'python':sys.version,'platform':platform.platform(),'bash':subprocess.check_output([bash,'--version'],text=True).splitlines()[0]},'inputs':values,'observations':rows,'scope':'local controlled argv/filename expansion; no eval or external service'}

if __name__=='__main__':print(json.dumps(observe(),indent=2))
