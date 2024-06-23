import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

# Inicializar Pygame y OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluOrtho2D(0, display[0], 0, display[1])

# Configuración del texto
font = pygame.font.SysFont("Arial", 32)
credits = "NATURENOOK"
text_speed = 0.05  # Velocidad a la que se imprimen los caracteres (en segundos)
current_text = ""

def render_text(text, x, y):
    """Renderiza el texto en las coordenadas (x, y)"""
    text_surface = font.render(text, False, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def main():
    global current_text
    last_update = time.time()

    y = 300
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Calcular el texto actual a mostrar basado en el tiempo
        if len(current_text) < len(credits) and time.time() - last_update >= text_speed:
            y+= 10
            current_text += credits[len(current_text)]
            last_update = time.time()

        # Renderizar el texto
        render_text(current_text, 300, y)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
