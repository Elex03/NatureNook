from model import *
import glm
import random


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)
        self.Positions = app.Position

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        n, s = 30, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))

        if self.app.var:
            self.app.moving_lampare = Old_Lantern(app, pos=(0, 3, 0))
            self.app.moving_cube = MovingCube(app, pos=(7, 6, 7), scale=(3, 3, 3), tex_id=1)
            print('if you are true im going to sleep')
        add(self.app.moving_cube)
        add(self.app.moving_lampare)



    def update(self, pos):
        self.app.moving_cube.rot.xyz = self.app.time
        self.app.moving_lampare.pos = glm.vec3(pos[0] + 1, pos[1] - 1, pos[2] - 1)

'''

        n, s = 30, 4
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                x_pos = x + random.uniform(0, 1)
                z_pos = z + random.uniform(0, 2)
                add(Trunk(app, pos=(x_pos, -2, z_pos)))
                add(Leaves(app, pos=(x_pos, -2, z_pos)))
                self.app.Position.append((x_pos, z_pos))
'''