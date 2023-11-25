import pygame
from pygame.locals import *
import glm
from gl import Renderer
from Model import Model
from shaders import vertex_shader, fragment_shader, fat_shader, acid_shader, woobly_vertex_shader, \
    shinny_edges_fragment_shader, noise_fragment_shader

GLOB_look_at = False

def menu():
    print("""
    Bienvenido al proyecto 3 de Graficas por Computadora!!

    A continuacion el indice de opciones:
        CAMARA:
            - Usa el mouse para rotar la camara haciendo click y moviendo en cualquier punto de la ventana
        
        MOVIMIENTO:
            - Usa WASD Para moverte de atras para adelante y de un lado para otro
            - Usa Q y E para moverte hacia arriba y abajo
    
        WIREFRAME:
            - Presiona espacio para poner la vista en modo wireframe
    
        LOOK AT:
            - Presiona O para activar y desactivar el look at
    
        ZOOM:
            - Usa la rueda de tu mouse para hacer zoom in y zoom out
    
        MODELOS:
            - Usa las flechas de los lados para cambiar de modelo.
    
        SHADERS:
            - Presiona 1 para un vertex shader standard
            - Presiona 2 para un fragment shader standard
            - Presiona 3 para el acid shader
            - Presiona 4 para usar el fat shader
                - Puedes usar las flechas de arriba y abajo para ajustar la configuracion de gordura del modelo
            - Presiona 5 para usar el shinny shader (RECUERDA MOVER TU CAMARA PARA VER EL EFECTO)
            - Presiona 6 para usar el noise shader
            - Presiona 7 para usar el woobly shader
        
    
    Finalmente disfruta de la musica ;)
""")


def run():
    width = 960
    height = 540

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("music/rick_roll.mp3")
    pygame.mixer.music.play(-1)
    menu()

    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    rend = Renderer(screen, target=(0, 6, -10))
    curr_vertex_shader = vertex_shader
    curr_fragment_shader = acid_shader
    rend.setShaders(curr_vertex_shader, curr_fragment_shader)

    def update_shader(render: Renderer):
        rend.setShaders(curr_vertex_shader, curr_fragment_shader)

    def toggle_look_at():
        rend.look_at = not rend.look_at
        global GLOB_look_at
        GLOB_look_at = not GLOB_look_at


    stormtrooper_model = Model("models/stormtrooper.obj", scale=(2, 2, 2), position=(0, -5, -10),
                               textureName="textures/Stormtrooper_D.png")
    face_model = Model("models/model.obj", scale=(3, 3, 3), position=(0, 0, -10), textureName="textures/model.bmp")
    cat_model = Model("models/cat.obj", position=(0, -2, -10), scale=(0.1, 0.1, 0.1), rotation=(-60, 0, 20),
                      textureName="textures/cat.jpg")
    skull_model = Model("models/skull.obj", position=(0, 0, -10), scale=(0.2, 0.2, 0.2), rotation=(-45, 0, 0),
                        textureName="textures/Skull.jpg")
    rick_model = Model("models/rickastley.obj", position=(0, -18, -12), rotation=(0, -25, 0), scale=(0.3, 0.3, 0.3),
                       textureName="textures/rickastley.jpg")

    rend.scene.append(rick_model)
    rend.scene.append(stormtrooper_model)
    rend.scene.append(face_model)
    rend.scene.append(cat_model)
    rend.scene.append(skull_model)

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

                if event.key == pygame.K_o:
                    toggle_look_at()

                if event.key == pygame.K_1:
                    curr_vertex_shader = vertex_shader
                    update_shader(rend)
                elif event.key == pygame.K_2:
                    curr_fragment_shader = fragment_shader
                    update_shader(rend)
                elif event.key == pygame.K_3:
                    curr_fragment_shader = acid_shader
                    update_shader(rend)
                elif event.key == pygame.K_4:
                    curr_vertex_shader = fat_shader
                    update_shader(rend)
                elif event.key == pygame.K_5:
                    curr_fragment_shader = shinny_edges_fragment_shader
                    update_shader(rend)
                elif event.key == pygame.K_6:
                    curr_fragment_shader = noise_fragment_shader
                    update_shader(rend)
                elif event.key == pygame.K_7:
                    curr_vertex_shader = woobly_vertex_shader
                    update_shader(rend)


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

        if not GLOB_look_at:
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

        rend.elapsed_time += deltaTime
        rend.update()
        rend.render()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
