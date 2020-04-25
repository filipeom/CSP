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
    
        pp = [ [0 for _ in range(n)] for _ in range(2)]

        for i in range(2):
            for j in range(n):
                random = getRandomRange(2, p - 1)
                pp[i][j] = pow(g, random, p)

        return pp

    def matrixExponentiation(matrix, exp, i, b):

        for row in range(2):
            
            for col in range(n):
    
                if row == i and col == b:
                    matrix[i][b] = "T"
                else:
                    matrix[row][col] = pow(pp[row][col], exp)

        return matrix

    pp = getPP(p, g, n)

    rho = []
    ct  = []
    M   = []

    for i in range(n):


        for b in range(2):
            rho_ib = []
            M_ib   = []
            ct_ib  = []
            
            for _ in range(r):
                randomNumber = getRandomRange(2, 100)
                rho_ib.append(randomNumber)

            for j in range(r):
                # pp remains intact
                M_ib_j = matrixExponentiation(deepcopy(pp), rho_ib[j], i, b)
                M_ib.append(M_ib_j)
            
            ct_ib.append(M_ib)
    
        rho.append(rho_ib)
        M.append(M_ib)
        ct.append(ct_ib)

    ik = [pp, ct]
    tk = [rho]

    return ik, tk, pp



def evaluation(ik, X, pp, n):
    x, b = X

    y = 1
    for i in range(2):
        for j in range(n):
            y = y * pp[i][x[j]] % p


    print ("y={}".format(y))

#security parameters

bits = 10
r = 6


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


evaluation(ik, [x, b], pp, n)