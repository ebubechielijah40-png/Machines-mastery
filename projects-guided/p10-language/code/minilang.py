"""Original bounded rational expression language. No eval/exec/Python parser.

Statements: let name = expression; or expression; . Arithmetic is exact Fraction.
A program's environment changes commit only if all statements evaluate.
"""
from dataclasses import dataclass
from fractions import Fraction
import re

MAX_SOURCE=16_384
MAX_TOKENS=4096
MAX_DEPTH=64
MAX_STEPS=10_000
MAX_INTEGER_BITS=4096

class LanguageError(ValueError):pass
@dataclass(frozen=True)
class Token:
    kind:str
    text:str
    offset:int


def tokenize(source):
    if not isinstance(source,str):raise LanguageError('source must be a string')
    if len(source)>MAX_SOURCE:raise LanguageError('source length limit')
    tokens=[];position=0
    while position<len(source):
        c=source[position]
        if c.isspace():position+=1;continue
        if c=='#':
            end=source.find('\n',position);position=len(source) if end<0 else end;continue
        match=re.match(r'[0-9]+|[A-Za-z_][A-Za-z_0-9]*|[+*/()=;\-]',source[position:])
        if not match:raise LanguageError(f'unexpected character at {position}')
        text=match.group();kind='int' if text[0].isdigit() else 'name' if text[0].isalpha() or text[0]=='_' else text
        if text=='let':kind='let'
        tokens.append(Token(kind,text,position));position+=len(text)
        if len(tokens)>MAX_TOKENS:raise LanguageError('token count limit')
    tokens.append(Token('eof','',len(source)));return tuple(tokens)


class Parser:
    def __init__(self,tokens):self.tokens=tokens;self.index=0
    def peek(self):return self.tokens[self.index]
    def take(self,kind):
        token=self.peek()
        if token.kind!=kind:raise LanguageError(f'expected {kind} at {token.offset}, got {token.kind}')
        self.index+=1;return token
    def program(self):
        result=[]
        while self.peek().kind!='eof':
            if self.peek().kind=='let':
                self.take('let');name=self.take('name').text;self.take('=');expr=self.expression(0);result.append(('let',name,expr))
            else:result.append(('expr',self.expression(0)))
            self.take(';')
        return tuple(result)
    def expression(self,depth):
        node=self.term(depth+1)
        while self.peek().kind in ('+','-'):
            op=self.peek().kind;self.take(op);node=(op,node,self.term(depth+1))
        return node
    def term(self,depth):
        node=self.unary(depth+1)
        while self.peek().kind in ('*','/'):
            op=self.peek().kind;self.take(op);node=(op,node,self.unary(depth+1))
        return node
    def unary(self,depth):
        if depth>MAX_DEPTH:raise LanguageError('syntax nesting limit')
        if self.peek().kind in ('+','-'):
            op=self.peek().kind;self.take(op);return ('unary'+op,self.unary(depth+1))
        token=self.peek()
        if token.kind=='int':
            self.take('int')
            if len(token.text)>1200:raise LanguageError('integer literal length limit')
            value=int(token.text)
            if value.bit_length()>MAX_INTEGER_BITS:raise LanguageError('integer bit limit')
            return ('number',value)
        if token.kind=='name':self.take('name');return ('name',token.text)
        if token.kind=='(':
            self.take('(');node=self.expression(depth+1);self.take(')');return node
        raise LanguageError(f'expected expression at {token.offset}')


def parse(source):return Parser(tokenize(source)).program()


def evaluate(source,environment=None):
    """Return output Fractions and commit bindings only after complete success.

    Mutable caller dict is optional. Each input value must be int or Fraction.
    This process is a teaching language, not a hardened hosted execution sandbox.
    """
    if environment is None:environment={}
    if not isinstance(environment,dict):raise LanguageError('environment must be a dictionary')
    if any(not isinstance(k,str) or type(v) not in (int,Fraction) for k,v in environment.items()):raise LanguageError('environment maps names to int/Fraction')
    local={k:Fraction(v) for k,v in environment.items()};program=parse(source);steps=0
    def checked(value):
        if max(value.numerator.bit_length(),value.denominator.bit_length())>MAX_INTEGER_BITS:raise LanguageError('rational bit limit')
        return value
    def visit(node,depth=0):
        nonlocal steps
        steps+=1
        if steps>MAX_STEPS:raise LanguageError('evaluation step limit')
        if depth>MAX_DEPTH:raise LanguageError('expression tree depth limit')
        op=node[0]
        if op=='number':return Fraction(node[1])
        if op=='name':
            if node[1] not in local:raise LanguageError('unbound name: '+node[1])
            return checked(local[node[1]])
        if op in ('unary+','unary-'):
            value=visit(node[1],depth+1);return value if op=='unary+' else -value
        left,right=visit(node[1],depth+1),visit(node[2],depth+1)
        if op=='+':result=left+right
        elif op=='-':result=left-right
        elif op=='*':result=left*right
        else:
            if right==0:raise LanguageError('division by zero')
            result=left/right
        return checked(result)
    outputs=[]
    for statement in program:
        if statement[0]=='let':local[statement[1]]=visit(statement[2])
        else:outputs.append(visit(statement[1]))
    environment.clear();environment.update(local)
    return outputs


if __name__=='__main__':
    import sys
    try:
        for value in evaluate(sys.stdin.read()):print(value)
    except LanguageError as error:
        print(f'language error: {error}',file=sys.stderr);raise SystemExit(2)
