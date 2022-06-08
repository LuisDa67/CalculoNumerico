from NewtonCotes import newtonCotes,newtonCotes_Spline
import numpy as np
from bisseccao import Bisseccao
# import random
import matplotlib.pylab as plt


def MValor(param):
    '''
        função para calcular anomalia média
            recebe:
            param - > t = tempo de orbita  P = Lei do Período orbital
    '''
    t=param[0]
    P=param[1]
    return (((np.pi*2)*t)/P)

def EValor(p,param):
    '''
        função para calcular a Anomalia excêntrica
        recebe:
            p-> usada no metódo da bissecção
            param -> M =anomalia média e e = excentricidade
    '''
    M=param[0]
    e = param[1]
    return p-e*np.sin(p)-M

def AnguloValor(param):
    '''
        função para calcular angulo em dado instante
            recebe:
            param - > E = anomalia média  e = excentricidade
    '''
    E=param[0]
    e=param[1]
    return np.arctan(np.sqrt((1+e)/(1-e))*np.tan(E/2))*2

def DistValor(param):
    '''
        função para calcular distancia do foco
            recebe:
            param - > angulo-> angulo com o eixo x, e = excentricidade e a-> parametro de orbita
    '''
    angulo = param[0]
    e= param[1]
    a= param[2]
    return a*((1-e**2)/(1+e*np.cos(angulo)))

def pontoElipse(t,xc,a,b):
    '''
        função para valores de y para x da elipse
            recebe:
            t
            xc,a,b -> parametro de orbita
    '''
    e= np.sqrt(1-(b**2/a**2))
    f=a*e
    M = MValor([t,P])
    E = Bisseccao(EValor,-1,2*np.pi,0.000000001,[M,e])
    angulo = AnguloValor([E,e])
    r = DistValor([angulo,e,a])
    x = (r*np.cos(angulo)+xc+f)
    y= (r*np.sin(angulo))
    return [x,y]

def FuncaoDaElipse(x):
    arq= open("../dados/ParametrosABC.bin","r")
    param = [0]*3
    i=0
    for line in arq:
        param[i] = float(line)
        i+=1
    arq.close()
    X=param[0]*x**2 + param[1]*x +param[2]
    if(X<=0):   return 0
    y = float(np.sqrt(X))
    return y

def AreaFeita(A,xTerra,Na=10):
    #reta 1 #reta 2
    A=np.asarray(A)

    base=0
    altura=0
    if(abs(A[0,0]-xTerra)>abs(A[1,0]-xTerra)):
        base1 = abs(A[0,0]-xTerra)
        altura1= A[0,1]
        base2= abs(A[1,0]-xTerra)
        altura2= A[1,1]
    else:
        base1 = abs(A[1,0]-xTerra)
        altura1= A[1,1]
        base2= abs(A[0,0]-xTerra)
        altura2= A[0,1]
    triangulo1= base1*altura1/2
    triangulo2 = base2*altura2/2
    #integral da elipse
    curva0 = newtonCotes(FuncaoDaElipse,A[1,0],A[0,0],5)
    arrayX = np.linspace(A[1,0],A[0,0],Na)
    arrayY=[0]*len(arrayX)
    for i in range(len(arrayX)):
        arrayY[i]=FuncaoDaElipse(arrayX[i])
    curva1= newtonCotes_Spline([arrayX,arrayY,[]],A[1,0],A[0,0],5)
    return [curva0+triangulo2-triangulo1,curva1+triangulo2-triangulo1]

# Lendo parametro de orbita
arq= open("../dados/Parametros.bin","r")
param = [0]*3
i=0
for line in arq:
    param[i] = float(line)
    i+=1
arq.close()
#Calculando o tempo de orbita
P= 2* np.pi*np.sqrt(param[1]**3/((6.67384*10**-11)*(5.972*10**24)))
k = 10 #random.randrange(5,100 )
tArray = np.linspace( 0,P/2, k )
t0= 1#random.randrange(1, k-1)
t1= 5#random.randrange(1,k-1)
#while(t1==t0):  t1= random.randrange(0,k)

