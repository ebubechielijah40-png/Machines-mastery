"""Atomic synthetic partition offset and grouped count effects, not a broker."""
OFFSET_KEY=-(1<<63)
SOURCE_KEY=OFFSET_KEY+1
MAX_TOTAL=(1<<63)-1


def consume(store,source,events,*,phase=lambda stage:None):
    if type(source) is not str or not 1<=len(source.encode('utf-8'))<=24:raise ValueError('source identity must be1..24 UTF-8 bytes')
    checked=[]
    for event in events:
        if len(checked)>=500:raise ValueError('at most500 events per call')
        if type(event) not in (tuple,list) or len(event)!=3:raise ValueError('(offset,group,delta) required')
        offset,group,delta=event
        if any(type(x) is not int for x in event) or not 1<=offset<=MAX_TOTAL or not 0<=group<=MAX_TOTAL or not -MAX_TOTAL<=delta<=MAX_TOTAL:
            raise ValueError('invalid event fields')
        if checked and offset!=checked[-1][0]+1:raise ValueError('batch offsets must be contiguous')
        checked.append(tuple(event))
    if not checked:raise ValueError('nonempty event batch required')
    before=store.snapshot()
    if before.rows.get(SOURCE_KEY,source)!=source:raise ValueError('source identity changed')
    offset=int(before.rows.get(OFFSET_KEY,'0'))
    if not 0<=offset<=MAX_TOTAL or str(offset)!=before.rows.get(OFFSET_KEY,'0'):raise ValueError('invalid retained offset')
    changes={};count=0
    for event_offset,group,delta in checked:
        if event_offset<=offset:continue
        if event_offset!=offset+1:raise ValueError('unseen intervening source event')
        old=changes[group] if group in changes else int(before.rows.get(group,'0'))
        total=old+delta
        if not -MAX_TOTAL<=total<=MAX_TOTAL:raise ValueError('total budget exceeded')
        changes[group]=total;offset=event_offset;count+=1
    if not count:return dict(applied_events=0,offset=offset,version=before.version)
    operations=[('put',SOURCE_KEY,source),('put',OFFSET_KEY,str(offset))]
    operations.extend(('put',k,str(v)) for k,v in sorted(changes.items()))
    version=store.commit(operations,expected_version=before.version,phase=phase)
    return dict(applied_events=count,offset=offset,version=version)
