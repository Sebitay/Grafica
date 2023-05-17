import numpy as np
import pyglet
import sys
import os

import libs.basic_shapes as bs
import libs.transformations as tr
import libs.scene_graph as sg
import libs.gpu_shape as gs
import libs.shaders as sh

from libs.assets_path import getAssetPath
from libs.obj_handler import read_OBJ,read_OBJ2
from OpenGL.GL import *



ASSETS = {
    "nave_obj":getAssetPath("nave.obj"),
    "cubo_obj":getAssetPath('cubo.obj'),
    "piramide_obj":getAssetPath('piramide.obj'),
    "towers_obj":getAssetPath('towers.obj'),
    "piso_obj":getAssetPath('piso.obj'),
    "sombra_obj":getAssetPath('sombra.obj'),
    "gate_obj":getAssetPath('gate.obj'),
    "cannon_obj":getAssetPath('cannon.obj'),
    "caneria_obj":getAssetPath('caneria.obj')
    }
WIDTH, HEIGHT = 1600, 1000


class Controller(pyglet.window.Window):

    def __init__(self, width, height, title=f"Tarea 2"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.gpuSombra = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["sombra_obj"], (0.3,0.3,0.3)))
        self.sombra = sg.SceneGraphNode('sombra')
        self.sombra.childs += [self.gpuSombra]
        

        self.gpuNave = gs.createGPUShape(pipeline,read_OBJ(ASSETS["nave_obj"], (0,0,0)))
        self.nave = sg.SceneGraphNode("nave")
        self.nave.childs = [self.gpuNave]
        self.advance = 0
        self.pos = [0,0,0]
        self.rotation = 0
        self.rotationSpeed = 0
        self.upward = 0
        self.zrotation = 0

    def update(self):
        self.rotation += self.rotationSpeed
        self.pos[1] += self.advance*np.sin(self.zrotation)
        self.pos[0] += self.advance*np.cos(self.rotation)*np.cos(self.zrotation)
        self.pos[2] -= self.advance*np.sin(self.rotation)*np.cos(self.zrotation)
        self.nave.transform = tr.matmul([tr.matmul([tr.translate(self.pos[0],self.pos[1],self.pos[2]),tr.rotationY(self.rotation)]),tr.rotationZ(self.zrotation)])
        self.sombra.transform = tr.matmul([tr.translate(self.pos[0],-29.9,self.pos[2]),tr.scale(5,0,5)])

class Camera:

    def __init__(self, at=np.array([0.0, 0.0, 0.0]), eye=np.array([-20.0,6.0,5.0]), up=np.array([0.0, 1.0, 0.0])) -> None:
        self.fillPolygon = True
        self.showAxis = True
        self.eye = eye
        self.at = at
        self.up = up
        self.projection = tr.ortho(-WIDTH/(2*10), WIDTH/(2*10), -HEIGHT/(2*10), HEIGHT/(2*10), -2000, 2000)
        self.advance = 0
        self.rotate = 0
        self.rotation = 0
        self.elevate = 0
        self.zrotation = 0


    def update(self):
        self.rotation +=self.rotate
        self.at[1] +=np.sin(self.zrotation)*self.advance
        self.at[0] += np.cos(self.rotation)*self.advance*np.cos(self.zrotation)
        self.at[2] -= np.sin(self.rotation)*self.advance*np.cos(self.zrotation)
        self.eye[1] +=np.sin(self.zrotation)*self.advance
        self.eye[0] += np.cos(self.rotation)*self.advance*np.cos(self.zrotation)
        self.eye[2] -= np.sin(self.rotation)*self.advance*np.cos(self.zrotation)



