# coding=utf-8
#Bastián Corrales
"""Textures and transformations in 3D"""
from msilib.schema import ControlEvent

#from pyrsistent import b
from libs.assets_path import getAssetPath
import libs.performance_monitor as pm
import libs.scene_graph as sg
import libs.easy_shaders as es
import libs.basic_shapes as bs
import libs.transformations as tr
import glfw
from OpenGL.GL import *
from libs.setup import setPlot, setView, createMinecraftBlock, CuadradoAutopista,Base_casa,cubo,MitadAutopista
import numpy as np
import sys
import os.path
import numpy as np
import random 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__author__ = "Gonzalo Alarcon"
__license__ = "MIT"




# La clase controller que tendrá todos los parametros necesarios
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.eye = np.array([5,10,-3],dtype=np.float32) #posición del ojo(observador)
        self.at = np.array([8,0.5,-5],dtype=np.float32)  #posición del objeto al que estoy mirando
        self.up = np.array([0,1,0],dtype=np.float32)  #vector que dice donde está el arriba
        self.front = self.at - self.eye
        self.right = np.cross(self.front,self.up) #vector que apunta desde el ojo hacia el punto(dirección hacia donde miro)
        self.avance = 0.008 #que tanto avanzo cuando voy hacia adelante o a atrás
        self.vuelo = 0.13  #que tanto se va hacia arriba o hacia abajo
        self.camera= np.pi/700 #que tan rapido es el movimiento de cámara
        self.axesOn = True   #si se muestran los ejes o no
    
    #se hace a mano ya que en los movimientos de cámara y laterales, no funciona bien si no se actualiza
    def actualizarRight(self): 
        self.right = np.cross(self.front,self.up)

#se llama a controller
controller = Controller()


#se define on_key para os casos discretos, es decir cuando solo se aprieta una sola vez, que sería
#sacar los ejes y cerrar la ventana
def on_key(window, key, scancode, action, mods):

    
    if action == glfw.PRESS: #si la acción es presionar
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True) #se cierra
        if key==glfw.KEY_Q:
            if controller.axesOn==False:  #se cambia el axesON 
                controller.axesOn = True
            else:
                controller.axesOn = False

