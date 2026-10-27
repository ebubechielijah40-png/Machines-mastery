"""Original bounded byte-pair merge tokenizer, not any production BPE format."""
from collections import Counter


class BytePairTokenizer:
    def __init__(self,training_text,merges=8):
        if not isinstance(training_text,str) or len(training_text.encode())>100_000:
            raise ValueError('bounded training text required')
        if type(merges) is not int or not 0<=merges<=100:
            raise ValueError('merges must be0..100')
        self.bytes={i:bytes([i]) for i in range(256)};self.merges=[]
        ids=list(training_text.encode('utf-8'))
        for _ in range(merges):
            counts=Counter(zip(ids,ids[1:]))
            if not counts:break
            pair=min(counts,key=lambda p:(-counts[p],p))
            token=256+len(self.merges)
            self.bytes[token]=self.bytes[pair[0]]+self.bytes[pair[1]]
            self.merges.append((pair,token));ids=self.replace(ids,pair,token)

    @staticmethod
    def replace(ids,pair,token):
        result=[];i=0
        while i<len(ids):
            if i+1<len(ids) and (ids[i],ids[i+1])==pair:
                result.append(token);i+=2
            else:result.append(ids[i]);i+=1
        return result

    def encode(self,text):
        if not isinstance(text,str):raise ValueError('text must be str')
        ids=list(text.encode('utf-8'))
        for pair,token in self.merges:ids=self.replace(ids,pair,token)
        return ids

    def decode(self,ids):
        ids=list(ids)
        if any(type(i) is not int or i not in self.bytes for i in ids):raise ValueError('invalid token IDs')
        return b''.join(self.bytes[i] for i in ids).decode('utf-8')
