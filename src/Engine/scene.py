from model import *
import random

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.index = 1  # Inicializa el índice de la animación
        self.old_lantern = None
        self.load()
        # skyBox
        self.skyBox = AdvancedSkyBox(app)
        self.Positions = app.Position

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def load(self):
        app = self.app
        add = self.add_object

        n, s = 30, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))

        n, s = 30, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                x_pos = x + random.uniform(0, 1)
                z_pos = z + random.uniform(0, 2)
                # add(Grass(app, pos=(x_pos, -1, z_pos)))
        if self.app.var:
            self.app.moving_cube = MovingCube(app, pos=(7, 6, 7), scale=(3, 3, 3), tex_id=1)
            n, s = 25, 5
            for x in range(-n, n, s):
                for z in range(-n, n, s):
                    x_pos = x + random.uniform(0, 1)
                    z_pos = z + random.uniform(0, 2)
                    add(Trunk(app, pos=(x_pos, -2, z_pos)))
                    add(Leaves(app, pos=(x_pos, -2, z_pos), tex_id=random.choice(['leaf1', 'leaf2', 'leaf3', 'leaf4'])))
                    self.app.Position.append((x_pos, z_pos))
            self.app.var = False
        else:
            for i in range(0, len(app.Position)):
                add(Trunk(app, pos=(app.Position[i][0], -2, app.Position[i][1])))
                add(Leaves(app, pos=(app.Position[i][0], -2, app.Position[i][1]),
                           tex_id=random.choice(['leaf1', 'leaf2', 'leaf3', 'leaf4'])))

        # Añadir el primer frame de Old_Lantern
        Old_Lantern_class = globals()[f'frame_{self.index}']
        self.old_lantern = Old_Lantern_class(app, pos=(0, 0, 0))
        add(self.old_lantern)

    def update(self, pos):
        self.index = self.index + 1 if (self.index + 1) < 25 else 1
        print(self.index)
        Old_Lantern_class = globals()[f'frame_{self.index}']

        # Elimina el objeto antiguo
        if self.old_lantern is not None:
            self.remove_object(self.old_lantern)

        # Crea y añade el nuevo objeto
        self.old_lantern = Old_Lantern_class(self.app, pos=self.old_lantern.pos)
        self.add_object(self.old_lantern)

        self.old_lantern.render()
