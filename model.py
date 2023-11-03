from OpenGL.GL import *
import glm
from numpy import array, float32


class Model(object):
    def __init__(self, data):
        self.vertBuffer = array(data, dtype=float32)

        # vertex buffer object
        self.VBO = glGenBuffers(1)

        # vertex array object
        self.VAO = glGenVertexArrays(1)

        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)


    def getModelMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))

        rotationMat = pitch * yaw * roll

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def render(self):
        # atamos los buffers del object a la GPU
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Especificamos informacion de vertices
        glBufferData(GL_ARRAY_BUFFER,  # buffer ID
                     self.vertBuffer.nbytes,  # buffer size in bytes
                     self.vertBuffer,  # buffer data
                     GL_STATIC_DRAW)  # usage

        # atributos
        # especificamos el contenido del vertice
        glVertexAttribPointer(0,  # attribute number
                              3,  # size
                              GL_FLOAT,  # type
                              GL_FALSE,  # is normalized
                              4 * 6,  # stride
                              ctypes.c_void_p(0))  # offset

        glEnableVertexAttribArray(0)

        # atributos de color
        glVertexAttribPointer(1,  # attribute number
                              3,  # size
                              GL_FLOAT,  # type
                              GL_FALSE,  # is normalized
                              4 * 6,  # stride
                              ctypes.c_void_p(4 * 3))

        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer) / 6))
