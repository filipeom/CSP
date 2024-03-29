from Crypto.Util.number import *

def getGenerator(p):
    for g in range(2, p - 1):
        if pow(g, (p-1)//2, p) in [-1, p - 1]:
            return g

def sampleGroupElement(g, p):
    return pow(g, getRandomRange(1, p - 1), p) 


def S(_lambda, n):
    '''Sampling algorithm

    Agrs:
        _lambda (int): security parameter, number of bits in p
        n (int): input length

    Returns:
        public hashkey:
            p (int): prime
            g (int): generator
            A (list): 

    '''
    
    def sampleA(p, g, n):
        A = []
        for i in range(n):
            gi0 = sampleGroupElement(g, p)
            gi1 = sampleGroupElement(g, p)
            A.append([gi0, gi1])
        return A


    p = getPrime(_lambda)
    g = getGenerator(p)
    A = sampleA(p, g, n)
    return (p, g, A)

#f_i(x) = x[i]

def G(hk, i):
    '''Generating algorithm

    Args:
        hk: public hash key
        i (int): index

    Returns:
        ek: encoding key
        td: trapdoor
    '''

    def sampleB(A, s, t, i, g, p):

        B = []
        n = len(A)
        for j in range(n):
            gj0 = A[j][0]
            gj1 = A[j][1]

            uj0 = pow(gj0, s, p)
            uj1 = pow(gj1, s, p) * (pow(g, t, p) if j == i else 1)  

            B.append([uj0, uj1])
        return B

    p, g, A = hk

    s = sampleGroupElement(g, p)
    t = sampleGroupElement(g, p)
    u = pow(g, s, p)
    B = sampleB(A, s, t, i, g, p)

    ek = (u, B)
    td = (s, t)
    
    return (ek, td)

def H(hk, x, r):
    '''Hashing algorithm

    Args:
        hk: Hash key
        x (tuple): bitstring
        r (int): randomness

    Returns:
        h (int): hash value
    '''

    p, g, A = hk
    h = pow(g, r, p)
    n = len(A)
    for j in range(n):
        h = (h * A[j][x[j]]) % p

    return h 

def E(ek, x, r, p):
    '''Encoding algorithm

    Args:
        ek: Encoding key
        x (tuple): bitstring
        r (int): randomness
        p (int): prime

    Returns:
        e (int): encoding
    '''

    u, B = ek
    e = pow(u, r, p)
    n = len(B)
    for j in range(n):
        e = (e * B[j][x[j]]) % p
    
    return e

def D(td, h, g, p):
    '''Decoding algorithm

    Args:
        td: trapdoor
        h (int): hash value
        g (int): generator
        p (int): prime

    Returns:
        e0 (int): zero-encoding
        e1 (int): one-encoding
    '''
    s, t = td

    e0 = pow(h, s, p)
    e1 = (pow(h, s, p) * pow(g, t, p)) % p
    return (e0, e1)

# Debug function to test the implemented functions
def debug():
    msg = "HELLO WORLD!"
    print ("Original message: {}".format(msg))
    msg = [bin(ord(i))[2:].rjust(8, "0") for i in msg]
    x = []
    for i in msg:
        for j in i:
            x.append(int(j))
    n = len(x)
    i = 1

    hk = S(8, n)
    p, g, A = hk
    ek, td = G(hk, i)
    r = sampleGroupElement(g, p)
    h = H(hk, x, r)
    e = E(ek, x, r, p)
    e0, e1 = D(td, h, g, p)
    print (" e:{}\ne0:{}\ne1:{}".format(e, e0, e1))
    if e0 == e:
        print ("bit shared is 0")
    elif e1 == e:
        print ("bit shared is 1")
    else:
        print ("smth wrong")
    print (x)
