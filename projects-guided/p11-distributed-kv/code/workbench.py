"""Execute explicit local replica schedules, without a network or persistent store."""
from dataclasses import asdict
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'15-distributed-systems'/'ordering-reconciliation'))
from reconcile import Replica


def scenario(document):
    if not isinstance(document,dict) or set(document)!={'nodes','events'}:
        raise ValueError('scenario needs exact nodes/events schema')
    nodes,events=document['nodes'],document['events']
    if not isinstance(nodes,list) or not 1<=len(nodes)<=8 or any(not isinstance(n,str) for n in nodes):
        raise ValueError('one to eight named nodes required')
    if len(set(nodes))!=len(nodes):raise ValueError('duplicate node identity')
    if not isinstance(events,list) or len(events)>200:raise ValueError('at most200 events')
    replicas={name:Replica(name) for name in nodes}
    messages={};trace=[]
    schemas={'put':{'op','node','key','value'},'delete':{'op','node','key'},
             'send':{'op','node','as'},'deliver':{'op','node','message'},'read':{'op','node'}}
    for step,event in enumerate(events):
        if not isinstance(event,dict) or not isinstance(event.get('op'),str):
            raise ValueError('event must be a typed object')
        op=event['op']
        if op not in schemas or set(event)!=schemas[op]:raise ValueError('unsupported event/schema')
        name=event['node']
        if not isinstance(name,str) or name not in replicas:raise ValueError('unknown node')
        replica=replicas[name]
        record={'step':step,'op':op,'node':name}
        if op=='put':
            if not isinstance(event['value'],str):raise ValueError('put needs string value; use delete for tombstones')
            record['write']=asdict(replica.put(event['key'],event['value']))
        elif op=='delete':record['write']=asdict(replica.delete(event['key']))
        elif op=='send':
            label=event['as']
            if not isinstance(label,str) or not 1<=len(label)<=64 or label in messages:
                raise ValueError('unique bounded message label required')
            messages[label]=replica.send()
            record.update(message=label,send_counter=messages[label].counter)
        elif op=='deliver':
            label=event['message']
            if not isinstance(label,str) or label not in messages:raise ValueError('unknown message')
            record.update(message=label,state_changed=replica.receive(messages[label]))
        else:record['visible']=replica.visible()
        record['clock']=replica.clock.value
        trace.append(record)
    return {'kind':'specified local replica schedule; no network, persistence or consensus',
            'trace':trace,'replicas':{name:{'clock':r.clock.value,'visible':r.visible(),
                 'records':[asdict(item) for item in r.snapshot()]} for name,r in replicas.items()}}


def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('duplicate JSON field')
        result[key]=value
    return result


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario',type=Path)
    args=parser.parse_args()
    try:
        # Read a bounded prefix too, so a changing file cannot bypass stat.
        with args.scenario.open('rb') as source:data=source.read(1_000_001)
        if len(data)>1_000_000:raise ValueError('scenario above1MB input bound')
        document=json.loads(data.decode('utf-8'),object_pairs_hook=unique_object)
        result=scenario(document)
    except (OSError,ValueError,UnicodeError) as exc:
        print(f'workbench: {exc}',file=sys.stderr)
        return 2
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
