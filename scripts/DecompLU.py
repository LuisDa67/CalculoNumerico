import numpy as np

def DecompositionLU(A):
    n=len(A)
    A = np.asarray(A)
    LU = [[0.0]*n]*n
    LU = np.asarray(LU)
    for i in range(n):
        for j in range(n):
            if i>=j:
                aux=0
                for k in range(j):
                    aux += LU[i,k]*LU[k,j]
                LU[i,j]= A[i,j]-aux
            else:
                aux=0
                for k in range(i):
                    aux += LU[i,k]*LU[k,j]
                LU[i,j]= (A[i,j]-aux)/LU[i,i]
    return LU

def Regression(LU,B):
    n=len(B)
    Y= [0]*n
    for i in range(n):
        aux=0
        for k in range(i):
            aux+=LU[i,k]*Y[k]
        Y[i]=(B[i]-aux)/LU[i,i]
    X = [0]*n
    for i in range(n-1,-1,-1):
        aux=0
        for k in range(n-1,i-1,-1):
            aux +=LU[i,k]*X[k]
        X[i]=Y[i]-aux
    return X

def SL(A,B):
    return Regression(DecompositionLU(A),B)