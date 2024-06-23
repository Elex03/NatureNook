# main.py

import pygame
from pygame.locals import *
import button
import opengl_config  # Importa el archivo de configuración de OpenGL

pygame.init()

# Define las dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Configura la pantalla de Pygame y OpenGL
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Main Menu")

# Inicializa OpenGL usando la función del archivo de configuración
opengl_config.init_opengl()

# Variables del juego
game_paused = False
menu_state = "main"
run = True

# Define fuentes
font = pygame.font.SysFont("arialblack", 40)

# Define colores
TEXT_COL = (128, 128, 128)

# Carga las imágenes de los botones
resume_img = pygame.image.load("button_resume.png").convert_alpha()
options_img = pygame.image.load("button_options.png").convert_alpha()
quit_img = pygame.image.load("button_quit.png").convert_alpha()
video_img = pygame.image.load('button_video.png').convert_alpha()
audio_img = pygame.image.load('button_audio.png').convert_alpha()
keys_img = pygame.image.load('button_keys.png').convert_alpha()
back_img = pygame.image.load('button_back.png').convert_alpha()

# Crea instancias de los botones
resume_button = button.Button(304, 125, resume_img, 1)
options_button = button.Button(297, 250, options_img, 1)
quit_button = button.Button(336, 375, quit_img, 1)
video_button = button.Button(226, 75, video_img, 1)
audio_button = button.Button(225, 200, audio_img, 1)
keys_button = button.Button(246, 325, keys_img, 1)
back_button = button.Button(332, 450, back_img, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def create_menu_surface():
    global game_paused, menu_state, run
    menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu_surface.fill((52, 78, 91))

    if game_paused:
        if menu_state == "main":
            if resume_button.draw(menu_surface):
                game_paused = False
            if options_button.draw(menu_surface):
                menu_state = "options"
            if quit_button.draw(menu_surface):
                run = False
        elif menu_state == "options":
            if video_button.draw(menu_surface):
                print("Video Settings")
            if audio_button.draw(menu_surface):
                print("Audio Settings")
            if keys_button.draw(menu_surface):
                print("Change Key Bindings")
            if back_button.draw(menu_surface):
                menu_state = "main"
    else:
        draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

    return menu_surface


def surface_to_texture(surface):
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture_id


def draw_texture(texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 0.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)



# Bucle del juego
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = not game_paused
        if event.type == pygame.QUIT:
            run = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)

    # Renderiza el menú como una textura en OpenGL
    menu_surface = create_menu_surface()
    menu_texture = surface_to_texture(menu_surface)
    draw_texture(menu_texture)

    pygame.display.flip()

pygame.quit()
