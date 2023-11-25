import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Renderer:
    def __init__(self, screen, target=(0, 0, 0)):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.clearColor = [0, 0, 0]
        self.elapsed_time = 0.0
        self.target = glm.vec3(*target)
        self.fov = 60

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        #glGenerateMipmap(GL_TEXTURE_2D)
        glViewport(0, 0, self.width, self.height)

        self.scene = []
        self.current_obj_idx = 0
        self.activeShader = None

        self.dirLight = glm.vec3(1, 0, 0)
        self.fatness = 0

        self.fillMode = True

        # view matrix
        self.camPosition = glm.vec3(0, 0, 0)
        self.camRotation = glm.vec3(0, 0, 0)
        self.viewMatrix = self.getViewMatrix()

        # projection matrix
        self.projectionMatrix = glm.perspective(glm.radians(self.fov),
                                                self.width / self.height,
                                                0.1,
                                                1000)

    def getProjectionMatrix(self):
        return glm.perspective(glm.radians(self.fov),
                                                self.width / self.height,
                                                0.1,
                                                1000)

    def next_obj(self):
        if self.scene:
            self.current_obj_idx = (self.current_obj_idx + 1) % len(self.scene)

    def prev_obj(self):
        if self.scene:
            self.current_obj_idx = (self.current_obj_idx - 1) % len(self.scene)

    def toggleFillMode(self):
        self.fillMode = not self.fillMode
        if self.fillMode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glEnable(GL_CULL_FACE)

        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDisable(GL_CULL_FACE)

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

    def update(self):
        self.viewMatrix = self.getViewMatrix()
        #self.viewMatrix = glm.lookAt(self.camPosition, self.target, glm.vec3(0,1,0))
        self.projectionMatrix = self.getProjectionMatrix()


    def render(self):
        glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.activeShader is not None:
            glUseProgram(self.activeShader)

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'viewMatrix'),
                               1,
                               GL_FALSE,
                               glm.value_ptr(self.viewMatrix))

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'projectionMatrix'),
                               1,
                               GL_FALSE,
                               glm.value_ptr(self.projectionMatrix))

            glUniform3fv(glGetUniformLocation(self.activeShader, 'dirLight'),
                         1,
                         glm.value_ptr(self.dirLight))

            glUniform3fv(glGetUniformLocation(self.activeShader, 'camRot'),
                         1,
                         glm.value_ptr(self.camRotation))

            glUniform1f(glGetUniformLocation(self.activeShader, 'fatness'),
                         self.fatness)

            glUniform1f(glGetUniformLocation(self.activeShader, 'time'),
                        self.elapsed_time)

        if self.scene:
            obj = self.scene[self.current_obj_idx]
            if self.activeShader is not None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, 'modelMatrix'),
                                   1,
                                   GL_FALSE,
                                   glm.value_ptr(obj.getModelMatrix()))
            obj.render()
