from OpenGL.GL import *
from numpy import array, float32
import glm


class Model:
    def __init__(self, data):
        self.vertBuffer = array(data, dtype=float32)

        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)

        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)

        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(0, 0, 0)

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
            4 * 6,
            ctypes.c_void_p(0)
        )

        glEnableVertexAttribArray(0)

        # atributo de colores
        glVertexAttribPointer(
            1,
            3,
            GL_FLOAT,
            GL_FALSE,
            4 * 6,
            ctypes.c_void_p(4 * 3)
        )
        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES,
                     0,
                     int(len(self.vertBuffer) / 6))
