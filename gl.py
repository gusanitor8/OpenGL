import glm
from OpenGL.GL import *


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.clearColor = [0, 0, 0]

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

    def render(self):
        glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)