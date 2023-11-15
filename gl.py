import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.clearColor = [0, 0, 0]

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.scene = []
        self.activeShader = None

        # view matrix
        self.camPosition = glm.vec3(0, 0, 0)
        self.camRotation = glm.vec3(0, 0, 0)

        # projection matrix
        self.projectionMatrix = glm.perspective(glm.radians(60),
                                                self.width / self.height,
                                                0.1,
                                                1000)


    def getViewMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.camPosition)

        pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0, 0, 1))

        rotateMat = pitch * yaw * roll

        camMatrix = translateMat * rotateMat

        return glm.inverse(camMatrix)


    def setShaders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                               compileShader(fragmentShader, GL_FRAGMENT_SHADER))
            glUseProgram(self.activeShader)
        else:
            self.activeShader = None



    def render(self):
        glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.activeShader is not None:
            glUseProgram(self.activeShader)

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'viewMatrix'),
                               1,
                               GL_FALSE,
                               glm.value_ptr(self.getViewMatrix()))

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'projectionMatrix'),
                               1,
                               GL_FALSE,
                               glm.value_ptr(self.projectionMatrix))

        for obj in self.scene:
            if self.activeShader is not None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'modelMatrix'),
                                   1,
                                   GL_FALSE,
                                   glm.value_ptr(obj.getModelMatrix()))
            obj.render()

