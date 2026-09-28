from dataclasses import dataclass, field
@dataclass
class Replica:
    name:str
    data:dict=field(default_factory=dict)
    seen:set=field(default_factory=set)
    def apply(self,event_id,key,value):
        if event_id in self.seen: return False
        self.seen.add(event_id); self.data[key]=value; return True

def deliver(replica,events):
    return [replica.apply(*e) for e in events]
