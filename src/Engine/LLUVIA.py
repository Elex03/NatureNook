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
    "Description:",
    "In today's technological and urban era,many people suffer from",
    "stress and anxiety due to constant exposure to devices electronics",
    "and the noise of the city.This generates a disconnection,"
    "with nature, ",
    "making it difficult to find moments of calm. Therefore, there is a",
    "growing need for virtual spaces that,"
    "offer a refuge in natural environments, ",
    "allowing you to relax,"
    "rejuvenate and reconnect with the environment.",
    "-------------------------------",
    "Developers: ",
    "__________________",
    "Ana Ordoñez:",
    "Role: Responsible for the User Interface (UI)",
    "Responsibilities:",
    "Design and creation of interactive menus.",
    "Implementation of events and actions",
    "associated with buttons.",
    "__________________",
    "Halley Rugama:",
    "Role: Responsible for the Import of Models and Sound",
    "Responsibilities:",
    "Import and adjustment of models in .obj format. ",
    "Implementation of proximity sound for animals.",
    "8D ambient sound integration.",
    "__________________",
    "Eliezer Acuña",
    "Role: Person in charge of the collision and animation",
    " of models",
    "Responsibilities:",
    "Management and optimization of the collision ",
    "between models.",
    "Development and improvement of ",
    "animations for models.",
    "___________________",
    "Benjamin Salguera:",
    "Role: Head of Lighting and Support in User Interface.",
    "Responsibilities:",
    "Application and adjustment of lighting in scenes.",
    "Collaboration in the development of the user interface, ",
    "including the creation of a soundbar."
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
    y_offset = 0  # Comienza desde la parte superior

    # Cargar imágenes de prueba
    texture_paths = ["SOFI.png", "Dai.png", "eliezer.png", "benja.png", "naturaleza.png"]
    textures = [load_texture(path) for path in texture_paths]

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        y = y_offset

        # Renderizar texto y posicionar imágenes
        for i, line in enumerate(credits):
            if line == "NATURENOOK":
                render_text(line, (display[0] // 2 - 140, y + 240), font_size=50, color=(30, 69, 65))  # Título grande y verde
            elif line.startswith("Description:"):
                render_text(line, (display[0] // 2 - 70, y + 220), font_size=24, color=(255, 255, 255))
                y -= 10  # Espacio mayor después de "Descripción:"
            else:
                render_text(line, (display[0] // 2 - 250, y + 200))

            if i == 10:  # Posicionar la primera imagen cerca de "Ana Ordoñez"
                render_texture(textures[0][0], (display[0] // 2 + 180, y +65), (130, 130))
            elif i == 11:  # Posicionar la segunda imagen cerca de "Halley Rugama:"
                render_texture(textures[1][0], (display[0] // 2 + 180, y -55), (130, 130))
            elif i == 12:  # Posicionar la tercera imagen cerca de "Eliezer Acuña"
                render_texture(textures[2][0], (display[0] // 2 + 180, y - 190), (130, 130))
            elif i == 13:  # Posicionar la cuarta imagen cerca de "Benjamin Salguera"
                render_texture(textures[3][0], (display[0] // 2 + 180, y - 330), (130, 130))

            y -= 20  # Espacio entre líneas

        y_offset += 2  # Mueve el texto hacia abajo

        if y_offset > display[1]:
            y_offset = -len(credits) * 60

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
