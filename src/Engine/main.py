import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from button import Button

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
        self.button = Button(10, 10, 150, 50, 'resources/textures/button_image2.png')
        self.isPause = False

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

        # Handle other events as needed
        # ...

    def render_Menu(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))  # Clear the background

        # Render menu elements
        self.button.draw(pg.display.get_surface())

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