A1= [pontoElipse(tArray[t0],param[0],param[1],param[2]),pontoElipse(tArray[t0+1],param[0],param[1],param[2])]
A2= [pontoElipse(tArray[t1],param[0],param[1],param[2]),pontoElipse(tArray[t1+1],param[0],param[1],param[2])]
xTerra = param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2)))
x01=A1[0][0]
y01=A1[0][1]
x11=A1[1][0]
y11=A1[1][1]
[xM1,yM1]= pontoElipse((tArray[t0]+tArray[t0+1])/2.0,param[0],param[1],param[2])
x02=A2[0][0]
y02=A2[0][1]
x12=A2[1][0]
y12=A2[1][1]
[xM2,yM2]= pontoElipse((tArray[t1]+tArray[t1+1])/2.0,param[0],param[1],param[2])

# print(A1)
# print(A2)
A1 = (AreaFeita(A1,xTerra,100))
A2 = (AreaFeita(A2,xTerra,100))


arq = open("../dados/Area.bin","w")
arq.write(str(A1[0])+"  "+str(A2[0])+"\n"+str(A1[1])+"  "+str(A2[1]))
arq.close()



print("Utilizando a função (6) y^2 = A*x^2 + B*x + C para calcular áreas feita pela orbita em um mesmo intervalo de tempo temos:\nA1 =", A1[0],"\nA2 =", A2[0])
print("Uma diferença de", abs(A1[0]-A2[0])," o que equivale a", str(abs(A1[0]-A2[0])/((A1[0]+A2[0])/2))+"% da média dessas áreas")


print("Utilizando o algoritmo spline com base em pontos conhecidos da orbita calculou-se a área feita pela mesma em um mesmo intervalo de tempo temos:\nA1 =", A1[1],"\nA2 =", A2[1])
print("Uma diferença de", abs(A1[1]-A2[1])," o que equivale a", str((abs(A1[1]-A2[1])/((A1[1]+A2[1])/2)))+"% da média dessas áreas")

print("Por fim temos que a diferença média dos métodos para calcular área é", ((abs(A1[0]-A1[1])+abs(A2[0]-A2[1]))/2))

#Desenhando a orbita
k = 10000
tArray = np.linspace( 0,P, k )
x=[0]*k
y=[0]*k
for i in range(k):
    aux = pontoElipse(tArray[i],param[0],param[1],param[2])
    x[i]=aux[0]
    y[i]=aux[1]


#plotando Elipse
plt.title("Segunda Lei de Kepler")

#Estilizando eixos
plt.axvline(x=0,color="grey",linestyle="-")
plt.axhline(y=0,color="grey",linestyle="-")
plt.xlabel("Eixo X (Em Km)")
plt.ylabel("Eixo Y (Em Km)")

#plotando a elipse
plt.plot(    x, y, "k-", label="Orbita")
#plotando a Terra
plt.plot(  param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))), 0, "go")
plt.annotate("Terra",(param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))), 0),(param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))-4.5e3), -2.8e2))
#plotando centro da elipse
plt.plot(  param[0], 0, "bo")
plt.annotate("Centro",(param[0], 0),(param[0]-5e3, 1.8e2))

#plotando pontos A1 e retas
plt.plot(  x01, y01, "ro")
plt.plot(  x11, y11, "ro")
plt.plot([param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x01],[0,y01],"r-")
plt.plot([param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x11],[0,y11],"r-")
plt.fill([param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x01,xM1,x11],[0,y01,yM1,y11],color="lightcoral",label="Area 1")

#plotando pontos A2 e retas
plt.plot(  x02, y02, "ko")
plt.plot(  x12, y12, "ko")
plt.plot([param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x02],[0,y02],"k-")
plt.plot([param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x12],[0,y12],"k-")
plt.fill([param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x02,xM2,x12],[0,y02,yM2,y12],color="dimgray",label="Area 2")

# plt.fill_between([y01,y11],[param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x01],[param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))),x11])
#plotando foco 1
plt.plot(  param[0]-(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))), 0, "bo")
plt.annotate("Foco",(param[0]-(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))), 0),(param[0]-(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))+4e3), 1.8e2))
#definindo escala
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

#plotando imagem final
plt.margins(0.1)
plt.grid(color="lightgray", linestyle="--")
plt.legend(loc='upper right')
plt.savefig("../dados/SegundaLeideKepler.jpg") 
    