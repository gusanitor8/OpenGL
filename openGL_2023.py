import pygame
from pygame.locals import *
from gl import Renderer
from Buffer import Buffer

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
rend = Renderer(screen)

triangle = [
    -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0,
    0.0, 0.5, 0.0
]

rend.scene.append(Buffer(triangle))

triangleBuffer = Buffer(triangle)

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

    if keys[pygame.K_RIGHT]:
        if rend.clearColor[0] < 1.0:
            rend.clearColor[0] += deltaTime

    elif keys[pygame.K_LEFT]:
        if rend.clearColor[0] > 0.0:
            rend.clearColor[0] -= deltaTime

    elif keys[pygame.K_UP]:
        if rend.clearColor[1] < 1.0:
            rend.clearColor[1] += deltaTime

    elif keys[pygame.K_DOWN]:
        if rend.clearColor[1] > 0.0:
            rend.clearColor[1] -= deltaTime

    elif keys[pygame.K_x]:
        if rend.clearColor[2] < 1.0:
            rend.clearColor[2] += deltaTime

    elif keys[pygame.K_z]:
        if rend.clearColor[2] > 0.0:
            rend.clearColor[2] -= deltaTime

    rend.render()
    pygame.display.flip()

pygame.quit()
