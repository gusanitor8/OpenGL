import pygame
from pygame.locals import *
import glm
from gl import Renderer
from Model import Model
from shaders import vertex_shader, fragment_shader, fat_shader


def run():
    width = 960
    height = 540

    pygame.init()

    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    rend = Renderer(screen, target=(0, 6, -10))
    rend.setShaders(vertex_shader, fragment_shader)

    stormtrooper_model = Model("models/stormtrooper.obj", scale=(2, 2, 2), position=(0, 0, -10),
                               textureName="textures/Stormtrooper_D.png")
    face_model = Model("models/model.obj", position=(0, 0, -10), textureName="textures/model.bmp")
    cat_model = Model("models/cat.obj", position=(0, 0, -10), textureName="textures/cat.jpg")

    rend.scene.append(stormtrooper_model)
    rend.scene.append(face_model)
    rend.scene.append(cat_model)

    def on_mouse_move(delta_x, delta_y):
        sensitivity = 0.1

        rend.camRotation.x += sensitivity * delta_y
        rend.camRotation.y += sensitivity * delta_x


    prev_mouse_pos = pygame.mouse.get_pos()
    left_button_pressed = False

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

                if event.key == pygame.K_RIGHT:
                    rend.next_obj()
                elif event.key == pygame.K_LEFT:
                    rend.prev_obj()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # Zoom out
                    if rend.fov < 125:
                        rend.fov += 40 * deltaTime

                elif event.button == 4:  # Zoom In
                    if rend.fov > 10:
                        rend.fov -= 40 * deltaTime

                if event.button == 1:  # Left mouse button
                    left_button_pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_button_pressed = False

        if left_button_pressed:
            current_mouse_pos = pygame.mouse.get_pos()

            # Calculate the change in mouse position
            dx = current_mouse_pos[0] - prev_mouse_pos[0]
            dy = current_mouse_pos[1] - prev_mouse_pos[1]

            # Call function based on mouse movement
            on_mouse_move(dx, dy)

        prev_mouse_pos = pygame.mouse.get_pos()

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
            if rend.fatness < 1.0:
                rend.fatness += 1 * deltaTime
        elif keys[pygame.K_DOWN]:
            if rend.fatness > 0.0:
                rend.fatness -= 1 * deltaTime

        # triangleModel.rotation.y += 45 * deltaTime

        rend.update()
        rend.render()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
