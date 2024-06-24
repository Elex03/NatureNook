from model import *
import glm
import random
from light import Light
from scene_renderer import SceneRenderer


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

        n, s = 50, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))

        n, s = 20, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                x_pos = x + random.uniform(0, 1)
                z_pos = z + random.uniform(0, 2)
                add(Grass(app, pos=(x_pos, -1, z_pos)))

        if self.app.var:
            self.app.moving_cube = MovingCube(app, pos=(7, 6, 7), scale=(3, 3, 3), tex_id=1)
            n, s = 30, 5
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
                add(Leaves(app, pos=(app.Position[i][0], -2, app.Position[i][1]), tex_id=random.choice(['leaf1', 'leaf2', 'leaf3', 'leaf4'])))

        if self.app.is_day:
            # Añadir el primer frame de Old_Lantern
            Old_Lantern_class = globals()['frame_1']
            self.old_lantern = Old_Lantern_class(app, pos=(0, 3, 0))
            add(self.old_lantern)
        else:
            Old_Latern_class = fireFly(app, pos=(0, 3, 0))
            add(Old_Latern_class)

    def update(self, pos):
        self.index = self.index + 1 if (self.index + 1) < 25 else 1

        if self.app.is_day:
            Old_Lantern_class = globals()[f'frame_{self.index}']
        else:
            Old_Latern_class = fireFly(self.app, pos=(0, 3, 0))


        # Calcular la nueva posición alrededor de la cámara
        radius = 1
        wave_amplitude = 0.5
        wave_frequency = 1
        offset = 1.5

        new_x = pos[0] + radius * glm.sin(self.app.time)
        new_z = pos[2] + radius * glm.cos(self.app.time)
        new_y = wave_amplitude * glm.sin(wave_frequency * self.app.time) + offset

        self.app.position_lamp = glm.vec3(new_x, new_y, new_z)

        if self.app.is_day:
            if self.old_lantern is not None:
                self.remove_object(self.old_lantern)

            # Crea y añade el nuevo objeto con la nueva posición
            self.old_lantern = Old_Lantern_class(self.app, pos=self.app.position_lamp)
            self.add_object(self.old_lantern)

            self.old_lantern.render()


        self.app.moving_cube.rot.xyz = self.app.time

        # Actualiza la lámpara móvil si es de noche
        if not self.app.is_day:
            self.app.light = Light(self.app, False, self.app.position_lamp)
            Scene(self.app)
            # Recargar renderer
            SceneRenderer(self.app)
