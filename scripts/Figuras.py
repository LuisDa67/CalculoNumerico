import numpy as np
from bisseccao import Bisseccao
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

def PontosElipse(Na,xc,a,b):
    '''
        função para calcular Na pontos equidistantes em tempo de uma orbita elítica
            recebe:
            Na-> numeros de pontos a ser calculado
            xc,a,b -> parametro de orbita
    '''
    P= 2* np.pi*np.sqrt(a**3/((6.67384*10**-11)*(5.972*10**24)))
    e= np.sqrt(1-(b**2/a**2))
    f=a*e
    tArray = np.linspace( 0, P, Na )
    x = []
    y= []
    for t in tArray:
        M = MValor([t,P])
        E = Bisseccao(EValor,-1,2*np.pi,0.000000001,[M,e])
        angulo = AnguloValor([E,e])
        r = DistValor([angulo,e,a])
        x.append(r*np.cos(angulo)+xc+f)
        y.append(r*np.sin(angulo))
    return x,y


# Lendo parametro de orbita
arq= open("../dados/Parametros.bin","r")
param = [0]*3
i=0
for line in arq:
    param[i] = float(line)
    i+=1
# xc = param[0]
# a = param[1]
# b = param[2]


#descobrindo pontos da elipse
x,y =PontosElipse(100000,param[0],param[1],param[2])

#plotando Movimento orbital
plt.title("Movimento Orbital")

#Estilizando eixos
plt.axvline(x=0,color="grey",linestyle="-")
plt.axhline(y=0,color="grey",linestyle="-")
plt.xlabel("Eixo X (Em Km)")
plt.ylabel("Eixo Y (Em Km)")

#plotando a elipse
plt.plot(    x, y, "k-", label="Orbita percorrida")
#plotando a Terra
plt.plot(  param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))), 0, "go")
plt.annotate("Terra",(param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))), 0),(param[0]+(param[1]*np.sqrt(1-(param[2]**2/param[1]**2))-5e3), 1.8e2))
#plotando centro da elipse
plt.plot(  param[0], 0, "bo")
plt.annotate("Centro",(param[0], 0),(param[0]-5e3, 1.8e2))
#plotando a
plt.plot([param[0],param[0]+param[1]],[0,0],"m-")
plt.annotate("a",(param[0],0),(param[0]+param[1]/2, 1.8e2))
#plotando b
plt.plot([param[0],param[0]],[0,param[2]],"m-")
plt.annotate("b",(param[0],0),(param[0]-1.5e3, param[2]/2))
#plotando xc
plt.plot([0,param[0]],[0,0],"m-")
plt.annotate("xc",(param[0],0),(param[0]/2, 1.8e2))

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
plt.savefig("../dados/MovimentoOrbital.jpg") 
    

#plotando a elipse
x1,y1= PontosElipse(30,param[0],param[1],param[2])
#plotando pontos equidistantes
plt.clf()
plt.title("Pontos Equidistantes")

#Estilizando eixos
plt.axvline(x=0,color="grey",linestyle="-")
plt.axhline(y=0,color="grey",linestyle="-")
plt.xlabel("Eixo X (Em Km)")
plt.ylabel("Eixo Y (Em Km)")

#plotando pontos e trajetoria
plt.plot(x1,y1,"ro",label="Pontos Equidistantes")
plt.plot(    x, y, "k-", label="Orbita percorrida")
#definindo escala
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#plotando imagem final
plt.margins(0.1)
plt.grid(color="lightgray", linestyle="--")
plt.legend(loc='upper right')
plt.savefig("../dados/PontosEquidistantes.jpg") 
    
    
    

