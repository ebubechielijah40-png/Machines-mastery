from crypto_lab import *

def run():
    assert sha256(b"a") != sha256(b"b")
    key=b"k"*32; msg=b"sensor=21.4"
    tag=make_hmac(key,msg)
    assert verify_hmac(key,msg,tag)
    assert not verify_hmac(key,msg+b"x",tag)
    salt=new_salt(); a=derive_password_key("pw",salt,1000); b=derive_password_key("pw",salt,1000)
    assert a==b and len(a)==32
    print("crypto_lab: PASS")
if __name__=='__main__': run()
