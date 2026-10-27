"""Actual bounded language traces, not interpreter performance evidence."""
import json,sys,platform
from minilang import parse,evaluate,LanguageError

def main():
    cases=[]
    for source in ['2+3*4;','(2+3)*4;','8/4/2;','let x=2; let x=x+3; x/2;','let x=9; 1/0;','let x=9; unknown;']:
        environment={'x':2};row={'source':source,'environment_before':{k:str(v) for k,v in environment.items()}}
        try:
            row['ast']=parse(source);row['outputs']=[str(x) for x in evaluate(source,environment)]
        except LanguageError as error:row['error']=str(error)
        row['environment_after']={k:str(v) for k,v in environment.items()};cases.append(row)
    print(json.dumps({'kind':'original synthetic language mechanism traces','python':sys.version,'platform':platform.platform(),'cases':cases},indent=2))
if __name__=='__main__':main()
