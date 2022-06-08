from Spline import *

def newtonCotes(f,a,b,n):
    """
    Calcula a integral de uma função pelo método de Newton-Cotes

    Recebe:
        f       => Função a ser integrada
        a,b     => Intervalo de integração
        n       => Grau de integração
        verbose => Imprime passo a passo
    
    Retorna:
        Valor da Integral
    """
    if(n>4):    n=4
    h = (b-a)/float(n)
    x=[0]*(n+1)
    for i in range(n+1):
        x[i]=a+i*h
    n=int(n)

    if(n<=1):
        I= h*(f(x[0])+f(x[1]))/2
    elif(n==2):
        I = h*(f(x[0])+4*f(x[1])+f(x[2]))/3
    elif(n==3):
        I = 3*h*(f(x[0])+3*f(x[1])+3*f(x[2])+f(x[3]))/8
    elif(n==4):
        I = 2*h*(7*f(x[0])+32*f(x[1])+12*f(x[2])+32*f(x[3])+7*f(x[4]))/45
    return I;

def newtonCotes_Spline(f,a,b,n):
    """
    Calcula a integral de uma função pelo método de Newton-Cotes

    Recebe:
        f       => Lista para função de Spline
        a,b     => Intervalo de integração
        n       => Grau de integração
        verbose => Imprime passo a passo
    
    Retorna:
        Valor da Integral
    """
    if(n>4):    n=4
    h = (b-a)/float(n)
    x=[0]*(n+1)
    for i in range(n+1):
        x[i]=a+i*h
    n=int(n)
    coef = spline(f[0],f[1],f[2])
    if(n<=1):
        I= h*(pontoSpline(f[0],x[0],coef)+pontoSpline(f[0],x[1],coef))/2
    elif(n==2):
        I = h*(pontoSpline(f[0],x[0],coef)+4*pontoSpline(f[0],x[1],coef)+pontoSpline(f[0],x[2],coef))/3
    elif(n==3):
        I = 3*h*(pontoSpline(f[0],x[0],coef)+3*pontoSpline(f[0],x[1],coef)+3*pontoSpline(f[0],x[2],coef)+pontoSpline(f[0],x[3],coef))/8
    elif(n==4):
        I = 2*h*(7*pontoSpline(f[0],x[0],coef)+32*pontoSpline(f[0],x[1],coef)+12*pontoSpline(f[0],x[2],coef)+32*pontoSpline(f[0],x[3],coef)+7*pontoSpline(f[0],x[4],coef))/45
    return I;