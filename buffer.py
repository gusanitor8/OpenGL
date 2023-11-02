from OpenGL.GL import *
from numpy import array, float32


class Buffer(object):
    def __init__(self, data):
        self.data = data
        self.vertBuffer = array(data, dtype=float32)

        # vertex buffer object
        self.VBO = glGenBuffers(1)

        # vertex array object
        self.VAO = glGenVertexArrays(1)

    def render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

