from gaussiana import EGaussiana
import numpy as np
import math

# Arrays Com Dados Fornecidos para x e y
x= [20621.3,34642.3,21168.5]
y= [5214.2009061,3201.7095080,5193.6201775]
#Fazendo matriz Aumentada
matriz= []
for i in range(3):
    aux = [x[i]**2,x[i],1,y[i]**2]
    matriz.append(aux)
#Usando Elimnação Gaussiana para A,B,C e então para conseguir xc,a,b
A,B,C = EGaussiana(np.asarray(matriz))
arq = open("../dados/ParametrosABC.bin","w")
arq.write(str(A)+"\n"+str(B)+"\n"+str(C)+"\n")
arq.close()
param = [0]*3
param[0]= -(B/(2*A))
param[1]= math.sqrt(param[0]**2-(C/A))
param[2]=param[1]* math.sqrt(-A)
#Armazenando xc,a,b em um arquivo
arq = open("../dados/Parametros.bin","w")
arq.write(str(param[0])+"\n"+str(param[1])+"\n"+str(param[2])+"\n")
arq.close()
