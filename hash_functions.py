import hashlib
from arithmetic import *


# These are hash functions from original article
# Due to implementation targets they are all the same


def hash(*args):
    h = hashlib.sha256()
    for item in args:
        h.update(str(item).encode(encoding='utf-8'))
    return Residue(int(h.hexdigest(), 16) % (Q - 1) + 1)  # mapping to Z_Q*


def hash1(*args):
    h = hashlib.sha256()
    for item in args:
        h.update(str(item).encode(encoding='utf-8'))
    return Residue(int(h.hexdigest(), 16) % (Q - 1) + 1)


def hash2(*args):
    h = hashlib.sha256()
    for item in args:
        h.update(str(item).encode(encoding='utf-8'))
    return Residue(int(h.hexdigest(), 16) % (Q - 1) + 1)
