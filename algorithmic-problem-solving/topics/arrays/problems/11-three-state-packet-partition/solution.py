def dutch_flag(values):
    low=mid=0; high=len(values)-1
    while mid<=high:
        if values[mid]==0:
            values[low],values[mid]=values[mid],values[low]; low+=1; mid+=1
        elif values[mid]==1:
            mid+=1
        elif values[mid]==2:
            values[mid],values[high]=values[high],values[mid]; high-=1
        else:
            raise ValueError("only 0,1,2 allowed")
    return values
