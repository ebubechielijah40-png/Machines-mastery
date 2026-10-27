"""PUBLIC deterministic keys for reproducible tests, never real secrets."""
from pathlib import Path
from protected_ledger import Configuration,WriterEpoch,EncryptionEpoch,Witness,ProtectedLedger,sign_versioned


def configuration():
    return Configuration((WriterEpoch('alpha','alpha-old',b'a'*32,1,2,frozenset({'room'})),
                          WriterEpoch('alpha','alpha-new',b'b'*32,3,10000,frozenset({'room'})),
                          WriterEpoch('beta','beta-key',b'c'*32,1,10000,frozenset({'lab'}))),
                         (EncryptionEpoch('cipher-old',b'd'*32,1,2),EncryptionEpoch('cipher-new',b'e'*32,3,10000)))


def resources(directory):
    root=Path(directory);config=configuration()
    witness=Witness(root/'authority.db','observations',config.fingerprint(),b'w'*32)
    ledger=ProtectedLedger(root/'ledger.db','observations',config,witness,witness.public_key)
    return config,witness,ledger


def observation(sequence,value=25001,producer='alpha'):
    if producer=='beta':return sign_versioned(b'c'*32,'beta-key','beta','lab',sequence,value)
    return sign_versioned(b'a'*32 if sequence<=2 else b'b'*32,'alpha-old' if sequence<=2 else 'alpha-new','alpha','room',sequence,value)
