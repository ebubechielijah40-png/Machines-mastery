"""Original finite GCM tag reconstruction for96-bit nonces/full128-bit tags.

Not used to protect ledger data. AES block encryption comes from cryptography;
field multiplication, padding, length binding and GHASH are explicit here.
"""
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes


def field_multiply(x,y):
    if any(type(v) is not int or not 0<=v<2**128 for v in (x,y)):raise ValueError('128-bit integer operands required')
    result=0;shifted=y
    for bit in range(127,-1,-1):
        if (x>>bit)&1:result^=shifted
        low=shifted&1;shifted>>=1
        if low:shifted^=0xe1000000000000000000000000000000
    return result


def checked_bytes(value,maximum):
    if type(value) is not bytes or len(value)>maximum:raise ValueError('bounded exact bytes required')


def ghash(h,aad,ciphertext):
    checked_bytes(h,16)
    if len(h)!=16:raise ValueError('128-bit hash subkey required')
    checked_bytes(aad,65536);checked_bytes(ciphertext,65536)
    data=aad+b'\0'*((-len(aad))%16)+ciphertext+b'\0'*((-len(ciphertext))%16)
    data+=(8*len(aad)).to_bytes(8,'big')+(8*len(ciphertext)).to_bytes(8,'big')
    state=0;factor=int.from_bytes(h,'big')
    for offset in range(0,len(data),16):state=field_multiply(state^int.from_bytes(data[offset:offset+16],'big'),factor)
    return state.to_bytes(16,'big')


def reconstructed_tag(key,nonce,aad,ciphertext):
    checked_bytes(key,32);checked_bytes(nonce,12)
    if len(key) not in (16,24,32) or len(nonce)!=12:raise ValueError('AES key and96-bit nonce required')
    cipher=Cipher(algorithms.AES(key),modes.ECB()).encryptor()
    blocks=cipher.update(b'\0'*16+nonce+b'\0\0\0\1')+cipher.finalize()
    h,mask=blocks[:16],blocks[16:]
    return bytes(a^b for a,b in zip(ghash(h,aad,ciphertext),mask))
