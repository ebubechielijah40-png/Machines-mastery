def move_zeros(values):
    write=0
    for x in values:
        if x!=0:
            values[write]=x; write+=1
    for i in range(write,len(values)):
        values[i]=0
    return values
