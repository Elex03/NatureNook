import pygame as pg
import moderngl as mgl
import sys
from button import Button
import time
import os


class GraphicEngine:
    def __init__(self, win_size=(800, 600)):
        pg.init()

        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.clock = pg.time.Clock()

        self.game_paused = True
        self.menu_state = "main"

        # Registro del tiempo de inicio
        self.start_time = time.time()

        self.font = pg.font.SysFont("arialblack", 40)
        self.TEXT_COL = (128, 128, 128)

        # Ruta de la carpeta de imágenes
        img_folder = 'C:\\Users\\HP\\Desktop\\proyecto\\NatureNook\\src\\Engine\\finished\\botton'
        # cambiar la ruta si se quiere usar.

        self.resume_img = pg.image.load(os.path.join(img_folder, "button_resume.png")).convert_alpha()
        self.options_img = pg.image.load(os.path.join(img_folder, "button_options.png")).convert_alpha()
        self.quit_img = pg.image.load(os.path.join(img_folder, "button_quit.png")).convert_alpha()
        self.video_img = pg.image.load(os.path.join(img_folder, 'button_video.png')).convert_alpha()
        self.audio_img = pg.image.load(os.path.join(img_folder, 'button_audio.png')).convert_alpha()
        self.keys_img = pg.image.load(os.path.join(img_folder, 'button_keys.png')).convert_alpha()
        self.back_img = pg.image.load(os.path.join(img_folder, 'button_back.png')).convert_alpha()

        self.resume_button = Button(304, 125, self.resume_img, 1)
        self.options_button = Button(297, 250, self.options_img, 1)
        self.quit_button = Button(336, 375, self.quit_img, 1)
        self.video_button = Button(226, 75, self.video_img, 1)
        self.audio_button = Button(225, 200, self.audio_img, 1)
        self.keys_button = Button(246, 325, self.keys_img, 1)
        self.back_button = Button(332, 450, self.back_img, 1)

        # Cargar imagen de fondo
        self.background_img = pg.image.load(os.path.join(img_folder, 'Logo.png')).convert()
        self.background_img = pg.transform.scale(self.background_img, self.WIN_SIZE)  # Redimensionar la imagen si es necesario

        self.set_mode()

    def set_mode(self):
        if self.game_paused:
            self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.RESIZABLE)
        else:
            self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen = pg.display.get_surface()
        screen.blit(img, (x, y))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_SPACE:
                    self.game_paused = not self.game_paused
                    self.set_mode()

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        # Aquí puedes agregar el código de renderizado de OpenGL
        pg.display.flip()

    def draw_menu(self):
        screen = pg.display.get_surface()

        # Dibujar imagen de fondo
        screen.blit(self.background_img, (0, 0))

        # Mostrar mensaje durante los primeros 3 segundos
        current_time = time.time()
        if current_time - self.start_time < 0:
            self.draw_text("hola mundo", self.font, self.TEXT_COL, 160, 250)
        else:
            if self.menu_state == "main":
                if self.resume_button.draw(screen):
                    self.game_paused = False
                    self.set_mode()  # Cambia el modo de pantalla al reanudar el juego
                if self.options_button.draw(screen):
                    self.menu_state = "options"
                if self.quit_button.draw(screen):
                    pg.quit()
                    sys.exit()
            elif self.menu_state == "options":
                if self.video_button.draw(screen):
                    print("Video Settings")
                if self.audio_button.draw(screen):
                    print("Audio Settings")
                if self.keys_button.draw(screen):
                    print("Change Key Bindings")
                if self.back_button.draw(screen):
                    self.menu_state = "main"

        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            if self.game_paused:
                self.draw_menu()
            else:
                self.render()
            self.clock.tick(60)


if __name__ == '__main__':
    app = GraphicEngine()
    app.run()



