import pygame
from pygame.locals import *
import glm
from gl import Renderer
from Model import Model
from shaders import vertex_shader, fragment_shader, fat_shader

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
rend = Renderer(screen, target=(0, 6, -10))
rend.setShaders(fat_shader , fragment_shader)

triangleData = [
    -0.5, -0.5, 0.0,      0.0, 0.0,     0.0, 0.0, 1.0,
    -0.5, 0.5, 0.0,       0.0, 1.0,     0.0, 0.0, 1.0,
    0.5, -0.5, 0.0,       1.0, 0.0,     0.0, 0.0, 1.0,

    -0.5, 0.5, 0.0,       0.0, 1.0,     0.0, 0.0, 1.0,
    0.5, 0.5, 0.0,        1.0, 1.0,     0.0, 0.0, 1.0,
    0.5, -0.5, 0.0,       1.0, 0.0,     0.0, 0.0, 1.0
]
objectModel = Model("models/stormtrooper.obj", scale=(2, 2, 2), position=(0, 0, -10), textureName="textures/Stormtrooper_D.png")

rend.scene.append(objectModel)


isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            if event.key == pygame.K_SPACE:
                rend.toggleFillMode()

    if keys[pygame.K_d]:
        rend.camPosition.x += 2 * deltaTime
    elif keys[pygame.K_a]:
        rend.camPosition.x -= 2 * deltaTime

    if keys[pygame.K_s]:
        rend.camPosition.z += 2 * deltaTime
    elif keys[pygame.K_w]:
        rend.camPosition.z -= 2 * deltaTime

    if keys[pygame.K_q]:
        rend.camPosition.y += 5 * deltaTime
    elif keys[pygame.K_e]:
        rend.camPosition.y -= 5 * deltaTime

    if keys[pygame.K_UP]:
        if rend.fatness<1.0:
            rend.fatness += 1 * deltaTime
    elif keys[pygame.K_DOWN]:
        if rend.fatness > 0.0:
            rend.fatness -= 1 * deltaTime

    if keys[pygame.K_RIGHT]:
        objectModel.rotation.y += 45 * deltaTime
    elif keys[pygame.K_LEFT]:
        objectModel.rotation.y -= 45 * deltaTime

    #triangleModel.rotation.y += 45 * deltaTime

    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
