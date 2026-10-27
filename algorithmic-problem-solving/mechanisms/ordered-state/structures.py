"""Original explicit hash buckets, stable binary heap and augmented unbalanced BST.

No dict/heapq/sorted is used to implement the mechanisms. They are independent
oracles in tests. Value objects are caller-owned; there is no thread safety.
"""
from dataclasses import dataclass


def byte_hash(key):
    if type(key) is not bytes: raise ValueError('immutable bytes key required')
    value = 0
    for byte in key: value = (257*value+byte) & ((1<<64)-1)
    return value


class ChainedMap:
    def __init__(self, hash_function=byte_hash):
        self._buckets = [[] for _ in range(4)]; self._count = 0; self._hash = hash_function
        self.key_comparisons = 0; self.rehashed_entries = 0

    def __len__(self): return self._count

    def _bucket(self,key, buckets=None):
        if type(key) is not bytes: raise ValueError('immutable bytes key required')
        code = self._hash(key)
        if type(code) is not int: raise ValueError('hash function must return an integer')
        return code % len(self._buckets if buckets is None else buckets)

    def _find(self,key):
        index = self._bucket(key); bucket = self._buckets[index]
        for j, (stored,_) in enumerate(bucket):
            self.key_comparisons += 1
            if key == stored: return index,j
        return index,None

    def __getitem__(self,key):
        i,j = self._find(key)
        if j is None: raise KeyError(key)
        return self._buckets[i][j][1]

    def __setitem__(self,key,value):
        i,j = self._find(key)
        if j is not None: self._buckets[i][j] = (key,value); return
        if 4*(self._count+1) > 3*len(self._buckets):
            # Compute a complete replacement before publishing new buckets.
            grown = [[] for _ in range(2*len(self._buckets))]
            for bucket in self._buckets:
                for k,v in bucket: grown[self._bucket(k,grown)].append((k,v))
            self.rehashed_entries += self._count; self._buckets = grown; i = self._bucket(key)
        self._buckets[i].append((key,value)); self._count += 1

    def __delitem__(self,key):
        i,j = self._find(key)
        if j is None: raise KeyError(key)
        del self._buckets[i][j]; self._count -= 1

    def items(self):
        # Snapshot, not a live iterator with unspecified mutation behavior.
        return tuple(item for bucket in self._buckets for item in bucket)

    def inspect(self):
        all_keys=[]
        for i,bucket in enumerate(self._buckets):
            for key,value in bucket:
                if self._bucket(key)!=i or key in all_keys: raise AssertionError('hash invariant violated')
                all_keys.append(key)
        if len(all_keys)!=self._count: raise AssertionError('count invariant violated')
        return {'capacity':len(self._buckets),'size':self._count,'max_chain':max(map(len,self._buckets)),'load':self._count/len(self._buckets)}


