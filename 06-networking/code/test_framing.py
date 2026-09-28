from framing import *
def run():
    wire=encode(b'abc')+encode(b'xyz')
    d=Decoder(); out=[]
    for b in wire: out += d.feed(bytes([b]))
    assert out==[b'abc',b'xyz']
    d=Decoder(); assert d.feed(wire)==[b'abc',b'xyz']
    try: Decoder(2).feed(encode(b'abc')); assert False
    except ValueError: pass
    print('network framing: PASS')
if __name__=='__main__': run()
