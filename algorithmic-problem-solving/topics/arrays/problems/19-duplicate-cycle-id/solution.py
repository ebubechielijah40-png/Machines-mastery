def find_duplicate(values):
    if len(values)<2: raise ValueError("invalid input")
    n=len(values)-1
    if any(not isinstance(v,int) or v<1 or v>n for v in values): raise ValueError("values out of range")
    slow=values[0]; fast=values[values[0]]
    while slow!=fast:
        slow=values[slow]; fast=values[values[fast]]
    slow=0
    while slow!=fast:
        slow=values[slow]; fast=values[fast]
    return slow
