"""Original demonstrations with semantic, not address-specific, assertions."""
import copy

def observations():
    a=[[1],[2]];b=a;c=a.copy();d=copy.deepcopy(a)
    initial={'alias_same':b is a,'shallow_outer_distinct':c is not a,'shallow_inner_same':c[0] is a[0],'deep_inner_distinct':d[0] is not a[0]}
    b[0].append(9)
    initial.update(after_mutation={'a':a,'b':b,'shallow':c,'deep':d})
    t=([1],);t[0].append(2);initial['tuple_contains_changed_list']=t[0]
    x=[1];y=x;x=x+[2];initial['rebind_does_not_mutate_alias']=(x,y)
    x=[1];y=x;x += [2];initial['augmented_list_mutates_alias']=(x,y)
    return initial


def append_item(item,container=None):
    if container is None:container=[]
    container.append(item);return container