def createScene():

    gpuCube = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["cubo_obj"], (1.0,0.5,0.3)))
    gpuPiramide = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["piramide_obj"], (1.0,0.5,0.3)))
    gpuTorres = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["towers_obj"], (0.2,1.0,1.0)))
    gpuPiso = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["piso_obj"], (0.4,0.2,0.0)))
    gpuGate = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["gate_obj"], (1,1,1)))
    gpuCannon = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["cannon_obj"], (1,1,1)))
    gpuCaneria = gs.createGPUShape(pipeline,read_OBJ2(ASSETS["caneria_obj"], (0.2,0.2,0.2)))



    #objetos individuales
    cubo_uno = sg.SceneGraphNode('cubo1')
    cubo_uno.transform = tr.translate(-100,0,-10)
    cubo_uno.childs += [gpuCube]

    piramide_uno = sg.SceneGraphNode('piramide1')
    piramide_uno.transform = tr.translate(0,-6.3,0)
    piramide_uno.childs +=[gpuPiramide]

    torre_uno = sg.SceneGraphNode('torre1')
    torre_uno.transform = tr.translate(200,-30,200)
    torre_uno.childs +=[gpuTorres]

    gate_uno = sg.SceneGraphNode('gate1')
    gate_uno.transform = tr.matmul([tr.matmul([tr.rotationY(np.pi/2),tr.scale(6,6,6)]),tr.translate(-10,-5,10)])
    gate_uno.childs +=[gpuGate]

    cannon_uno = sg.SceneGraphNode('cannon1')
    cannon_uno.transform = tr.matmul([tr.scale(6,6,6),tr.translate(-20,-5,20)])
    cannon_uno.childs +=[gpuCannon]

    caneria_uno = sg.SceneGraphNode('caneria1')
    caneria_uno.transform = tr.matmul([tr.translate(50,0,165),tr.rotationY(np.pi/2)])
    caneria_uno.childs +=[gpuCaneria]

    caneria_dos = sg.SceneGraphNode('caneria2')
    caneria_dos.transform = tr.matmul([tr.translate(10,0,150),tr.rotationY(np.pi)])
    caneria_dos.childs +=[gpuCaneria]

    caneria_tres = sg.SceneGraphNode('caneria3')
    caneria_tres.transform = tr.matmul([tr.translate(0,0,170),tr.rotationY(3*np.pi/2)])
    caneria_tres.childs +=[gpuCaneria]

    naveM = sg.SceneGraphNode("naveM")
    naveM.childs +=[controller.nave]
    naveM.childs +=[controller.sombra]

    naveI =  sg.SceneGraphNode("naveI")
    naveI.transform = tr.translate(-12,0,-8)
    naveI.childs +=[controller.nave]
    naveI.childs +=[controller.sombra]

    naveD =  sg.SceneGraphNode("naveD")
    naveD.transform = tr.translate(-12,0,8)
    naveD.childs +=[controller.nave]
    naveD.childs +=[controller.sombra]


    piso = sg.SceneGraphNode('piso')
    piso.transform = tr.matmul([tr.translate(0,-30,0),tr.scale(100,0,100)])
    piso.childs += [gpuPiso]

    #grupos de objetos
    cubos = sg.SceneGraphNode('cubos')
    cubos.transform = tr.scale(3,3,3)
    cubos.childs += [cubo_uno]

    piramides = sg.SceneGraphNode('piramides')
    piramides.transform = tr.scale(5,5,5)
    piramides.childs += [piramide_uno]

    torres = sg.SceneGraphNode('torres')
    torres.transform = tr.scale(1,1,1)
    torres.childs += [torre_uno]

    gates = sg.SceneGraphNode('gates')
    gates.transform = tr.scale(1,1,1)
    gates.childs += [gate_uno]
    
    cannons = sg.SceneGraphNode('cannons')
    cannons.transform = tr.scale(1,1,1)
    cannons.childs += [cannon_uno]

    canerias = sg.SceneGraphNode('canerias')
    canerias.transform = tr.translate(0,-30,0)
    canerias.childs += [caneria_uno]
    canerias.childs += [caneria_dos]
    canerias.childs += [caneria_tres]

    naves = sg.SceneGraphNode("naves")
    naves.childs += [naveM]
    naves.childs += [naveI]
    naves.childs += [naveD]


    #escena
    scene = sg.SceneGraphNode('scene')
    scene.childs += [naves]
    scene.childs += [cubos]
    scene.childs += [piramides]
    scene.childs += [torres]
    scene.childs += [piso]
    scene.childs += [gates]
    scene.childs += [cannons]
    scene.childs += [canerias]

    return scene


pipeline = sh.SimpleModelViewProjectionShaderProgram()
camera = Camera()
controller = Controller(width=WIDTH,height=HEIGHT)


glClearColor(0.1, 0.1, 0.1, 1.0)
glEnable(GL_DEPTH_TEST)
glUseProgram(pipeline.shaderProgram)
draw = createScene()


@controller.event
def on_key_press(symbol, modifiers):
    global draw
    if symbol == pyglet.window.key.W:
        controller.advance +=1
        camera.advance += 1
    elif symbol == pyglet.window.key.S:
        camera.advance -= 1
        controller.advance -=1
    elif symbol == pyglet.window.key.A:
        controller.rotationSpeed += 0.1
        camera.rotate +=0.1
    elif symbol == pyglet.window.key.D:
        camera.rotate -=0.1
        controller.rotationSpeed -= 0.1


@controller.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.W:
        controller.advance -=1
        camera.advance -= 1
    elif symbol == pyglet.window.key.S:
        camera.advance += 1
        controller.advance +=1
    elif symbol == pyglet.window.key.A:
        camera.rotate -= 0.1
        controller.rotationSpeed -= 0.1
    elif symbol == pyglet.window.key.D:
        camera.rotate += 0.1
        controller.rotationSpeed += 0.1


@controller.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    if pyglet.window.mouse.LEFT:
        controller.zrotation += 0.01*dy
        camera.zrotation += 0.01*dy

@controller.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        #controller.zrotation = 0
        #camera.zrotation = 0 
        pass
        

@controller.event
def on_draw():
    controller.clear()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = tr.lookAt(camera.eye,camera.at,camera.up) 
    camera.update()
    controller.update()
 
    sg.drawSceneGraphNode(draw,pipeline,"model")
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, camera.projection)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)



def update(dt, controller):
    controller.total_time += dt


if __name__ == '__main__':
    # Try to call this function 60 times per second
    pyglet.clock.schedule(update, controller)
    # Set the view
    pyglet.app.run()