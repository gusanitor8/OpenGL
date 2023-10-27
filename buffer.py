import ctypes

try:
    import OpenGL as ogl

    try:
        import OpenGL.GL  # this fails in <=2020 versions of Python on OS X 11.x
    except ImportError:
        print('Drat, patching for Big Sur')
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res: return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
except ImportError:
    pass
from numpy import array, float32


class Buffer:
    def __init__(self, data):
        self.vertBuffer = array(data, dtype=float32)

        # vertex buffer object
        self.VBO = ogl.GL.glGenBuffers(1)

        # vertex array object
        self.VAO = ogl.GL.glGenVertexArrays(1)

    def render(self):
        ogl.GL.glBindBuffer(ogl.GL.GL_ARRAY_BUFFER, self.VBO)
        ogl.GL.glBindVertexArray(self.VAO)

        # especificar la informacion de los vertices
        ogl.GL.glBufferData(ogl.GL.GL_ARRAY_BUFFER,  # buffer id
                            self.vertBuffer.nbytes,  # tamano del buffer en bytes
                            self.vertBuffer,  # informacion a cargar en el buffer
                            ogl.GL.GL_STATIC_DRAW)  # uso que se le va a dar al buffer

        ogl.GL.glVertexAttribPointer(0,  # attribute number
                                     3,  # size
                                     ogl.GL.GL_FLOAT,  # type
                                     ogl.GL.GL_FALSE,  # is normalized
                                     4 * 3,  # stride
                                     ctypes.c_void_p(0))  # array buffer offset

        ogl.GL.glEnableVertexAttribArray(0)
        ogl.GL.glDrawArrays(ogl.GL.GL_TRIANGLES, 0, int(len(self.vertBuffer) / 3))
