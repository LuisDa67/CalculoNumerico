import numpy as np
from DecompLU import SL

def spline(arrayX,arrayY,derivadas=[]):
    #Tamanho dos vetores dados
    N = len(arrayX)
    # Criando Vetores
    arrayA= arrayY.copy()
    arrayH= np.zeros(N-1)
    for i in range(N-1):
        arrayH[i]= arrayX[i+1]-arrayX[i]
    
    #matrizes para resolver
    matrizA = np.zeros((N,N))
    matrizB = np.zeros(N)

    #Parte comum a fixa e livre
    for i in range(1, N-1):
        matrizA[i,i-1]=arrayH[i-1]
        matrizA[i,i]=2*(arrayH[i-1]+arrayH[i])
        matrizA[i,i+1]=arrayH[i]

        matrizB[i] = 3.0*(arrayA[i+1] - arrayA[i])/float(arrayH[i]) - 3.0*(arrayA[i] - arrayA[i-1])/float(arrayH[i-1])

    #Livre
    try:
        df0= derivadas[0]
        df1= derivadas[1]
        matrizA[0][0]   = 2*arrayH[0]
        matrizA[0][1]   = arrayH[0]
        matrizA[-1][-2] = arrayH[-2]
        matrizA[-1][-1] = 2*arrayH[-2]

        matrizB[0] = 3.0*(arrayA[1] - arrayA[0])/float(arrayH[0]) - 3*df0
        matrizB[-1] = 3*df1 - 3.0*(arrayA[-1] - arrayA[-2])/float(arrayH[-2])
    except:
        matrizA[0][0]   = 1.0
        matrizA[-1][-1] = 1.0

    #Resolvendo C
    arrayC = SL(matrizA,matrizB)
    arrayB= np.zeros(N-1)
    arrayD= np.zeros(N-1)

    for i in range(N-1):
        arrayB[i]=((arrayA[i+1]-arrayA[i])/float(arrayH[i]))-(arrayH[i]/3.0)*(2*arrayC[i]+arrayC[i+1])
        arrayD[i]=(arrayC[i+1]-arrayC[i])/float(3*arrayH[i])
    coef = np.zeros( (N-1,4) )
    for i in range(N-1):
        coef[i][0] = arrayA[i]
        coef[i][1] = arrayB[i]
        coef[i][2] = arrayC[i]
        coef[i][3] = arrayD[i]
    return coef

def pontoSpline(arrayX,x,coef):
    y = 0
    # try:
    #     n = len(x)
    #     y = np.zeros(n)
    #     for i in range(n):
    #         y[i] = pontoSpline( arrayX, x[i], coef )
    # except:
        # Encontra a posição de X dentro do vetor x
    k=0
    for i in range(len(arrayX)):
        if((x)>(arrayX[i])):
            k=i
        else: break
    if k==len(arrayX): k -= 1
    H = x - arrayX[k]
    ak = coef[k][0]
    bk = coef[k][1]
    ck = coef[k][2]
    dk = coef[k][3]
    y = ak + H*( bk + H*( ck + H*dk ) )

    return y