def createScene(pipeline):
    """
    Esta funcion crea la escena
    """
    # Creamos TODOS objetos particuales, que son todas las partes de las casas y de las carreteras

    shapeCasa = Base_casa()
    gpuCasa = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCasa)
    gpuCasa.fillBuffers(
        shapeCasa.vertices, shapeCasa.indices, GL_STATIC_DRAW)
    gpuCasa.texture = es.textureSimpleSetup(
        getAssetPath("casa.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) #bloque casa grande
    
    shapePuerta = cubo()
    gpuPuerta = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPuerta)
    gpuPuerta.fillBuffers(
        shapePuerta.vertices, shapePuerta.indices, GL_STATIC_DRAW)
    gpuPuerta.texture = es.textureSimpleSetup(
        getAssetPath("texture_door.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) #textura puerta casa normal

    shapeVentana = cubo()
    gpuVentana = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuVentana)
    gpuVentana.fillBuffers(
        shapeVentana.vertices, shapeVentana.indices, GL_STATIC_DRAW)
    gpuVentana.texture = es.textureSimpleSetup(
        getAssetPath("ventana.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) #texutra ventana casa normal
    
    shapeCubo = cubo()
    gpuCubo = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubo)
    gpuCubo.fillBuffers(
        shapeCubo.vertices, shapeCubo.indices, GL_STATIC_DRAW)
    gpuCubo.texture = es.textureSimpleSetup(
        getAssetPath("bloque_minecraft.PNG"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) #textura bloque minecraft
        
    shapeWindow = cubo()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(
        shapeWindow.vertices, shapeWindow.indices, GL_STATIC_DRAW)
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath("window.PNG"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) #bloque ventana minecraft

    shapeDoor = cubo()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(
        shapeDoor.vertices, shapeDoor.indices, GL_STATIC_DRAW)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("door.PNG"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)#bloque puerta minecraft
    
    shapeStair = cubo()
    gpuStair = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuStair)
    gpuStair.fillBuffers(
        shapeStair.vertices, shapeStair.indices, GL_STATIC_DRAW)
    gpuStair.texture = es.textureSimpleSetup(
        getAssetPath("amatista.PNG"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)#bloque del techo de minecrat

    
    shapeRoof = CuadradoAutopista()
    gpuRoof = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRoof)
    gpuRoof.fillBuffers(
        shapeRoof.vertices, shapeRoof.indices, GL_STATIC_DRAW)
    gpuRoof.texture = es.textureSimpleSetup(
        getAssetPath("roof2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)#plano para el techo casa normal
    shapeAutopista = CuadradoAutopista()

    gpuAutopista = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuAutopista)
    gpuAutopista.fillBuffers(
        shapeAutopista.vertices, shapeAutopista.indices, GL_STATIC_DRAW)
    gpuAutopista.texture = es.textureSimpleSetup(
        getAssetPath("autopista.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)#plano para autopista
    
    shapePasto = CuadradoAutopista()
    gpuPasto = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPasto)
    gpuPasto.fillBuffers(
        shapePasto.vertices, shapePasto.indices, GL_STATIC_DRAW)
    gpuPasto.texture = es.textureSimpleSetup(
        getAssetPath("pasto4.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) #plano para el pasto
    
    shapeMitad = MitadAutopista()
    gpuMitad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuMitad)                                                     
    gpuMitad.fillBuffers(
        shapeMitad.vertices, shapeMitad.indices, GL_STATIC_DRAW)
    gpuMitad.texture = es.textureSimpleSetup(
        getAssetPath("pasto4.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)#triangulo para el pasto

    

    
    # Definimos el nodo escena
    scene = sg.SceneGraphNode('system')

    # Definimos el nodo que tendra todas las cosas
    floor = sg.SceneGraphNode('floor')

    #frontal casa minecraft
    frontal = sg.SceneGraphNode('frontal')

    #base casa minecraft

    casa_minecraft = sg.SceneGraphNode('casa_minecraft')
    #intento de la casa de minecraft
    bloque = sg.SceneGraphNode('cubo')
    bloque.transform = tr.matmul([tr.uniformScale(0.1)]) #se hacen chicos para poder recrear minecraft
    bloque.childs += [gpuCubo]

    #ventanas
    window = sg.SceneGraphNode('window')
    window.transform = tr.matmul([tr.uniformScale(0.1)])
    window.childs += [gpuWindow]

    #primera parte de abajo de la cara de la casa
    linea = sg.SceneGraphNode('bloques')
    for i in [0,1,2,3,6,7,8,9]:
        for j in [1,2,3]:
            block = sg.SceneGraphNode(f'block {i,j}')
            block.transform = tr.matmul([tr.translate(i*0.1,j*0.1,0)])
            block.childs += [bloque]
            linea.childs += [block]
    
    frontal.childs += [linea]

    #partes verticales
    vertical = sg.SceneGraphNode('vertical')
    for i in [0,1]:
        for j in range(1,5):
            block = sg.SceneGraphNode(f'block {i,j}')
            block.transform = tr.matmul([tr.translate(i*0.1,j*0.1,0),tr.translate(0,0.3,0)])
            block.childs += [bloque]
            vertical.childs += [block]
    
    frontal.childs += [vertical]

    vertical2 = sg.SceneGraphNode('vertical2')
    vertical2.transform = tr.matmul([tr.translate(0.4,0,0)])
    vertical2.childs += [vertical]

    frontal.childs += [vertical2]

    vertical3 = sg.SceneGraphNode('vertical2')
    vertical3.transform = tr.matmul([tr.translate(0.8,0,0)])
    vertical3.childs += [vertical]

    frontal.childs += [vertical3]

    #ahora los restos de la parte superior

    resto1 = sg.SceneGraphNode('resto1')
    for i in [0,1]:
        for j in [0,1]:
            block = sg.SceneGraphNode(f'block {i,j}')
            block.transform = tr.matmul([tr.translate(0.2 + 0.1*i, 0.6 +0.1*j,0)])
            block.childs += [bloque]
            resto1.childs += [block]
    
    frontal.childs += [resto1]

    resto2 = sg.SceneGraphNode('resto2')
    resto2.transform = tr.matmul([tr.translate(0.4,0,0)])
    resto2.childs += [resto1]

    frontal.childs += [resto2]

    #ventanas
    ventana1 = sg.SceneGraphNode('ventana1')
    for i in [0,1]:
        for j in [0,1]:
            block = sg.SceneGraphNode(f'block {i,j}')
            block.transform = tr.matmul([tr.translate(0.2 + 0.1*i, 0.4 +0.1*j,0)])
            block.childs += [window]
            ventana1.childs += [block]
    
    frontal.childs += [ventana1]

    ventana2 = sg.SceneGraphNode('resto2')
    ventana2.transform = tr.matmul([tr.translate(0.4,0,0)])
    ventana2.childs += [ventana1]
    frontal.childs += [ventana2]

    #puerta

    door = sg.SceneGraphNode('door')
    door.transform = tr.matmul([tr.translate(0.45,0.2,0),tr.scale(0.2,0.3,0.1)])
    door.childs += [gpuDoor]

    frontal.childs += [door]
    frontal.transform = tr.matmul([tr.translate(-0.45,0,0.45)])

    casa_minecraft.childs += [frontal]


    #ahora a hacer las paredes de los lados con la cara de un creeper

    cara_creeper = np.array([
    [1,1,1,1,1,1,1,1,1,1],  #para saber las posiciones sin tener que calcularlas a mano
    [1,1,0,0,1,1,0,0,1,1],
    [1,1,0,0,1,1,0,0,1,1],
    [1,1,1,1,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,1,1,1],
    [1,1,1,0,1,1,0,1,1,1]
    ])

    textured_blocks = []
    window_blocks = []

    for y in range(7):
        for x in range(10):
            if cara_creeper[y][x] == 1: #si estamos en 1 entonces son las textura de los bloques negros
                textured_blocks.append((x,y))
            else:
                window_blocks.append((x,y))


    lado_casa1 = sg.SceneGraphNode('lado_casa1')
    lado_casa1.transform = tr.matmul([tr.translate(-0.45,0,0.45)])
    for pos in textured_blocks:
        segmento_lado = sg.SceneGraphNode(f'textured_block {pos}')
        segmento_lado.transform = tr.matmul([tr.translate(0,0.7-pos[1]*0.1,-pos[0]*0.1)])
        segmento_lado.childs += [bloque]
        lado_casa1.childs.append(segmento_lado)

    for pos in window_blocks:
        segmento_lado = sg.SceneGraphNode(f'window_block {pos}')
        segmento_lado.transform = tr.matmul([tr.translate(0,0.7-pos[1]*0.1,-pos[0]*0.1)])
        segmento_lado.childs += [window]
        lado_casa1.childs.append(segmento_lado)

    casa_minecraft.childs += [lado_casa1]

    lado_casa2 = sg.SceneGraphNode('lado_casa2')
    lado_casa2.transform = tr.matmul([tr.rotationY(-np.pi/2)]) #simplemente se rota el otro lado
    lado_casa2.childs += [lado_casa1]

    casa_minecraft.childs += [lado_casa2]

    lado_casa3 = sg.SceneGraphNode('lado_casa2')
    lado_casa3.transform = tr.matmul([tr.rotationY(-np.pi/2)]) #se rota el otro lado
    lado_casa3.childs += [lado_casa2]

    casa_minecraft.childs += [lado_casa3]

    #empieza el techo
    bloque_escalera = sg.SceneGraphNode('bloque_escalera')
    bloque_escalera.transform = tr.matmul([tr.scale(2,1,1),tr.uniformScale(0.1)])
    bloque_escalera.childs += [gpuStair]

    base_escalera = sg.SceneGraphNode('base_escalera') #lo que se replicará hacia atrás ( en z)
    for i in range(0,4):
        stair = sg.SceneGraphNode(f'stair {i}')
        stair.transform = tr.matmul([tr.translate(0.1*i,0.1*i,0),tr.translate(-0.4,0.80,+0.55)])
        stair.childs += [bloque_escalera]
        base_escalera.childs += [stair]
    
    casa_minecraft.childs += [base_escalera]

    escalera1 = sg.SceneGraphNode('escalera1')
    for z in range(1,12):
        stair = sg.SceneGraphNode(f'escalera {z}')
        stair.transform = tr.matmul([tr.translate(0,0,-0.1*z)])
        stair.childs += [base_escalera]
        escalera1.childs += [stair]
    
    casa_minecraft.childs+=[escalera1]

    escalera2 = sg.SceneGraphNode('escalera2')
    escalera2.transform = tr.matmul([tr.rotationY(-np.pi)]) #se crea la otra parte de la escalera
    escalera2.childs += [escalera1]

    casa_minecraft.childs+=[escalera2]

    #parte del entre-techo

    entre_techo = sg.SceneGraphNode('Entre-techo')
    A = []
    for i in range(0,6):
        A+=[(-0.25+i*0.1,0.8,0.45)] #se crean las posiciones para no tener que hacerlas con muchos for separados

    B = []
    for j in range(0,4):
        B+=[(-0.15 +j*0.1,0.9,0.45)]
    
    C =[]
    for k in range(0,2):
        C+=[(-0.05 +k*0.1,1,0.45)]

    
    L=[]
    L=L+A+B+C
    
    for pos in L:
        segmento_lado = sg.SceneGraphNode(f'entre-techo {pos}')
        segmento_lado.transform = tr.matmul([tr.translate(pos[0],pos[1],pos[2])])
        segmento_lado.childs += [bloque]
        entre_techo.childs.append(segmento_lado)
    
    full_entretecho=sg.SceneGraphNode('entretecho full')#se le añade profundidad
    for z in range(0,10):
        parte = sg.SceneGraphNode(f'full entre-techo {z}')
        parte.transform = tr.matmul([tr.translate(0,0,-0.1*z)])
        parte.childs+=[entre_techo]
        full_entretecho.childs += [parte]
    
    casa_minecraft.childs+=[full_entretecho]


    
    #se agranda la casa y se rota, para que sea de las mismas dimensiones y dirección que la casa normal
    casa_minecraft.transform = tr.matmul([tr.rotationY(-np.pi/2),tr.scale(1,1,1.5),tr.translate(0,-0.1,0)])



    #floor.childs += [casa_minecraft]









    #nodo que tendrá la casa, con sus partes
    casa = sg.SceneGraphNode('casa')

    #base de la casa
    base_casa = sg.SceneGraphNode('base_casa')
    base_casa.transform = tr.matmul([tr.translate(0,0.5,0),tr.scale(1,1,1.5)])
    base_casa.childs += [gpuCasa]

    casa.childs += [base_casa]

    #puerta
    puerta = sg.SceneGraphNode('puerta')
    puerta.transform = tr.matmul([tr.translate(0,-0.18,0.63),tr.translate(0,0.5,0),tr.scale(0.3,0.6,0.3)])
    puerta.childs += [gpuPuerta]
    casa.childs += [puerta]


    #ventanas

    ventanas = sg.SceneGraphNode('ventanas')
    lista = [-1,1]
    for i in lista:
        ventana = sg.SceneGraphNode('ventana'+str(i))
        ventana.transform = tr.matmul([tr.translate(0,0.5,0.63*i),tr.translate(0,0.5,0),tr.scale(0.3,0.3,0.3)])
        ventana.childs += [gpuVentana]
        ventanas.childs += [ventana]
    for j in lista:
        for k in [0,0.55]:
            ventana = sg.SceneGraphNode('ventana'+str(j)+str(k))
            ventana.transform = tr.matmul([tr.translate(0.38*j,0,k-0.3),tr.translate(0,0.5,0),tr.scale(0.3,0.3,0.3)])
            ventana.childs += [gpuVentana]
            ventanas.childs += [ventana]

    
    casa.childs += [ventanas]

    #techo
    roof = sg.SceneGraphNode('roof')
    roof.transform = tr.matmul([tr.translate(-0.1,0.9,0),tr.rotationZ(-np.pi/4),tr.scale(0.75,1,1.5)])
    roof.childs += [gpuRoof]
    roof2 = sg.SceneGraphNode('roof2')
    roof2.transform = tr.matmul([tr.translate(+0.1,0.9,0),tr.rotationZ(np.pi/4),tr.scale(0.75,1,1.5)])
    roof2.childs += [gpuRoof]

    casa.childs += [roof,roof2]

    #rotar la casa"

    casa.transform = tr.matmul([tr.rotationY(-np.pi/2)])

    #hacer los barrios
    
    casas1 = sg.SceneGraphNode('casas1')
    for i in [0,1]:
        for j in range(1,10):
            home = sg.SceneGraphNode('C1'+str(i)+','+str(j))
            home.transform = tr.matmul([tr.translate(6.75+1.5*i,0,-1.5-j),tr.rotationY(np.pi*i)])
            if j==3 and i==0: #pongo una casa de minecraft para que se vea
                home.childs += [casa_minecraft]
            else:
                home.childs += [casa]
            casas1.childs += [home]

    
    floor.childs += [casas1]

    casas2 = sg.SceneGraphNode('casas2')
    for i in [0,1]:
        for j in range(1,10):
            home = sg.SceneGraphNode('C1'+str(i)+','+str(j))
            home.transform = tr.matmul([tr.translate(11.75+1.5*i,0,-1.5-j),tr.rotationY(np.pi*i)])
            home.childs += [casa]
            casas2.childs += [home]

    floor.childs += [casas2]




    #el barrio más chico, acá si se quiere ver las casas al hazar porfavor sacar los # y quitar el home.childs+=[casa]
    #esto para lo hago para que sepan que puedo poner las casas de manera random, pero se laguea mucho por lo pesado
    #que es la casa de minecraft al haber sido creado con muuchos cubos y partes individuales
    casas3 = sg.SceneGraphNode('casas3')
    for i in [0,1]:
        for j in range(1,5):
            k = random.randint(0,1)
            home = sg.SceneGraphNode('C3'+str(i)+','+str(j))
            home.transform = tr.matmul([tr.translate(1.75+1.5*i,0,-1.5-j),tr.rotationY(np.pi*i)])
            #if k==0:
            #    home.childs += [casa]
            #else:
            #    home.childs += [casa_minecraft]
            home.childs += [casa]
            casas2.childs += [home]
            

    floor.childs += [casas3]



    #se define el bloque de autopista
    autopista = sg.SceneGraphNode('autopista')
    autopista.transform = tr.matmul([tr.translate(0,-0.5,-1)])
    autopista.childs += [gpuAutopista]

    #se definen los bloques de pasto
    pasto = sg.SceneGraphNode('pasto')
    pasto.transform = tr.matmul([tr.translate(0,-0.5,-1)])
    pasto.childs += [gpuPasto]

    #y una mitad para un caso especifico
    mitad_pasto = sg.SceneGraphNode('pasto/2')
    mitad_pasto.transform = tr.matmul([tr.translate(0,-0.5,-1)])
    mitad_pasto.childs += [gpuMitad]

    ###############################

    #parten las autopistas verticales
    autopista1 = sg.SceneGraphNode('autopista1')
    for j in range(1,11):
        road = sg.SceneGraphNode('A1'+''+str(j))
        road.transform = tr.matmul([tr.translate(14.5,0,-0.5-j)])
        road.childs += [autopista]
        autopista1.childs += [road]
    
    floor.childs += [autopista1]

    autopista2 = sg.SceneGraphNode('autopista2')
    for i in range(0,2):
        for j in range(0,9):
            road = sg.SceneGraphNode('A2'+''+str(i)+','+str(j))
            road.transform = tr.matmul([tr.translate(9.5+i,0,-1.5-j)])
            road.childs += [autopista]
            autopista2.childs += [road]
    
    floor.childs += [autopista2]
    
    autopista3 = sg.SceneGraphNode('autopista3')
    autopista3.transform = tr.matmul([tr.translate(-5,0,0)])
    autopista3.childs += [autopista2]

    floor.childs += [autopista3]

    autopista5 = sg.SceneGraphNode('autopista5')
    for j in range(1,7):
        road = sg.SceneGraphNode('A5'+''+str(j))
        road.transform = tr.matmul([tr.translate(+0.5,0,-0.5-j)])
        road.childs += [autopista]
        autopista5.childs += [road]
    
    floor.childs += [autopista5]

    #para esta autopista hago un shearing para hacer que sea diagonal, de manera muy aproximada
    autopista6 = sg.SceneGraphNode('autopista6')
    for j in range(1,4):
        road = sg.SceneGraphNode('A6'+''+str(j))
        road.transform = tr.matmul([tr.shearing(0,0,-1,0,0,0),tr.translate(-7.5,0,-6.5-j)])
        road.childs += [autopista]
        autopista6.childs += [road]
    
    road4 = sg.SceneGraphNode('A6'+''+str(4))
    road4.transform = tr.matmul([tr.shearing(0,0,-1,0,0,0),tr.translate(-7.5,-0.001,-6.5-4)])
    road4.childs += [autopista]
    autopista6.childs += [road4]

    floor.childs += [autopista6]
    



    #autopistas horizontal

    autopista_down = sg.SceneGraphNode('autopista_down')
    autopista_down.transform = tr.matmul([tr.translate(0,-0.5,-1),tr.rotationY(np.pi/2)])
    autopista_down.childs += [gpuAutopista]

    autopista4 = sg.SceneGraphNode('autopista4')
    for i in range(0,15):
        road = sg.SceneGraphNode('A4'+' '+str(i))
        road.transform = tr.matmul([tr.translate(0.5+i,0,-0.5)])
        road.childs += [autopista_down]
        autopista4.childs += [road]
    
    floor.childs += [autopista4]

    autopista7 = sg.SceneGraphNode('autopista7')
    for i in range(0,10):
        road = sg.SceneGraphNode('A4'+' '+str(i))
        road.transform = tr.matmul([tr.translate(4.5+i,0,-10.5)])
        road.childs += [autopista_down]
        autopista4.childs += [road]

    ######################

    #parte del pasto
    pasto1 = sg.SceneGraphNode('pasto1')
    for i in range(1,4):
        for j in range(0,2):
            grass = sg.SceneGraphNode('P1'+' '+str(i)+' '+str(j))
            grass.transform = tr.matmul([tr.translate(0.5+i,0,-5.5-j)])
            grass.childs += [pasto]
            pasto1.childs += [grass]
    
    floor.childs += [pasto1]
    
    #parte del triangulo del pasto
    pasto2 = sg.SceneGraphNode('pasto2')
    pasto2.transform = tr.matmul([tr.translate(2.5,0,-6.5),tr.uniformScale(3)])
    pasto2.childs += [mitad_pasto]

    floor.childs += [pasto2]




    #Arboles del maincra que saqué del archivo dado en el aux y modifiqué para que funcionará acá,todo esto se puede
    #sacar también si se quieren más FPS

    shapeWoodBlock = createMinecraftBlock()
    gpuWoodBlock = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWoodBlock)
    gpuWoodBlock.fillBuffers(
        shapeWoodBlock.vertices, shapeWoodBlock.indices, GL_STATIC_DRAW)
    gpuWoodBlock.texture = es.textureSimpleSetup(
        getAssetPath("minecraft_wood.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Creamos el bloque de hojas
    shapeLeavesBlock = createMinecraftBlock()
    gpuLeavesBlock = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLeavesBlock)
    gpuLeavesBlock.fillBuffers(
        shapeLeavesBlock.vertices, shapeLeavesBlock.indices, GL_STATIC_DRAW)
    gpuLeavesBlock.texture = es.textureSimpleSetup(
        getAssetPath("minecraft_leaves.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    # Definimos el nodo arbol
    tree = sg.SceneGraphNode('tree')

    # Definimos el nodo tronco del arbol
    treeTrunk = sg.SceneGraphNode('treeTrunk')

    # Agregamos los bloques de madera al nodo tronco del arbol
    for i in range(5):
        woodBlock = sg.SceneGraphNode('woodBlock('+str(i)+')')
        woodBlock.transform = tr.matmul([tr.translate(
            0.0, 0.5*i, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.5, 0.0)])
        woodBlock.childs += [gpuWoodBlock]
        treeTrunk.childs += [woodBlock]
    
    # Agregamos el tronco del arbol al nodo arbol
    tree.childs += [treeTrunk]

    # Definimos el nodo follaje del arbol
    treeFoliage = sg.SceneGraphNode('treeFoliage')

    # Definimos el nodo follaje superior del arbol
    treeUpperFoliage = sg.SceneGraphNode('treeUpperFoliage')

    # Agregamos los bloque de hoja al nodo follaje superior del arbol
    for i in range(3):
        for j in range(2):
            for k in range(3):
                if(j == 1 or (j == 0 and ((i % 2) != 0 or (k % 2) != 0))):
                    leavesBlock = sg.SceneGraphNode(
                        'upperLeavesBlock('+str(i)+', '+str(j)+', '+str(k)+')')
                    leavesBlock.transform = tr.matmul([tr.translate(
                        0.5-0.5*i, -0.5*j, 0.5-0.5*k), tr.uniformScale(0.5), tr.translate(0.0, 6.5, 0.0)])
                    leavesBlock.childs += [gpuLeavesBlock]
                    treeUpperFoliage.childs += [leavesBlock]

    # Agregamos el nodo follaje superior del arbol al nodo follaje del arbol
    treeFoliage.childs += [treeUpperFoliage]

    # Definimos el nodo follaje inferior del arbol
    treeLowerFoliage = sg.SceneGraphNode('treeLowerFoliage')

    # Agregamos los bloques de hoja al nodo follaje inferior del arbol
    for i in range(5):
        for j in range(2):
            for k in range(5):
                if(i != 2 or k != 2):
                    leavesBlock = sg.SceneGraphNode(
                        'lowerLeavesBlock('+str(i)+', '+str(j)+', '+str(k)+')')
                    leavesBlock.transform = tr.matmul([tr.translate(
                        1.0-0.5*i, -0.5*j, 1.0-0.5*k), tr.uniformScale(0.5), tr.translate(0.0, 4.5, 0.0)])
                    leavesBlock.childs += [gpuLeavesBlock]
                    treeLowerFoliage.childs += [leavesBlock]

    # Agregamos el nodo follaje inferior del arbol al nodo follaje del arbol
    treeFoliage.childs += [treeLowerFoliage]

    # Agregamos el nodo follaje del arbol al nodo arbol
    tree.childs += [treeFoliage]
    trees = sg.SceneGraphNode('trees')
    for i in range(2):
        arbol = sg.SceneGraphNode('arbol'+' ' +str(i))
        arbol.transform = tr.matmul([tr.translate(3.5,0,-10+(i*1.1)),tr.uniformScale(0.3)])
        arbol.childs += [tree]
        trees.childs += [arbol]
    
    arbol = sg.SceneGraphNode('arbol'+' ' +str(i) + str(1))
    arbol.transform = tr.matmul([tr.translate(3.5-1,0,-10+(i*1.4)),tr.uniformScale(0.3)])
    arbol.childs += [tree]
    trees.childs += [arbol]

    floor.childs += [trees]


    

    
   





    

    # Agregamos el nodo piso al nodo escena
    scene.childs += [floor]

    #### DEBEN AGREGAR AQUI LOS NODOS NECESARIOS PARA MODELAR LA ESCENA ####

    return scene


def main():
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 2000
    height = 1000
    title = "Barrio genérico"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    cpuAxis = bs.createAxis(2)
    gpuAxis = es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    #acá es donde se crea la ESCENA, ya que se llama a la función que trabajamos harto
    dibujo = createScene(textureShaderProgram)

    #se llama al textureShaderProgram para poder procesar las texturas
    setPlot(textureShaderProgram, colorShaderProgram, width, height)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    #mientras las ventanas NO estén cerradas
    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        #controles, que estarán acá para que el movimiento sea fluido

        #si se usa el UP, entonces el ojo se mueve un poco en la dirección donde está mirando (FRONT)
        # y se hace lo mismo con at para que nos demos una vuelta
        if glfw.get_key(window,glfw.KEY_UP) == glfw.PRESS:
            controller.eye = controller.eye + controller.front*controller.avance
            controller.at  = controller.at  + controller.front*controller.avance
        
        if glfw.get_key(window,glfw.KEY_DOWN) == glfw.PRESS:
            controller.eye = controller.eye - controller.front*controller.avance
            controller.at  = controller.at  - controller.front*controller.avance
        
        #si nos movemos a la derecha, debemos movernos un poco en la dirección de la derecha, que es un producto
        #cruz entre el vector up y el front
        if glfw.get_key(window,glfw.KEY_RIGHT) == glfw.PRESS:
            controller.eye += controller.right*controller.avance
            controller.at  += controller.right*controller.avance

        if glfw.get_key(window,glfw.KEY_LEFT) == glfw.PRESS:
            controller.eye -= controller.right*controller.avance
            controller.at  -= controller.right*controller.avance

        #con la O subimos, es decir solo debe aumentar la coordenada Y del eye y del at
        if glfw.get_key(window,glfw.KEY_O) == glfw.PRESS:
            controller.eye[1] += controller.vuelo
            controller.at[1]  += controller.vuelo

        #con la L bajoamos
        if glfw.get_key(window,glfw.KEY_L) == glfw.PRESS:
            controller.eye[1] -= controller.vuelo
            controller.at[1]  -= controller.vuelo

        #se rota la camara, esto es complicado y funciona asi:
        #se quiere rotar el at con respecto al UP, que en este caso es paralelo al eye Y, por lo tanto debemos
        #transladar hacia el origen, rotar en Y y luego devolver a la posición original
        if glfw.get_key(window,glfw.KEY_A) == glfw.PRESS:
            copia = np.array([*controller.at,1])
            controller.at = tr.matmul([
                            tr.translate(*controller.eye),
                            tr.rotationY(controller.camera*10),
                            tr.translate(*-controller.eye),
                            copia])[0:3]
            controller.front = controller.at - controller.eye #se actualiza el front con el nuevo at
            controller.actualizarRight()
            
        if glfw.get_key(window,glfw.KEY_D) == glfw.PRESS:
            copia = np.array([*controller.at,1])
            controller.at = tr.matmul([
                            tr.translate(*controller.eye),
                            tr.rotationY(-controller.camera*10),
                            tr.translate(*-controller.eye),
                            copia])[0:3]
            controller.front = controller.at - controller.eye
            controller.actualizarRight()

        #esto es parecido solo que se tiene que rotar con respectol eje que marca hacia donde está la derecha
        if glfw.get_key(window,glfw.KEY_W) == glfw.PRESS:
            copia = np.array([*controller.at,1])
            controller.at = tr.matmul([
                            tr.translate(*controller.eye),
                            tr.rotationA(controller.camera,controller.right),
                            tr.translate(*-controller.eye),
                            copia])[0:3]
            controller.front = controller.at - controller.eye
            controller.actualizarRight()
        
        if glfw.get_key(window,glfw.KEY_S) == glfw.PRESS:
            copia = np.array([*controller.at,1])
            controller.at = tr.matmul([
                            tr.translate(*controller.eye),
                            tr.rotationA(-controller.camera,controller.right),
                            tr.translate(*-controller.eye),
                            copia])[0:3]
            controller.front = controller.at - controller.eye
            controller.actualizarRight()
        
        
        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        setView(textureShaderProgram, colorShaderProgram, controller)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if (controller.axesOn):
            # Drawing axes (no texture)
            glUseProgram(colorShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(
                colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            colorShaderProgram.drawCall(gpuAxis, GL_LINES)

        # Drawing minecraft's dirt block (with texture, another shader program)
        glUseProgram(textureShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(dibujo, textureShaderProgram, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()

    glfw.terminate()

    return 0


if __name__ == "__main__":
    main()


