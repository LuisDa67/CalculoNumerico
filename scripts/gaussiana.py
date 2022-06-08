
def EGaussiana(A):
    '''
        Função Elimanação Gaussiana
        recebe:
            A-> Matriz aumentada do sistema linear
        retorna:
            x-> Array contendo o valor x0 a xn 
    '''
    # Tamanho da Matriz
    n= len(A)

    #Escalonamento de todas  linhas 
    for i in range(n-1):

        #pivo
        p=i
        while A[p,i]==0 and p<n+1:
            p+=1
            if A[p,i]==0:
                exit("O Pivô é nulo, o algoritmo falha!")
        #trocando linhas
        if p!=i:
            x = A[i].copy()
            A[i]=A[p]
            A[p]= x
        for l in range(i+1,n):
            m = A[l,i]/A[i,i]
            A[l]= A[l]- m*A[i]
    # Não posso iniciar a substituição regressiva
    if A[n-1,n-1]==0:
        exit("A[%d,%d] = 0, não existe solução única!" % (n-1,n-1) )
    #Regressão
    x = [0]*n
    x[n-1] = A[n-1,n]/A[n-1,n-1]
    for i in range(n-2,-1,-1):
        s = 0
        for j in range(i+1,n):
            s += A[i,j]*x[j]
        x[i] = (A[i,n] - s)/A[i,i]
    return x
