import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from Slider import Slider
from switch import Switch

pg.init()
pg.mixer.init()

sound = pg.mixer.Sound('resources/sounds/a.wav')

class GraphicsEngine:
    def __init__(self, win_size=(630, 480)):
        self.WIN_SIZE = win_size
        self.scene_skybox = ('skybox2', 'skybox1')

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # Create the Pygame window
        pg.display.set_mode(self.WIN_SIZE, flags=pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.color = [(1, 1, 1), (0.145, 0.157, 0.314)]
        self.is_day = True

        self.light = Light(self)
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

        self.sound_music = pg.mixer.Sound('resources/sounds/sound.mp3')
        self.isPause = False

        self.slider = Slider(200, 200, 200, 20, 0, 100, 50)
        self.switch = Switch(280, 250, 60, 30)

        self.show_slider_and_switch = True  # Mostrar el slider y el switch por defecto

        self.cursor_index = 0  # Índice del cursor para señalar el elemento actual (0: slider, 1: switch)
        self.holding_a = False
        self.holding_d = False

        self.font = pg.font.SysFont("arialblack", 24)  # Crear una fuente para el texto de pausa

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.isPause = not self.isPause
                pg.mouse.set_visible(1)  # Show mouse when paused
                if self.isPause:
                    pg.display.set_mode(self.WIN_SIZE, flags=pg.RESIZABLE)
                else:
                    pg.mouse.set_visible(0)
                    GraphicsEngine()
            if event.type == pg.KEYDOWN:
                if self.show_slider_and_switch:
                    if event.key == pg.K_TAB:  # Cambiar entre el slider y el switch con TAB
                        self.cursor_index = (self.cursor_index + 1) % 2
                    if event.key == pg.K_a:
                        self.holding_a = True
                    if event.key == pg.K_d:
                        self.holding_d = True
                    if event.key == pg.K_w:
                        self.cursor_index = 0  # Mover el cursor al slider
                    if event.key == pg.K_s:
                        self.cursor_index = 1  # Mover el cursor al switch

            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    self.holding_a = False
                if event.key == pg.K_d:
                    self.holding_d = False

            if self.show_slider_and_switch:
                self.slider.handle_event(event)
                self.switch.handle_event(event)

    def update_slider_and_switch(self):
        if self.cursor_index == 0:  # Slider
            if self.holding_a:
                self.slider.adjust_value(-1)
            if self.holding_d:
                self.slider.adjust_value(1)
        elif self.cursor_index == 1:  # Switch
            if self.holding_a and self.switch.get_state():  # Si el switch está en ON
                self.switch.state = False
                print('OFF')
            if self.holding_d and not self.switch.get_state():  # Si el switch está en OFF
                self.switch.state = True
                print('ON')

    def render_Menu(self):
        surface = pg.display.get_surface()
        surface.fill((0, 0, 0))  # Clear the entire surface

        # Render the "Pause" text
        pause_text = self.font.render("Pause", True, (255, 255, 255))
        surface.blit(pause_text, (self.slider.rect.x + 70, self.slider.rect.y - 70))

        # Render menu elements
        self.slider.draw(surface)
        self.switch.draw(surface)

        # Dibujar el cursor alrededor del elemento actual
        if self.cursor_index == 0:  # Cursor en el slider
            pg.draw.rect(surface, (255, 0, 0), self.slider.rect.inflate(10, 10), 2)
        elif self.cursor_index == 1:  # Cursor en el switch
            pg.draw.rect(surface, (255, 0, 0), self.switch.rect.inflate(10, 10), 2)

        pg.display.flip()  # Update the display

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))  # Clear the background

        self.scene_renderer.render()  # Render the 3D scene

        pg.display.flip()  # Update the display

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.check_events()
            self.update_slider_and_switch()

            if not self.isPause:
                self.camera.update()
                self.render()
            else:
                self.render_Menu()

            self.get_time()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.sound_music.play()
    app.run()
