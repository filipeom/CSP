# -- coding: utf-8 --
import random
import argparse

from tdh_ddh import *

def bOT1(_lambda, k,  inp):
    # inp
    # 0 .. k   |
    # 0 .. k   | 
    # 0 .. k   |   N
    #  ...     | 
    # 0 .. k   | 
    n = len(inp)
    hk = S(_lambda, k * n)

    msg1 = [hk]
    st   = [inp, hk]
    for j in range(n):
        ekj, tdj = G(hk, j * k + inp[j])
        st.append(tdj)
        msg1.append(ekj)

    return (st, msg1)

def bOT2(msg1, secrets):

    hk, ek = msg1[0], msg1[1:]

    p, g = hk[0], hk[1]
    r = sampleGroupElement(g, p)
    new_secrets = [bit for secret in secrets for bit in secret]

    n = len(secrets)
    h = H(hk, new_secrets, r)
    e = [E(ek[j], new_secrets, r, p) for j in range(n)]

    msg2 = [h] + e
    return msg2


def bOT3(st, msg2):
    

    inp, hk, td = st[0], st[1], st[2:]
    h, e = msg2[0], msg2[1:]
    p, g = hk[0], hk[1]

    s = []
    n = len(inp)
    for j in range(n):
        ej0, ej1 = D(td[j], h, g, p)

        if ej0 == ej1:
            s.append(-1)
        
        elif e[j] == ej0:
            s.append(0)

        elif e[j] == ej1:
            s.append(1)

    return s

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sp', type=int, help='Security Parameter')
    parser.add_argument('k',  type=int)
    parser.add_argument('n',  type=int)
    args = parser.parse_args()

    sp = args.sp
    k  = args.k
    n  = args.n

    secrets = [[random.randint(0, 1) for i in range(k)] for i in range(n)]

    inp = [random.randint(0, k-1) for _ in range(n)]
    print ("Bob has secrets:")
    i = 0
    for si in secrets:
        print ("s{} -> {}".format(i, si))
        i += 1

    st, msg1 = bOT1(sp, k, inp)
    msg2 = bOT2(msg1, secrets)
    s = bOT3(st, msg2)

    print ("Alice retrived:")
    for i in range(len(s)):
        print ("The {}th bit from s{}, which is: {}".format(inp[i]+1, i, s[i]))

    # Verify correctness
    fail = False
    for i in range(n):
        if secrets[i][inp[i]] != s[i]:
            fail = True

    print ("SUCCESS={}".format(not fail))

main()
