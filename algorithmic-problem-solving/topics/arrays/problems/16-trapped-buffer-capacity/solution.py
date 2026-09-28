def trapped_water(heights):
    l=0; r=len(heights)-1; lm=rm=0; total=0
    while l<=r:
        if lm <= rm:
            lm=max(lm,heights[l]); total+=lm-heights[l]; l+=1
        else:
            rm=max(rm,heights[r]); total+=rm-heights[r]; r-=1
    return total
