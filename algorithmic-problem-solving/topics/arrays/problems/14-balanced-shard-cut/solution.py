def equilibrium_indices(values):
    total=sum(values); left=0; out=[]
    for i,x in enumerate(values):
        right=total-left-x
        if left==right: out.append(i)
        left+=x
    return out
