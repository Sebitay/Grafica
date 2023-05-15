# Bastián Corrales

import glfw  
from OpenGL.GL import *  #se importan todas las funciones de OpenGL
from gpu_shape import GPUShape #GPU Shape es para dibujar las figuras
from easy_shaders import SimpleModelViewProjectionShaderProgram  #Función que permite visualizar CUERPOS 
from basic_shapes import * #importa el objeto cubo, que posee los vertices y como unirlos
import numpy as np
import transformations as tr   #matrices de transformaciones
import constants  # las constantes de las dimensiones de las ventanas

def main():
    
    if not glfw.init():  #si no está inicalizada la ventana
        glfw.set_window_should_close(window, True)  #entonces se cierra
        return -1

    width = constants.SCREEN_WIDTH #se extraen las dimensiones de la ventana desde constants.py
    height = constants.SCREEN_HEIGHT

    window = glfw.create_window(width, height, "Cuadrado?", None, None) #se crea el objeto ventana

    if not window:  #si no hay objeto ventana, entonces termina el proceso
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)
 
    #La clase controller sirve para cambiar parametros cuando se apreten diversas teclas, con la cámara, con el portal y las rotaciones
    class Controller:
       def __init__(self):
           self.angulo = 0  #angulo que se irá moviendo para la cámara pedida en el enunciado
           self.anguloZ = np.arcsin(0.3/4)  #angulo que parte en esto para que 4*sin(arcsin(0.3/4))=0.3, como se pide 
           self.portal = 0 #valor que cuando es 0, se cancela el efecto del portal y cuando es 1 se activa
           self.rotacionX = 0 #valor que cuando es 0 se cancela el efecto de la rotacion c/r al eje X y cuando es 1 se activa
           self.rotacionY = 0 #valor que cuando es 0 se cancela el efecto de la rotacion c/r al eje Y y cuando es 1 se activa
           self.rotacionZ = 0 #valor que cuando es 0 se cancela el efecto de la rotacion c/r al eje Z y cuando es 1 se activa
           self.anguloup = (np.pi/2 - np.arcsin(0.3/4))/5  #angulo para la flecha de arriba (por eso up), y es eso para que en 5 saltos se llegue a pi/2
           self.angulodown = (-np.pi/2 - np.arcsin(0.3/4))/5 #angulo para la flecha de abajo(down), y es eso para que en 5 saltos se llegue a -pi/2

       def cambiar_rotacionZ(self): #si la rotacion era 0, entonces se vuelve 1 y viceversa
           if self.rotacionZ==0:
               self.rotacionZ=1
           else:
                self.rotacionZ=0

       def cambiar_rotacionX(self):
           if self.rotacionX==0:
               self.rotacionX=1
           else:
                self.rotacionX=0
       
       def cambiar_rotacionY(self):
           if self.rotacionY==0:
               self.rotacionY=1
           else:
                self.rotacionY=0
       
       def cambiar_portal(self): #si el portal es 0 entonces se cambia a 1 y viceversa
           if self.portal == 0:
                self.portal = 1
           else:
               self.portal=0

       def rotate(self, alpha): #aumenta el angulo en alpha
           self.angulo+= alpha
           return

       def rotateZ(self,alpha): #aumenta el angulo en Z con el alpha
           self.anguloZ += alpha                                                                                                                                                                   
           return

    controller = Controller()

    def on_key(window, key, scancode, action, mods):

        if action == glfw.PRESS:
            if key==glfw.KEY_Z: #si se apreta la tecla es Z
                controller.cambiar_rotacionZ() #entonces se cambia el valor de rotacionZ, lo mismo con todo lo demás
            if key==glfw.KEY_Y:
                controller.cambiar_rotacionY()
            if key==glfw.KEY_X:
                controller.cambiar_rotacionX()
            if key==glfw.KEY_P:
                controller.cambiar_portal()
            if key == glfw.KEY_RIGHT:
                controller.rotate(2*np.pi/15)  #se aumenta el angulo en 2pi/15
            if key == glfw.KEY_LEFT:
                controller.rotate(-2*np.pi/15)
            if key == glfw.KEY_UP:
                controller.rotateZ(controller.anguloup)
            if key == glfw.KEY_DOWN:
                controller.rotateZ(controller.angulodown)
            
            

    glfw.set_key_callback(window, on_key)  #se le dice a la ventana que haga caso al onkey

    pipeline = SimpleModelViewProjectionShaderProgram() #función que permite dibujar CUERPOS
    glUseProgram(pipeline.shaderProgram) 

    L = 0.1 #radio de las esferas

    #se ponen los vertices y los indices para poder dibujar

   

    projection = tr.perspective(20, float(width)/float(height), 0.1, 100) #la perspectiva, donde el fov dice que tanta perspectiva tienes

    glClearColor(0, 0, 0, 1.0) #se dan los colores del fondo 

    glEnable(GL_DEPTH_TEST)

    theta = 0

    class esferita:
        def __init__(self,posX,posY,posZ,velX,velY,velZ): #se definen las posiciones y las velocidades iniciales
            self.posX = posX
            self.posY = posY
            self.posZ = posZ
            self.velX = velX
            self.velY = velY
            self.velZ = velZ
        
        def aumentarX(self,t): #aumentan las posiciones en x,y,z con el dt
            self.posX = self.posX + self.velX*t
        def aumentarY(self,t):
            self.posY = self.posY + self.velY*t
        

        def gravedad(self,g,t):
            self.velZ = self.velZ -g*t #la velocidad en z se va bajando con g
        
        def cambiarZ(self,t):
            self.posZ = self.posZ + self.velZ*t

    #importando las funciones matemáticas
    from numpy import sqrt
    from numpy import cos
    from numpy import sin

    #aqui se van a poner todos los datos iniciales y funciones auxilares que ayudarán dentro del while


    complejidad_esfera = 15
    t0 = glfw.get_time() #se inicaliza el tiempo
    z = 0.3 # posicion incial del z
    Vx1 = 0.2 #velocidad inicial de x
    Vy1 = sqrt( 0.4**2 - Vx1**2) #con la fórmula se calcula la otra
    Vx2 = 0.1
    Vy2 = sqrt( 0.4**2 - Vx2**2)
    g = 9.8 #gravedad en la tierra
    esfera1 = esferita(0,0,z,Vx1,Vy1,0)  
    esfera2 = esferita(-0.3,0.3,z,Vx2,Vy2,0)

    def distancia(x1,x2,y1,y2): #función distancia entre dos punotos
        return sqrt((x1-x2)**2 + (y1-y2)**2)

    C = np.array([         #colores iniciales de los vertices del cubo grande 
        [0.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
        ])

    
    colors = C.transpose() #se transpone la matriz
    R = list(colors[0]) #para luego obtener la primera columna
    G = list(colors[1])
    B = list(colors[2])
    m=0 # m va desde 0 hasta n, saltando de uno en uno, sirve para ir cambiando los colores poco a poco del cubo
    n=20 #son 100 pasos 
    rotacion = 0 #la rotación c/r a su propio centro en Z
    rotacionX=0 #rotacion c/r al eje x cuando el centro de la esfera NO está en el centro del sistema
    rotacionY=0 #rotacion c/r al eje y cuando el centro de la esfera NO está en el centro del sistema
    rotacionZ=0 #rotacion c/r al eje z cuando el centro de la esfera NO está en el centro del sistema
    direccion_rotacion = 1 #la dirección de rotación es 1 y -1 cuando chocan las esferas entre ellas
    R_esfera = [] #listas que van a poseer los colores de los puntos de la esferas, R_esfera posee todos los rojos y así
    G_esfera = []
    B_esfera = []

    #las rellenamos de manera random
    for i in range(0,50):
        R_esfera += [randint(0,255)/255] #las rellenamos de manera random
        G_esfera += [randint(0,255)/255]
        B_esfera += [randint(0,255)/255]



    #ahora viene le while de la ventana, todo va a cambiar constantemente dentro de este while, en especifico este while se ejecutará
    #siempre y cuando la ventana esté abierta
        
    while not glfw.window_should_close(window): # mientras NO se cierre la ventana

        t1 = glfw.get_time() #tiempo 1                  
        dt = t1 - t0 #la diferencia de tiempos, que sirve para multiplicar en la suma de los pasos de tiempo para ajustar los fps del monitor
        t0 = t1
      
        c1 = crearcuboColor(C,n,m,R,G,B)  #se crea el cubo con la matriz C de los colores originales
        gpuC1 = GPUShape().initBuffers() #
        pipeline.setupVAO(gpuC1)
        gpuC1.fillBuffers(c1.vertexData, c1.indexData) #se ponen los vertices y los indices para poder dibujar

        c2 = Esfera(L,complejidad_esfera,R_esfera,G_esfera,B_esfera) #se crea la esfera
        gpuC2 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC2)
        gpuC2.fillBuffers(c2.vertexData, c2.indexData) 

        c3 = Esfera(L,complejidad_esfera,R_esfera,G_esfera,B_esfera )  #se crea la esfera
        gpuC3 = GPUShape().initBuffers() #
        pipeline.setupVAO(gpuC3)
        gpuC3.fillBuffers(c3.vertexData, c3.indexData) #se ponen los vertices y los indices para poder dibujar
        

        m+=1 #los vertices cambián un poquito

        if m==n: # si llegamos al final, entonces reiniciamos
            m=0
            R = [R[-1]] + list(R[0:-1]) # Se pone el último verice primero y luego todos los demás, para cambiarlos de posición
            G = [G[-1]] + list(G[0:-1])
            B = [B[-1]] + list(B[0:-1])


        view = tr.lookAt(
            np.array([4*cos(controller.angulo)*cos(controller.anguloZ),4*sin(controller.angulo),4*sin(controller.anguloZ)]), #posición del ojo, que depende de los ángulos cuando se rota en plano XY o ZX
            np.array([0,0,0]),   #la posición a la que se está mirando, que es el centro del cubo, que también es el origen
            np.array([-1*sin(controller.anguloZ),0,1*cos(controller.anguloZ)])#el up va cambiando cuando se rota en plano ZX
                            )
    
        #si la distancia entre los centros de la esfera es 2 veces el radio, el diametro
        if distancia(esfera1.posX,esfera2.posX,esfera1.posY,esfera2.posY)<=2*L:
            if controller.portal==0: #si no hay opción de portal, entonces chocan las esferas, si no no chocan
                esfera1.velX,esfera2.velX = esfera2.velX,esfera1.velX
                esfera1.velY,esfera2.velY = esfera2.velY,esfera1.velY
                if direccion_rotacion ==1: #cuando chocan cambian el sentido de rotación
                    direccion_rotacion=-1
                else:
                    direccion_rotacion=1
        

        if (esfera1.posZ-L)<(-0.5): #si se llega a la parte de abajo
                esfera1.velZ = sqrt(2*(z+0.5)*g) #la velocidad se reinicia, con la formula itineraria

        if (esfera1.posZ+L)>(0.5): #si se llega a arriba, se pone en 0
            esfera1.velZ = 0
        
        if (esfera1.posX-L)<(-0.5) or (esfera1.posX+L)>(0.5): #si se choca en alguna pared en X, rebota
                if controller.portal==0:
                    esfera1.velX = -esfera1.velX
                else:
                    if esfera1.posX>0: #si choca con la pared de adelante
                        esfera1.posX = -0.5+L #aparece por atrás magicamente
                    else:
                        esfera1.velX = -esfera1.velX #de lo contrario choca normalmente
         
        
        if (esfera1.posY-L)<(-0.5) or (esfera1.posY+L)>(0.5): #si chocan en las paredes Y
            if controller.portal==0:
                esfera1.velY = -esfera1.velY #chocan 
            else:
                if esfera1.posY<0: #si choca con la pared de la izquierda
                    esfera1.posY = 0.5 - L #aparece en la derecha
                else:
                    esfera1.velY = -esfera1.velY 


        
        esfera1.aumentarX(dt) #se aumentan todas las posiciones y la gravedad
        esfera1.aumentarY(dt)
        esfera1.gravedad(g,dt)
        esfera1.cambiarZ(dt)

        if (esfera2.posZ-L)<(-0.5): 
                esfera2.velZ = sqrt(2*(z+0.5)*g)

                
        
        if (esfera2.posZ+L)>(0.5):
            esfera2.velZ = 0
        
        if (esfera2.posX-L)<(-0.5) or (esfera2.posX+L)>(0.5):
             if controller.portal==0:
                esfera2.velX = -esfera2.velX
             else:
                if esfera1.posX<0:
                    esfera1.posX = 0.5-L
                else:
                    esfera2.velX = -esfera2.velX



        if (esfera2.posY-L)<(-0.5) or (esfera2.posY+L)>(0.5):
            if controller.portal==0:
                esfera2.velY = -esfera2.velY
            else:
                if esfera2.posY>0:
                    esfera2.posY = -0.5 + L
                else:
                    esfera2.velY = -esfera2.velY

        #se aumentan todas las posicones de la 2 esfera
        esfera2.aumentarX(dt)
        esfera2.aumentarY(dt)
        esfera2.gravedad(g,dt)
        esfera2.cambiarZ(dt)

        glfw.poll_events() 
 
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) #se pintan las lineas del poligono, llenandolas con FILL en general

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, 0.0, 0.0) #no se translada hacia ningun lado el cubo
        ]))
        
        pipeline.drawCall(gpuC1,GL_LINES) #se dibuja

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.rotationZ(rotacionZ), #se hacen todas las rotaciones y se translada
            tr.rotationY(rotacionY),
            tr.rotationX(rotacionX),
            tr.translate(esfera1.posX, esfera1.posY, esfera1.posZ),  
            tr.rotationY(rotacion*direccion_rotacion),    #se rota c/r a su propio eje en Y, por esto hace ese giro hacia "adelante" o "atrás"
        ]))

        pipeline.drawCall(gpuC2) #se dibujan

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.rotationZ(rotacionZ),
            tr.rotationY(rotacionY),
            tr.rotationX(rotacionX),
            tr.translate(esfera2.posX, esfera2.posY, esfera2.posZ),          
            tr.rotationY(rotacion*direccion_rotacion)
        ]))

        pipeline.drawCall(gpuC3)

        rotacion +=np.pi/15 #se aumenta la rotación hacia adelante o atrás
        
        if controller.rotacionX==1: #si se apreta x entones de rota en X o deja de hacerlo
            rotacionX+=np.pi/400
        else:
            rotacionX=0

        if controller.rotacionY==1:
            rotacionY+=np.pi/400
        else:
            rotacionY=0

        if controller.rotacionZ==1:
            rotacionZ+=np.pi/400
        else:
            rotacionZ=0

        glfw.swap_buffers(window) #se crea el buffer

    gpuC1.clear() 

    glfw.terminate()

    return 0 #se retorna para poder terminar

main()

