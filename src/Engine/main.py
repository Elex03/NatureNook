import time
import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer

pg.init()
pg.mixer.init()


class GraphicsEngine:
    def __init__(self, win_size=(840, 480)):
        # window size
        self.WIN_SIZE = win_size
        # skybox change state
        self.scene_skybox = ('Skybox2', 'skybox1')
        # init pygame modules
        pg.init()
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF | pg.SRCALPHA)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self.ctx.front_face = 'ccw'  # 'ccw' means counter-clockwise, which is the default
        self.ctx.cull_face = 'back'  # Cull back faces (default)
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # color of the light
        self.color = [(1, 1, 1), (0.145,0.157,0.314),(0.961,0.588,0.133)]
        # camera
        self.is_day = True
        self.isStatic = True
        self.camera = Camera(self)
        self.position_camera = self.camera.position
        # light
        self.light = Light(self, True, (50, 50, -10))
        # Array
        self.Position = []
        # scene
        self.var = True
        # mesh
        self.mesh = Mesh(self)
        self.position_lamp = (0, 0, 0)
        self.position_fox = [0, -1, 0]
        self.position_grass = []
        self.rot_fox = 0
        self.bool_fox = True
        self.scene = Scene(self)
        # renderer
        self.scene_renderer = SceneRenderer(self)
        # rain
        self.isRain = False
        self.isMoon = False

    def check_events(self):
        for event in pg.event.get():
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                self.isRain = not self.isRain
            if event.type == pg.KEYDOWN and event.key == pg.K_o:
                self.isStatic = not self.isStatic


    def render(self):
        # clear frame buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene_renderer.render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.scene.update(app.position_camera)
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
