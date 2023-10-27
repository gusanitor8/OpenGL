import glm

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

from OpenGl.GL.shaders import compileProgram, compileShader

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.clearColor = [0, 0, 0]

        ogl.GL.glEnable(ogl.GL.GL_DEPTH_TEST)
        ogl.GL.glViewport(0, 0, self.width, self.height)
        self.scene = []

        self.active_shader = None

    def setShaders(self, vertex_shader, fragment_shader):
        if vertex_shader is not None and fragment_shader is not None:
            self.active_shader = compileProgram(compileShader(vertex_shader, ogl.GL.GL_VERTEX_SHADER),
                                                compileShader(fragment_shader, ogl.GL.GL_FRAGMENT_SHADER))

        else:
            self.active_shader = None

    def render(self):
        ogl.GL.glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1)
        ogl.GL.glClear(ogl.GL.GL_COLOR_BUFFER_BIT | ogl.GL.GL_DEPTH_BUFFER_BIT)

        if self.active_shader:
            ogl.GL.glUseProgram(self.active_shader)

        for obj in self.scene:
            obj.render()