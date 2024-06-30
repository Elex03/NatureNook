import pygame as pg
import moderngl as mgl
from ImageLoader import ImageLoader
from ButtonManager import ButtonManager
from Menu import Menu
from ButtonCreator import ButtonCreator
from EventChecker import EventChecker

class GraphicEngine:
    def __init__(self, win_size=(800, 600)):
        pg.init()
        self.WIN_SIZE = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = None  # Inicializar el contexto de OpenGL como None
        self.clock = pg.time.Clock()
        self.game_paused = True  # Comenzar en modo pausa (menú)

        # Initialize ImageLoader
        img_folder = r'finished/botton/'
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

        # Create a transparent surface for the pause overlay
        self.overlay_surface = pg.Surface(self.WIN_SIZE, pg.SRCALPHA)

    def set_mode(self):
        if not self.game_paused:
            if not self.ctx:
                self.ctx = mgl.create_context()

    def render(self):
        if self.ctx:
            self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
            pg.display.flip()
        else:
            self.screen.fill((0, 0, 0))  # Clear the screen with black
            # Add any other rendering logic here if necessary
            if not self.game_paused:
                # Draw the game scene here
                self.screen.fill((0, 0, 0))  # This would be your game rendering logic

    def run(self):
        while True:
            self.event_checker.check_events()  # Use EventChecker to handle events
            if self.game_paused:
                # Render the game scene
                self.render()
                # Fill the overlay with a semi-transparent color
                self.overlay_surface.fill((0, 0, 0, 128))
                self.screen.blit(self.overlay_surface, (0, 0))
                # Draw the menu on top
                action = self.menu.draw_menu()
                self.menu.adjust_volume_continuously()  # Continuously adjust volume
                if action == "resume":
                    self.game_paused = False
                    self.set_mode()
            else:
                self.render()
            self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicEngine()
    app.run()
