def compact_active(values):
    write=0
    for x in list(values):
        if x is not None:
            values[write]=x
            write+=1
    for i in range(write,len(values)):
        values[i]=None
    return write
