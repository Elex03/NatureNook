import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# Inicializa Pygame y configura la ventana
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("Pantalla de Créditos")

# Configura OpenGL
glClearColor(0.0, 0.0, 0.0, 1.0)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, display[0], 0, display[1])
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Definir el texto de los créditos
credits = [
    "NATURENOOK",
    "Descripción",
    "Ana Ordoñez",
    "Halley Rugama:",
    "sonidos y animaciones",
    "Acuña Matuz",
    "Salguera Benjamin"
]

# Función para renderizar texto utilizando Pygame
def render_text(text, pos, font_size=24, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, False, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(pos[0], pos[1])
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# Cargar imagen y crear textura
def load_texture(image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.flip(image, True, False)
    image_data = pygame.image.tostring(image, "RGBA", True)
    width, height = image.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    return texture_id, width, height

# Renderizar textura
def render_texture(texture_id, pos, size):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(pos[0], pos[1])
    glTexCoord2f(1, 0)
    glVertex2f(pos[0] + size[0], pos[1])
    glTexCoord2f(1, 1)
    glVertex2f(pos[0] + size[0], pos[1] + size[1])
    glTexCoord2f(0, 1)
    glVertex2f(pos[0], pos[1] + size[1])
    glEnd()
    glDisable(GL_TEXTURE_2D)

# Función principal de renderizado
def main():
    clock = pygame.time.Clock()
    running = True
    y_offset = display[1]

    # Cargar imágenes de prueba
    texture_paths = ["halley2.png", "SOFI.png", "eliezer.png", "benja.png"]
    textures = [load_texture(path) for path in texture_paths]

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        y = y_offset

        for line in credits:
            render_text(line, (display[0] // 2 - 100, y))
            y -= 50  # Espacio entre líneas

        # Renderizar imágenes en diferentes posiciones
        positions = [(700, y + 200), (700, y + 300), (700, y + 400), (700, y + 100)]
        size = (80, 80)  # Tamaño de las imágenes
        for (texture_id, width, height), pos in zip(textures, positions):
            render_texture(texture_id, pos, size)

        y_offset -= 1  # Mueve el texto hacia arriba

        if y_offset < -len(credits) * 50:
            y_offset = display[1]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
