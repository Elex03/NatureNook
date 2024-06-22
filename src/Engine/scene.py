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
            n, s = 30, 5
            for x in range(-n, n, s):
                for z in range(-n, n, s):
                    x_pos = x + random.uniform(0, 1)
                    z_pos = z + random.uniform(0, 2)
                    add(Trunk(app, pos=(x_pos, -2, z_pos)))
                    add(Leaves(app, pos=(x_pos, -2, z_pos)))
                    self.app.Position.append((x_pos, z_pos))
        else:
            for i in range(0, len(app.Position)):
                add(Trunk(app, pos=(app.Position[i][0], -2, app.Position[i][1])))
                add(Leaves(app, pos=(app.Position[i][0], -2, app.Position[i][1])))

            
        add(self.app.moving_cube)
        add(self.app.moving_lampare)



    def update(self, pos):
        self.app.moving_cube.rot.xyz = self.app.time
        radius = 2
        wave_amplitude = 1
        wave_frequency = 1
        # self.app.moving_lampare.pos = glm.vec3(pos[0] + 1, pos[1] - 1, pos[2] - 1)
        new_x = pos[0] + 1 * glm.sin(self.app.time)
        new_z = pos[2] + 1 * glm.cos(self.app.time)
        new_y = wave_amplitude * glm.sin(wave_frequency * self.app.time) + 1  # Adding 1 to keep it above the ground

        self.app.moving_lampare.pos = (new_x, new_y, new_z)

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