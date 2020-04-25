from Crypto.Util.number import *
import numpy as np
from copy import deepcopy


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
                    matrix[col][row] = pow(pp[col][row], exp)

        return matrix

    pp = getPP(p, g, n)

    rho = []
    ct  = []

    for i in range(n):
        ct_ib  = []

        for b in range(2):
            rho_ib = []
            M_ib   = []
            
            for _ in range(r):
                randomNumber = getRandomRange(2, 4)
                rho_ib.append(randomNumber)

            for j in range(r):
                # pp remains intact
                M_ib_j = matrixExponentiation(deepcopy(pp), rho_ib[j], i, b)
                M_ib.append(M_ib_j)
            
            ct_ib.append(M_ib)

        rho.append(rho_ib)
        ct.append(ct_ib)

    ik = [pp, ct]
    tk = [rho]

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
            res *= matrix[j][x_j]

        return res

    x, b = X
    pp, ct = ik

    y = 1
    for j in range(n):
        x_j = x[j]
        y = (y * pp[j][x_j]) % p

    e = []
    for i in range(n):
        e_i = []
        for j in range(r):
            x_i = x[i]
            M_i_xi_r = ct[i][x_i][j]
            e_i.append(HC(multiplyMatrix(M_i_xi_r, x, n)))

    # permutations

#security parameters

bits = 3
r = 4

p = getPrime(bits)
g = getGenerator(p)
n = 10
x = [0,1,1,1,1,1,1,1,1,0]

b = []
for i in range(n):
    b.append(getRandomNBitInteger(r))

print ("p={}".format(p))
print ("g={}".format(g))
print ("n={}".format(n))

ik, tk, pp = keyGeneration(p, g, n, r)

evaluation(ik, [x, b], n, r)