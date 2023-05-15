import libs.transformations as tr
from OpenGL.GL import glUseProgram, glUniformMatrix4fv, glGetUniformLocation,\
    GL_TRUE, glUniform3f, glUniform1ui, glUniform1f
import numpy as np
import libs.basic_shapes as bs


def setPlot(pipeline, mvpPipeline, width, height):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "lightPosition"), 5, 5, 5)

    glUniform1ui(glGetUniformLocation(
        pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(
        pipeline.shaderProgram, "constantAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(
        pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(
        pipeline.shaderProgram, "quadraticAttenuation"), 0.01)


def setView(pipeline, mvpPipeline, controller):
    view = tr.lookAt(controller.eye,controller.at,controller.up)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"),
                *controller.eye)

def MitadAutopista():
    vertices = [ 0.5, 0.5, -0.5, 1/6, 1, #super-der
                 0.5, 0.5,  0.5, 0, 1, #inf-der
                 -0.5, 0.5,  0.5, 0,0] #inf-izq
    indices =  [0,1,2]

    return bs.Shape(vertices,indices)


def CuadradoAutopista():
    vertices = [-0.5, 0.5, -0.5, 1, 0, 
                 0.5, 0.5, -0.5, 1, 1, 
                 0.5, 0.5,  0.5, 0, 1,  #  +Y
                 -0.5, 0.5,  0.5, 0,0]
    indices =  [0, 1, 2, 2, 3, 0]

    return bs.Shape(vertices, indices)

def Frente_casa():
    vertices = [
        #   positions         texture coordinates
        # Z+: block top
        0.5,  0.5,  0.5, 1, 0, #0: sup-dere
        0.5, -0.5,  0.5, 1, 1,   #1: inf-der
        -0.5, -0.5,  0.5, 0, 1,  #2  inf-izq
        -0.5,  0.5,  0.5, 0,0] #3: sup.izq
    indices = [
        0, 1, 2, 2, 3, 0]  # Z+

    return bs.Shape(vertices, indices)

def Lado_2ventana():
    vertices = [0.5, -0.5, -0.5, 1, 1,  #inf-der
        0.5,  0.5, -0.5,1, 0,   #sup-der
        0.5,  0.5,  0.5,0, 0,   #sup.izq
        0.5, -0.5,  0.5, 0,1   ]#inf-izq
    indices =  [0, 1, 2, 2, 3, 0]
    return bs.Shape(vertices, indices)

def Lado_1ventana():
    vertices = [-0.5, -0.5, -0.5, 0,1,  #inf-izq
        -0.5,  0.5, -0.5, 0, 0,  #sup-izq
        -0.5,  0.5,  0.5, 1, 0,  #sup-der
        -0.5, -0.5,  0.5, 1,1   ]#inf-der
    indices =  [0, 1, 2, 2, 3, 0]
    return bs.Shape(vertices, indices)

def Lado_trasero():
    vertices = [-0.5, -0.5, -0.5, 0, 1, #inf-izq
        0.5, -0.5, -0.5, 1, 1,  #inf-der
        0.5,  0.5, -0.5, 1, 0,  #sup-der
        -0.5,  0.5, -0.5, 0,0,  ]#sup-izq
    indices =  [0, 1, 2, 2, 3, 0]
    return bs.Shape(vertices, indices)


def Base_casa():
    vertices = [
        #   positions         texture coordinates
        # Z+: block top
        0.5,  0.5,  0.5, 1, 0, #0: sup-dere
        0.5, -0.5,  0.5, 1, 1,   #1: inf-der
        -0.5, -0.5,  0.5, 0, 1,  #2  inf-izq
        -0.5,  0.5,  0.5, 0,0,  #3: sup.izq

        # Z-: block bottom
        -0.5, -0.5, -0.5, 0, 1, #inf-izq
        0.5, -0.5, -0.5, 1, 1,  #inf-der
        0.5,  0.5, -0.5, 1, 0,  #sup-der
        -0.5,  0.5, -0.5, 0,0,  #sup-izq

        # X+: block right
        0.5, -0.5, -0.5, 1, 1,  #inf-der
        0.5,  0.5, -0.5,1, 0,   #sup-der
        0.5,  0.5,  0.5,0, 0,   #sup.izq
        0.5, -0.5,  0.5, 0,1,   #inf-izq

        # X-: block left
        -0.5, -0.5, -0.5, 0,1,  #inf-izq
        -0.5,  0.5, -0.5, 0, 0,  #sup-izq
        -0.5,  0.5,  0.5, 1, 0,  #sup-der
        -0.5, -0.5,  0.5, 1,1,   #inf-der

        # Y-: yellow face
        -0.5, -0.5, -0.5, 1, 0, #16 
        0.5, -0.5, -0.5, 1, 1,  #17
        0.5, -0.5,  0.5, 0, 1,  #18
        -0.5, -0.5,  0.5, 0,0, #19

        #triangulos sobre la casa:
        
        #triangulo en Z+
        0.5,  0.5,  0.5, 1, 1, #sup dere #20
        -0.5,  0.5,  0.5, 0,1, #sup izq #21
          0,    1,   0.5, 0.5,0,  #22 punta

        #triangulo en Z-
        0.5,  0.5, -0.5, 1, 1,  #sup-der 23
        -0.5,  0.5, -0.5, 0,1,  #sup-izq 24
          0,    1,   -0.5,0.5,0  #25 punta
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,# Y-
        21,22,20,24,25,23]  #triangulo en Z

    return bs.Shape(vertices, indices)

def createMinecraftBlock():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top
        0.5,  0.5,  0.5, 1/4, 2/3,
        0.5, -0.5,  0.5, 0, 2/3,
        -0.5, -0.5,  0.5, 0, 1/3,
        -0.5,  0.5,  0.5, 1/4, 1/3,

        # Z-: block bottom
        -0.5, -0.5, -0.5, 3/4, 1/3,
        0.5, -0.5, -0.5, 3/4, 2/3,
        0.5,  0.5, -0.5, 2/4, 2/3,
        -0.5,  0.5, -0.5, 2/4, 1/3,

        # X+: block left
        0.5, -0.5, -0.5, 2/4, 1,
        0.5,  0.5, -0.5, 2/4, 2/3,
        0.5,  0.5,  0.5, 1/4, 2/3,
        0.5, -0.5,  0.5, 1/4, 1,

        # X-: block right
        -0.5, -0.5, -0.5, 3/4, 2/3,
        -0.5,  0.5, -0.5, 2/4, 2/3,
        -0.5,  0.5,  0.5, 2/4, 1/3,
        -0.5, -0.5,  0.5, 3/4, 1/3,

        # Y+: white face
        -0.5,  0.5, -0.5, 2/4, 1/3,
        0.5,  0.5, -0.5, 2/4, 2/3,
        0.5,  0.5,  0.5, 1/4, 2/3,
        -0.5,  0.5,  0.5, 1/4, 1/3,

        # Y-: yellow face
        -0.5, -0.5, -0.5, 1, 1/3,
        0.5, -0.5, -0.5, 1, 2/3,
        0.5, -0.5,  0.5, 3/4, 2/3,
        -0.5, -0.5,  0.5, 3/4, 1/3
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return bs.Shape(vertices, indices)

def cubo():
    vertices = [
        #   positions         texture coordinates
        # Z+: block top
        0.5,  0.5,  0.5, 1, 0, #0: sup-dere
        0.5, -0.5,  0.5, 1, 1,   #1: inf-der
        -0.5, -0.5,  0.5, 0, 1,  #2  inf-izq
        -0.5,  0.5,  0.5, 0,0,  #3: sup.izq

        # Z-: block bottom
        -0.5, -0.5, -0.5, 0, 1, #inf-izq
        0.5, -0.5, -0.5, 1, 1,  #inf-der
        0.5,  0.5, -0.5, 1, 0,  #sup-der
        -0.5,  0.5, -0.5, 0,0,  #sup-izq

        # X+: block right
        0.5, -0.5, -0.5, 1, 1,  #inf-der
        0.5,  0.5, -0.5,1, 0,   #sup-der
        0.5,  0.5,  0.5,0, 0,   #sup.izq
        0.5, -0.5,  0.5, 0,1,   #inf-izq

        # X-: block left
        -0.5, -0.5, -0.5, 0,1,  #inf-izq
        -0.5,  0.5, -0.5, 0, 0,  #sup-izq
        -0.5,  0.5,  0.5, 1, 0,  #sup-der
        -0.5, -0.5,  0.5, 1,1,   #inf-der

        # Y-: yellow face
        -0.5, -0.5, -0.5, 1, 0, #16 
        0.5, -0.5, -0.5, 1, 1,  #17
        0.5, -0.5,  0.5, 0, 1,  #18
        -0.5, -0.5,  0.5, 0,0,  #19
        
        # Y+: yellow face
        -0.5, +0.5, -0.5, 1, 0, #20
        0.5, +0.5, -0.5, 1, 1,  #21
        0.5, +0.5,  0.5, 0, 1,  #22
        -0.5, +0.5,  0.5, 0,0 #23

        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,# Y-
        23,22,21,21,20,23]  #+Y

    return bs.Shape(vertices, indices)

    