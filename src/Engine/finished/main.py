import pygame as pg
import moderngl as mgl
import sys
from ImageLoader import ImageLoader
from ButtonManager import ButtonManager
from Menu import Menu
from ButtonCreator import ButtonCreator
from EventChecker import EventChecker

class GraphicEngine:
    def __init__(self, win_size=(800, 600)):
        pg.init()
        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.clock = pg.time.Clock()
        self.game_paused = True

        # Initialize ImageLoader
        img_folder = r'C:\Users\HP\Desktop\proyecto\NatureNook\src\Engine\finished\botton'
        self.image_loader = ImageLoader(img_folder)

        # Initialize ButtonManager and create buttons
        self.button_manager = ButtonManager(self.image_loader)
        self.button_creator = ButtonCreator(self.button_manager)
        self.button_creator.create_buttons()

        # Initialize Menu
        font = pg.font.SysFont("arialblack", 40)
        text_color = (128, 128, 128)
        background_img = self.image_loader.load_background('Logo.png', self.WIN_SIZE)
        self.menu = Menu(font, text_color, self.button_manager, background_img)

        # Initialize EventChecker
        self.event_checker = EventChecker(self.menu, self.button_manager, self)

        self.set_mode()

    def set_mode(self):
        if self.game_paused:
            self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.RESIZABLE)
        else:
            self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

    def adjust_volume_continuously(self):
        keys = pg.key.get_pressed()
        if self.menu.menu_state == "audio":
            if keys[pg.K_a]:
                self.menu.volume_slider.adjust_value(-1)
                volume = self.menu.volume_slider.get_value() / 100
                pg.mixer.music.set_volume(volume)
                print(f"Volume: {self.menu.volume_slider.get_value()}%")
            if keys[pg.K_d]:
                self.menu.volume_slider.adjust_value(1)
                volume = self.menu.volume_slider.get_value() / 100
                pg.mixer.music.set_volume(volume)
                print(f"Volume: {self.menu.volume_slider.get_value()}%")

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        pg.display.flip()

    def run(self):
        while True:
            self.event_checker.check_events()  # Use EventChecker to handle events
            self.adjust_volume_continuously()  # Adjust volume continuously based on key presses
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
