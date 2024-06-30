# main.py

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
        # window size
        self.WIN_SIZE = win_size
        # skybox change state
        self.scene_skybox = ('skybox2', 'skybox1')
        # init pygame modules
        pg.init()
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(True)  # Make the mouse visible for interaction
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # color of the light
        self.color = [(1, 1, 1), (0.145, 0.157, 0.314)]
        self.is_day = True
        # light
        self.light = Light(self)
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)
        # renderer
        self.scene_renderer = SceneRenderer(self)
        # sound
        self.sound_music = pg.mixer.Sound('resources/sounds/sound.mp3')

        # Create a button with an image
        self.button = Button(10, 10, 150, 50, 'resources/textures/button_image2.png')

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.button.is_clicked(event.pos):
                    # Button clicked, toggle day/night
                    self.is_day = not self.is_day
                    # reload light
                    self.light = Light(self)
                    # reload mesh
                    self.mesh.update()
                    # scene
                    self.scene = Scene(self)
                    # renderer
                    self.scene_renderer = SceneRenderer(self)

            pulsar = pg.key.get_pressed()
            if pulsar[pg.K_a] or pulsar[pg.K_s] or pulsar[pg.K_d] or pulsar[pg.K_w]:
                if not pg.mixer.Channel(0).get_busy():
                    print(self.sound_music.get_volume())
            else:
                sound.fadeout(500)


    def render(self):
        # clear frame buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene_renderer.render()

        # Render button
        self.button.draw(pg.display.get_surface())

        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.sound_music.play()
    app.run()
