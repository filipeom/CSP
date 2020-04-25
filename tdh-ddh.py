from Crypto.Util.number import *

def getGenerator(p):
    for g in range(2, p - 1):
        if pow(g, (p-1)//2, p) in [-1, p - 1]:
            return g

def sampleA(p, g, n):
    A = []
    for j in range(n):
        A.append([])
        for b in range(2 * n):
           A[j].append(pow(g, getRandomRange(0, p - 1), p))
    return A

def sampleB(A, p, g, n, s, t, i):
    B = []
    for j in range(n):
        B.append([])
        for b in range(2 * i, 2 * (i + 1)):
            u_jb = (pow(A[j][b], s, p) * pow(g, t, p)) % p if j == i and b == (2 * i + 1) else pow(A[j][b], s, p)
            B[j].append(u_jb)
    return B

def main():
    msg = "HELLO WORLD!"
    print ("Original message: {}".format(msg))
    msg = [bin(ord(i))[2:].rjust(8, "0") for i in msg]
    x = []
    for i in msg:
        for j in i:
            x.append(int(j))
    n = len(x)
    i = 1
    # begin S
    p = getPrime(16)
    g = getGenerator(p)
    A = sampleA(p, g, n)
    # end S
    # begin G
    s = [getRandomRange(2, p - 1) for _ in range(n)]
    t = [getRandomRange(2, p - 1) for _ in range(n)]
    u = [pow(g, s_i, p) for s_i in s]
    B = [sampleB(A, p, g, n, s[i], t[i], i) for i in range(n)]
    # end G
    # being H
    r = [getRandomRange(2, p - 1) for _ in range(n)]
    h = [pow(g, r[i], p) for i in range(n)]
    for i in range(n):
        for j in range(n):
            x_j = x[j]
            h[i] = (h[i] * A[j][2 * i + x_j]) % p
    # end H
    # begin E
    e = [pow(u[i], r[i], p) for i in range(n)]
    for i in range(n):
        for j in range(n):
            x_j = x[j]
            e[i] = (e[i] * B[i][j][x_j]) % p
    # end E
    e_0 = [pow(h[i], s[i], p) for i in range(n)]
    e_1 = [(e_0[i] * pow(g, t[i], p)) % p for i in range(n)]

    msg = ""
    cnt = 0
    char = []
    for i in range(n):

        if e[i] == e_0[i]:
            char.append(0)
        elif e[i] == e_1[i]:
            char.append(1)
        else:
            print ("Error")
        
        cnt += 1    

        if cnt == 8:
            msg += chr(int("".join(str(c) for c in char),2))
            char = []
            cnt = 0
    
    print ("Received message: {}".format(msg))


main()
