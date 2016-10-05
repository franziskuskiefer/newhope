#python3

import os
from hashlib import sha256
#return sha256(seed).hexdigest()

n = 1024
q = 12289

omega = 49
gamma = 9
omegamone = 1254
gammamone = 8778
nmone = 12277

def generate_a():
    # TODO: we should get 32 bytes and use SHAKE-128 here. boring uses AES-CTR.
    # We use the pure randomness here and parse it to a.
    a = []
    for i in range(0, n):
        seed = 0
        while True:
            seed = int.from_bytes(os.urandom(2), byteorder='little')
            seed = seed % 16384 # 2^14 = 16384
            if seed < q: # this is ok because values are public
                break
        a.append(seed)
    return a

# print("random: "+str(generate_a()))

def sample_error():
    # sample from binomial distribution (n 16)
    coefficients = []
    for i in range(0, n):
        # for that we first get uniformly distributed 16 bits
        urandom = int.from_bytes(os.urandom(4), byteorder='little')
        s = 0
        # now let's count the bits in each byte
        for j in range(0, 8):
            s += (urandom >> j) & 0x01010101
        lower = (s & 0xff) + ((s & 0xff00) >> 8)
        higher = ((s & 0xff0000) >> 16) + (s >> 24)
        coefficients.append(lower - higher + q)
    return coefficients

# print("error: "+str(sample_error()))

def poly_pw_mul(a, b):
    result = []
    for i in range(0, n):
        # we could do more efficient montgomery here (see ref and paper)
        result.append((a[i] * b[i]) % q)
    return result

def poly_add(a, b):
    result = []
    for i in range(0, n):
        # we could do more efficient barrett here (see ref and paper)
        result.append((a[i] + b[i]) % q)
    return result

def compute_b():
    # get two random coefficient sets and a
    ahat = generate_a()
    shat = sample_error()
    ehat = sample_error()

    # bhat = ahat * shat + ehat
    bhat = poly_pw_mul(ahat, shat)
    bhat = poly_add(bhat, ehat)
    return bhat


print("b: "+str(compute_b()))
