import pygame as pg
import moderngl as mgl
import sys

#inicializar pygame
pg.init()
pg.mixer.init()
sound1 = pg.mixer.Sound('a.wav')
sound2 = pg.mixer.Sound('grillos.wav')
class GraphicEngine:
    def __init__(self, win_size=(600, 300)):
        self.WIN_SIZE = win_size
        # set opengl attribute
        pg.display.gl_get_attribute(pg.GL_CONTEXT_MAJOR_VERSION)
        pg.display.gl_get_attribute(pg.GL_CONTEXT_MINOR_VERSION)
        pg.display.gl_get_attribute(pg.GL_CONTEXT_PROFILE_MASK)
        # create opengl Context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        #create an object to help track the time
        self.clock = pg.time.Clock()

    def play_sounds(self):
        sound1.play()
        sound2.play()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.type == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            pulsada = pg.key.get_pressed()
            if pulsada[pg.K_n]:
                if pg.mixer.Channel(0).get_busy() == False:
                    self.play_sounds()

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1))
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.render()
            self.clock.tick(60)


if __name__ == '__main__':
    app = GraphicEngine()
    app.run()