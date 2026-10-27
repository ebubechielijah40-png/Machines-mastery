"""Actual object-semantic and local bytecode observations; no address dependence."""
import dis,json,platform,sys
from model import append_item,observations

def rebind(x):x=x+[2];return x

def augment(x):x += [2];return x

def observe():
    def shared_default(item,container=[]):container.append(item);return container
    first=shared_default('a');before_second=first.copy();second=shared_default('b')
    instructions={fn.__name__:[{'op':i.opname,'argument':i.argrepr} for i in dis.get_instructions(fn)] for fn in (rebind,augment)}
    return {'environment':{'python':sys.version,'implementation':platform.python_implementation(),'platform':platform.platform()},'semantic_observations':observations(),'default_argument':{'after_first':before_second,'after_second':second,'same_container':first is second,'fresh_none_default_calls':[append_item('a'),append_item('b')]},'local_bytecode':instructions,'scope':'selected list/tuple/copy semantics; local disassembly is not a portable ABI'}

if __name__=='__main__':print(json.dumps(observe(),indent=2))
