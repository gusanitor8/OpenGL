import ctypes
import OpenGL.GL as ogl
from numpy import array, float32


class Buffer:
    def __init__(self, data):
        self.vertBuffer = array(data, dtype=float32)

        # vertex buffer object
        self.VBO = ogl.glGenBuffers(1)

        # vertex array object
        self.VAO = ogl.glGenVertexArrays(1)

    def render(self):
        ogl.glBindBuffer(ogl.GL.GL_ARRAY_BUFFER, self.VBO)
        ogl.glBindVertexArray(self.VAO)

        # especificar la informacion de los vertices
        ogl.glBufferData(ogl.GL.GL_ARRAY_BUFFER,  # buffer id
                            self.vertBuffer.nbytes,  # tamano del buffer en bytes
                            self.vertBuffer,  # informacion a cargar en el buffer
                            ogl.GL_STATIC_DRAW)  # uso que se le va a dar al buffer

        ogl.GL.glVertexAttribPointer(0,  # attribute number
                                     3,  # size
                                     ogl.GL_FLOAT,  # type
                                     ogl.GL_FALSE,  # is normalized
                                     4 * 3,  # stride
                                     ctypes.c_void_p(0))  # array buffer offset

        ogl.glEnableVertexAttribArray(0)
        ogl.glDrawArrays(ogl.GL_TRIANGLES, 0, int(len(self.vertBuffer) / 3))
