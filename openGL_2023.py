import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import vertex_shader, fragment_shader

width = 950
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader, fragment_shader)

# temporal
triangle = [-0.5, -0.5, 0.0,
            0, 0.5, 0.0,
            0.5, -0.5, 0.0]

rend.scene.append(Buffer(triangle))

isRunning = True

while isRunning:
    keys = pygame.key.get_pressed()
    deltaTime = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    if keys[pygame.K_RIGHT]:
        if rend.clearColor[0] < 1:
            rend.clearColor[0] += 0.01 * deltaTime

    pygame.display.flip()

pygame.quit()
