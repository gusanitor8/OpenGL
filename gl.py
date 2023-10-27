import glm
import OpenGL.GL as ogl
from OpenGl.GL.shaders import compileProgram, compileShader


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.clearColor = [0, 0, 0]

        ogl.glEnable(ogl.GL_DEPTH_TEST)
        ogl.glViewport(0, 0, self.width, self.height)
        self.scene = []

        self.active_shader = None

    def setShaders(self, vertex_shader, fragment_shader):
        if vertex_shader is not None and fragment_shader is not None:
            self.active_shader = compileProgram(compileShader(vertex_shader, ogl.GL_VERTEX_SHADER),
                                                compileShader(fragment_shader, ogl.GL_FRAGMENT_SHADER))

        else:
            self.active_shader = None

    def render(self):
        ogl.glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1)
        ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)

        if self.active_shader:
            ogl.glUseProgram(self.active_shader)

        for obj in self.scene:
            obj.render()
