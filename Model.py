from OpenGL.GL import *
from numpy import array, float32
import pygame
import glm


class Model:
    def __init__(self, data, textureName=None, position=(0,0,-5), rotation=(0,0,0), scale=(1,1,1)):
        self.vertBuffer = array(data, dtype=float32)

        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)

        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)

        if textureName is not None:
            self.loadTexture(textureName)

        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)

    def loadTexture(self, textureName):
        self.textureSurface = pygame.image.load(textureName)
        self.textureData = pygame.image.tostring(self.textureSurface, "RGB", True)
        self.textureBuffer = glGenTextures(1)

    def getModelMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))

        rotateMat = pitch * yaw * roll

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotateMat * scaleMat

    def render(self):
        # atamos los bbuffers a la GPU
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Espeificar la informacion de vertices
        glBufferData(GL_ARRAY_BUFFER,
                     self.vertBuffer.nbytes,
                     self.vertBuffer,
                     GL_STATIC_DRAW)

        # Atributos
        # Especificar el contenido del buffer
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            4 * 8,
            ctypes.c_void_p(0)
        )

        glEnableVertexAttribArray(0)


        # atributo de textura
        glVertexAttribPointer(
            1,
            2,
            GL_FLOAT,
            GL_FALSE,
            4 * 8,
            ctypes.c_void_p(4 * 3)
        )
        glEnableVertexAttribArray(1)

        # atributo de normales
        glVertexAttribPointer(
            2,
            3,
            GL_FLOAT,
            GL_FALSE,
            4 * 8,
            ctypes.c_void_p(4 * 5)
        )
        glEnableVertexAttribArray(1)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
        glTexImage2D(GL_TEXTURE_2D,
                                 0,
                                 GL_RGB,
                                 self.textureSurface.get_width(),
                                 self.textureSurface.get_height(),
                                 0,
                                 GL_RGB,
                                 GL_UNSIGNED_BYTE,
                                 self.textureData)

        glGenerateTextureMipmap(self.textureBuffer)



        glDrawArrays(GL_TRIANGLES,
                     0,
                     int(len(self.vertBuffer) / 8))