class StableHeap:
    def __init__(self,items=()):
        self._data = []; self._serial = 0; self.comparisons = 0
        for priority,value in items:
            self._priority(priority);self._data.append((priority,self._serial,value));self._serial+=1
        for i in range(len(self._data)//2-1,-1,-1): self._down(i)

    @staticmethod
    def _priority(priority):
        if type(priority) is not int: raise ValueError('integer priority required')

    def __len__(self):return len(self._data)

    def _less(self,a,b):
        self.comparisons+=1
        return a[:2]<b[:2]

    def _down(self,i):
        data=self._data
        while 2*i+1<len(data):
            child=2*i+1
            if child+1<len(data) and self._less(data[child+1],data[child]):child+=1
            if not self._less(data[child],data[i]):break
            data[i],data[child]=data[child],data[i];i=child

    def push(self,priority,value):
        self._priority(priority)
        self._data.append((priority,self._serial,value));self._serial+=1;i=len(self._data)-1
        while i:
            parent=(i-1)//2
            if not self._less(self._data[i],self._data[parent]):break
            self._data[i],self._data[parent]=self._data[parent],self._data[i];i=parent

    def pop(self):
        if not self._data:raise IndexError('empty priority queue')
        first=self._data[0];last=self._data.pop()
        if self._data:self._data[0]=last;self._down(0)
        return first[0],first[2]

    def inspect(self):
        for i in range(1,len(self._data)):
            if self._data[i][:2]<self._data[(i-1)//2][:2]:raise AssertionError('heap order violated')
        return {'size':len(self),'comparisons':self.comparisons}


@dataclass
class _Node:
    key:int
    value:object
    left:object=None
    right:object=None
    size:int=1


def size(node):return 0 if node is None else node.size


class SearchTree:
    def __init__(self):self._root=None;self.key_comparisons=0
    def __len__(self):return size(self._root)

    @staticmethod
    def _key(key):
        if type(key) is not int:raise ValueError('integer key required')

    def __getitem__(self,key):
        self._key(key);node=self._root
        while node is not None:
            self.key_comparisons+=1
            if key==node.key:return node.value
            node=node.left if key<node.key else node.right
        raise KeyError(key)

    def __setitem__(self,key,value):
        self._key(key);path=[];node=self._root
        while node is not None:
            self.key_comparisons+=1
            if key==node.key:node.value=value;return
            path.append(node);node=node.left if key<node.key else node.right
        new=_Node(key,value)
        if not path:self._root=new
        elif key<path[-1].key:path[-1].left=new
        else:path[-1].right=new
        for ancestor in reversed(path):ancestor.size=1+size(ancestor.left)+size(ancestor.right)

    def __delitem__(self,key):
        self._key(key);path=[];node=self._root
        while node is not None and node.key!=key:
            self.key_comparisons+=1;path.append(node);node=node.left if key<node.key else node.right
        if node is None:raise KeyError(key)
        self.key_comparisons+=1
        if node.left is not None and node.right is not None:
            path.append(node);successor=node.right
            while successor.left is not None:path.append(successor);successor=successor.left
            node.key,node.value=successor.key,successor.value
            # The last ancestor names which successor link gets spliced out.
            parent=path[-1]
            if parent.right is successor:parent.right=successor.right
            else:parent.left=successor.right
        else:
            child=node.left if node.left is not None else node.right
            if not path:self._root=child
            elif path[-1].left is node:path[-1].left=child
            else:path[-1].right=child
        for ancestor in reversed(path):ancestor.size=1+size(ancestor.left)+size(ancestor.right)

    def items(self):
        result=[];stack=[];node=self._root
        while stack or node is not None:
            while node is not None:stack.append(node);node=node.left
            node=stack.pop();result.append((node.key,node.value));node=node.right
        return tuple(result)

    def rank(self,key):
        self._key(key);node=self._root;count=0
        while node is not None:
            if key<=node.key:node=node.left
            else:count+=1+size(node.left);node=node.right
        return count

    def select(self,index):
        if type(index) is not int or not 0<=index<len(self):raise IndexError('rank outside tree')
        node=self._root
        while node is not None:
            left=size(node.left)
            if index==left:return node.key,node.value
            if index<left:node=node.left
            else:index-=left+1;node=node.right
        raise AssertionError('invalid size metadata')

    def inspect(self):
        if self._root is None:return {'size':0,'height':0}
        seen=set();heights={};sizes={};stack=[(self._root,None,None,False)]
        while stack:
            node,lower,upper,visited=stack.pop()
            if not visited:
                if id(node) in seen:raise AssertionError('cycle or shared subtree')
                seen.add(id(node))
                if (lower is not None and node.key<=lower) or (upper is not None and node.key>=upper):raise AssertionError('search order violated')
                stack.append((node,lower,upper,True))
                if node.right is not None:stack.append((node.right,node.key,upper,False))
                if node.left is not None:stack.append((node.left,lower,node.key,False))
            else:
                computed=1+sizes.get(id(node.left),0)+sizes.get(id(node.right),0)
                if computed!=node.size:raise AssertionError('size metadata violated')
                sizes[id(node)]=computed;heights[id(node)]=1+max(heights.get(id(node.left),0),heights.get(id(node.right),0))
        return {'size':len(seen),'height':heights[id(self._root)]}
