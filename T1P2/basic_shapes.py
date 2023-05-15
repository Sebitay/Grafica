import numpy as np
from OpenGL.GL import *
import constants

SIZE_IN_BYTES = constants.SIZE_IN_BYTES

# La clase shape guarda los vertices y los indices aparte
class Shape:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData



    
#crear cubo con GL_LINES, la única diferencia con los cubos FILL son los indices que se unen de a pares
def createCube():
    
    vertexData = np.array([
        # positions        # colors
         0.5,  0.5,  0.5,  0.0, 0.0, 1.0, #0
        -0.5,  0.5,  0.5,  1.0, 1.0, 1.0, #1
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0, #2
         0.5, -0.5,  0.5,  0.0, 1.0, 0.0, #3
         0.5,  0.5, -0.5,  1.0, 0.0, 1.0, #4
        -0.5,  0.5, -0.5,  1.0, 1.0, 1.0, #5
        -0.5, -0.5, -0.5,  1.0, 0.0, 0.0, #6
         0.5, -0.5, -0.5,  0.0, 1.0, 0.0  #7
    ], dtype=np.float32) 

    indexData = np.array([
        0,1,
        1,2,
        2,3,
        3,0,
        4,5,
        5,6,
        6,7,
        7,4,
        0,4,
        1,5,
        2,6,
        3,7




        ],dtype=np.uint32)

    return Shape(vertexData, indexData)




from numpy import pi
from numpy import sqrt
from numpy import cos
from numpy import sin

def x(r,teta,phi):
    return r*sin(teta)*cos(phi)

def y(r,teta,phi):
    return r*sin(teta)*sin(phi)

def z(r,teta):
    return r*cos(teta)

from random import randint

def Esfera(radio,n,R,G,B):
    cantidad_colores = len(R)
    paso = n/cantidad_colores
    vertices = [0,0,radio,R[0],G[0],B[0]] #el que está en la punta superior, vertice 0
    for i in range(0,n): #que teta vaya desde 1*pi/n hasta (n-1)pi)/n
        teta = i*pi/n 
        r,g,b = [R[int(i/paso)],G[int(i/paso)],B[int(i/paso)]] #hace el cajón inferior para que se hagan las bandas correctamente
        for j in range(1,2*n+1):      #phi va desde 0 hasta 2pi(n-1)/n, haciendo saltos de pi/n
            phi = j*pi/n
            vertices = vertices +  [x(radio,teta,phi),y(radio,teta,phi),z(radio,teta),r,g,b] #se añaden los puntos con colores randoms
    vertices += [0,0,-radio,R[-1],G[-1],B[-1]] #se añade el polo sur, el punto de más de abajo
    vertexData = np.array(vertices,dtype=np.float32)
    indices = []

    #hacer los indices del polo norte
    for i in range(1,2*n):
        indices = indices + [0,i,i+1] #se arman los triangulos
    indices += [0,2*n,1] #se añade el final de manera no automatica, ya que no se puede en el for 
    
    
    # La parte del medio
    for i in range(0,n-2): # hay n-2 bandas en total
       for k in range(1,2*n): # se mueve en los anillos, con 2n cambios
           indices += [k + (2*n)*i, 2*n + k + (2*n)*i , 2*n + (k+1) + (2*n)*i] #indices de los trinagulos 1
           indices += [k + (2*n)*i , k+1 + (2*n)*i , 2*n + (k+1) + (2*n)*i] #indices de los triangulos tipo 2
       indices += [2*n + (2*n)*i , 4*n + (2*n)*i ,2*n + 1 + (2*n)*i] #los casos finales de esos triangulos 1
       indices += [2*n + (2*n)*i, 1 + (2*n)*i , 2*n +1 + (2*n)*i] #casos finales triangulos 2

    
    #ahora veamos el polo sur papito 

    #el indice de más de abajo es el total de puntos que hay menos 1, y el total tenemos (n-1)*(2n)+2, ya que son n-1 anillos
    #por los cuales hay 2n (los phi) por cada anillo, pero aparte están el punto (0,0,r) y (0,0,-r), así que por eso el +2

    f = ((n-1)*2*n + 2)- 1 #indice final
    #print(f+1)
    for k in range(0,2*n-1): #k va desde 0 hasta 2n-2
        indices += [f , f - 2*n + k , f - 2*n + (k+1)] # se añaden los triangulos anclados al vertice de más al sur
    indices += [f,f-1,f-2*n] #se añade el final

    IndexData = np.array(indices,dtype=np.uint32)

    return Shape(vertexData,IndexData)


def crearcuboColor(C,n,m,R,G,B): #funció para cambiar los colores
    for N in range(8): #mientras nos movamos en los 8 vértices
        C[N][0] = R[N] - (R[N] - R[N-1])*m/n #el rojo del n vertice se cambia gradualmente 
        C[N][1] = G[N] - (G[N] - G[N-1])*m/n
        C[N][2] = B[N] - (B[N] - B[N-1])*m/n


    vertexData = np.array([
        # positions        # colors
        0.5,  0.5,  0.5,  C[0,0],C[0,1],C[0,0],  #0
        -0.5,  0.5,  0.5, C[1,0],C[1,1],C[1,2],  #1
        -0.5, -0.5,  0.5, C[2,0],C[2,1],C[2,2],  #2
        0.5, -0.5,  0.5,  C[3,0],C[3,1],C[3,2],  #3
        0.5,  0.5, -0.5,  C[4,0],C[4,1],C[4,2],  #4
        -0.5,  0.5, -0.5, C[5,0],C[5,1],C[5,2],  #5
        -0.5, -0.5, -0.5, C[6,0],C[6,1],C[6,2],  #6
        0.5, -0.5, -0.5,  C[7,0],C[7,1],C[7,2]   #7
    ], dtype=np.float32) 


    indexData = np.array([
        0,1,
        1,2,
        2,3,
        3,0,
        4,5,
        5,6,
        6,7,
        7,4,
        0,4,
        1,5,
        2,6,
        3,7
        ],dtype=np.uint32)

    return Shape(vertexData, indexData)

