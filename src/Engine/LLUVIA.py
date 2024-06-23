import pygame
from OpenGL.raw.GLU import gluOrtho2D
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

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
    "Creditos",
    "Desarrollado por:",
    "Ordoñez Ana",
    "Rugama Halley",
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

# Función principal de renderizado
def main():
    clock = pygame.time.Clock()
    running = True
    y_offset = display[1]

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        y = y_offset

        for line in credits:
            render_text(line, (display[0] // 2 - 100, y))
            y -= 50  # Espacio entre líneas

        y_offset -= 1  # Mueve el texto hacia arriba

        if y_offset < -len(credits) * 30:
            y_offset = display[1]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
