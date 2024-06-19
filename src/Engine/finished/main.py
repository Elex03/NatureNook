import pygame as pg
import moderngl as mgl
import sys
from ImageLoader import ImageLoader
from ButtonManager import ButtonManager
from Menu import Menu

class GraphicEngine:
    def __init__(self, win_size=(800, 600)):
        pg.init()
        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.clock = pg.time.Clock()
        self.game_paused = True

        # Initialize ImageLoader
        img_folder = 'botton/'
        self.image_loader = ImageLoader(img_folder)

        # Initialize ButtonManager and create buttons
        self.button_manager = ButtonManager(self.image_loader)
        self.button_manager.create_button("resume", 304, 125, "button_resume.png", 1)
        self.button_manager.create_button("options", 297, 250, "button_options.png", 1)
        self.button_manager.create_button("quit", 336, 375, "button_quit.png", 1)
        self.button_manager.create_button("video", 226, 75, "button_video.png", 1)
        self.button_manager.create_button("audio", 225, 200, "button_audio.png", 1)
        self.button_manager.create_button("keys", 246, 325, "button_keys.png", 1)
        self.button_manager.create_button("back", 332, 450, "button_back.png", 1)

        # Initialize Menu
        font = pg.font.SysFont("arialblack", 40)
        text_color = (128, 128, 128)
        background_img = self.image_loader.load_background('Logo.png', self.WIN_SIZE)
        self.menu = Menu(font, text_color, self.button_manager, background_img)

        self.set_mode()

    def set_mode(self):
        if self.game_paused:
            self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.RESIZABLE)
        else:
            self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

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
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            if self.game_paused:
                action = self.menu.draw_menu()
                if action == "resume":
                    self.game_paused = False
                    self.set_mode()
            else:
                self.render()
            self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicEngine()
    app.run()
