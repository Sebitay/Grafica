import numpy as np
import pyglet
import sys
import os

import libs.basic_shapes as bs
import libs.transformations as tr
import libs.easy_shaders as es
import libs.scene_graph as sg
import libs.gpu_shape as gs
import libs.shaders as sh

from libs.assets_path import getAssetPath
from libs.obj_handler import read_OBJ
from OpenGL.GL import *



ASSETS = {"nave_obj":getAssetPath("nave.obj")}
WIDTH, HEIGHT = 800, 800


class Controller(pyglet.window.Window):

    def __init__(self, width, height, title=f"nave :3"):
        super().__init__(width, height, title)
        self.total_time = 0.0


class Camera:

    def __init__(self):
        self.fillPolygon = True
        self.showAxis = False
        self.eye = np.array([5,5,5])
        self.at = np.array([0,0,0])
        self.up = np.array([0,1,0])
        self.projection = tr.ortho(-8, 8, -8, 8, 0.1, 100)
    


def createScene(pipeline, r, g, b):
    color =(r,g,b)
    gpuNave = gs.createGPUShape(pipeline,read_OBJ(ASSETS["nave_obj"], color))

    nave = sg.SceneGraphNode("nave")
    nave.transform = tr.identity()
    nave.childs +=[gpuNave]

    return nave


camera = Camera()
controller = Controller(width=WIDTH,height=HEIGHT)
pipeline = sh.SimpleModelViewProjectionShaderProgram()


glClearColor(0.1, 0.1, 0.1, 1.0)
glEnable(GL_DEPTH_TEST)
glUseProgram(pipeline.shaderProgram)


@controller.event
def on_draw():
    controller.clear()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = tr.lookAt(camera.eye,camera.at,camera.up)


    draw = createScene(pipeline,0,0,1)
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