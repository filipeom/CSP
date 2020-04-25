from Crypto.Util.number import *
import numpy as np
from copy import deepcopy
from random import randint


# p must me a prime number
def getGenerator(p):
    phi = p - 1

    for g in range(2, p):
        if pow(g, phi//2, p) in [-1, phi]:
            return g


def keyGeneration(p, g, n, r):
    
    #p prime, g generator of Zp, n size input
    def getPP(p, g, n):

        pp = [ [0 for _ in range(2)] for _ in range(n)]

        for j in range(n):
            for i in range(2):
                random = getRandomRange(2, p - 1)
                pp[j][i] = pow(g, random, p)
    
        return pp

    def matrixExponentiation(matrix, exp, i, b):

        for col in range(n):
            for row in range(2):
                if col == i and row == b:
                    matrix[i][b] = "T"
                else:
                    matrix[col][row] = pow(pp[col][row], exp, p)

        return matrix

    pp = getPP(p, g, n)

    rho = []
    ct  = []

    for i in range(n):
        ct_i  = []
        rho_i = []

        for b in range(2):
            M_ib   = []
            rho_ib = []
            
            for _ in range(r):
                rho_ib.append(getRandomRange(2, 4))

            for j in range(r):
                # pp remains intact
                M_ib_j = matrixExponentiation(deepcopy(pp), rho_ib[j], i, b)
                M_ib.append(M_ib_j)
            
            ct_i.append(M_ib)
            rho_i.append(rho_ib)

        rho.append(rho_i)
        ct.append(ct_i)

    ik = [pp, ct]
    tk = [pp, rho]

    # ro = [ro1, ro2, ..., ron]
    # ro1 = [ro10, ro11]
    # ro10 = [ro10, ..., ro10_r]

    # ct = [c1, c2, ..., cn]

    # c1 = [c10, c11]
    # c2 = [c20, c21]
    # cn = [cn0, cn1]
    
    # c10 = [M10, M20, ... Mn0]
    # c11 = [M11, M21, ... Mn1]

    return ik, tk, pp


def evaluation(ik, X, n, r):

    def HC(x):
        binary = [int(i) for i in bin(x)[2:]]
        res = 0
        for i in binary:
            res ^= i

        return res

    def multiplyMatrix(matrix, x, n):

        res = 1
        for j in range(n):
            x_j = x[j]
            if matrix[j][x_j] == "T":
                continue
            res = (res * matrix[j][x_j]) % p

        return res

    def Perm(u1, u2, xi):
        if xi == 0:
            return [u1, u2]
        else:
            return [u2, u1]

    x, b = X
    pp, ct = ik

    y = 1
    for j in range(n):
        x_j = x[j]
        y = (y * pp[j][x_j]) % p

    print ("y={}".format(y))
    e = []
    for i in range(n):
        e_i = []
        for j in range(r):
            x_i = x[i]
            M_i_xi_r = ct[i][x_i][j]
            e_i.append(HC(multiplyMatrix(M_i_xi_r, x, n)))
        e.append(e_i)

    Y = []
    Y.append(y)
    Y.append([])

    # permutations
    for i in range(len(e)):
        # print ("{} {} {} -> {}".format(e[i], b[i], x[i], Perm(e[i], b[i], x[i])))
        Y[1].append(Perm(e[i], b[i], x[i]))

    return Y


def inversion(tk, Y):
    def HC(x):
        binary = [int(i) for i in bin(x)[2:]]
        res = 0
        for i in binary:
            res ^= i

        return res

    pp, rho = tk
    y, perm = Y

    x = []
    b = []

    for i in range(n):
        rho_i0 = rho[i][0]
        rho_i1 = rho[i][1]
        e_i0 = []
        e_i1 = []
        for j in range(len(rho_i0)):
            e_i0.append(HC(pow(y, rho_i0[j], p)))
            e_i1.append(HC(pow(y, rho_i1[j], p)))
        e = []
        e.append(e_i0)
        e.append(e_i1)
        print(perm[i][0] == e_i0)
        print(perm[i][1] == e_i1)


#security parameters

bits = 10
r = 10

p = getPrime(bits)
g = getGenerator(p)
x = [0,0,0,1,1,1]
n = len(x)
b = []

for i in range(n):
    b.append([])
    for _ in range(r):
        b[i].append(randint(0,1))

print ("p={}".format(p))
print ("g={}".format(g))
print ("n={}".format(n))

ik, tk, pp = keyGeneration(p, g, n, r)

Y = evaluation(ik, [x, b], n, r)

inversion(tk, Y)
