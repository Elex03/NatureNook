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
        self.index2 = 10  # Inicializa el índice2 de la animación 2
        self.index_Fox = 1
        self.index_Bird = 1
        self.old_lantern = None
        self.Rain = None
        self.second_lantern = None  # Añadido para la segunda linterna
        self.Fox = None
        n = 10
        self.array = [{'water': None, 'y_rain': random.uniform(10, 15), 'x_rain': x, 'z_rain': z}
                      for x in range(-n, n+1) for z in range(-n, n+1)]
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

        add(rock(app, pos=(0, -1, 0)))

        if self.app.var:
            self.app.moving_cube = MovingCube(app, pos=(7, 6, 7), scale=(3, 3, 3), tex_id=1)
            self.app.moving_lamp = fireFly(app, pos=self.app.position_lamp, scale=(1, 1, 1))

            n, s = 20, 2
            for x in range(-n, n, s):
                for z in range(-n, n, s):
                    x_pos = x + random.uniform(0, 1)
                    z_pos = z + random.uniform(0, 2)
                    self.app.position_grass.append((x_pos, z_pos))
                    add(Grass(app, pos=(x_pos, -1, z_pos)))

            n, s = 30, 5
            for x in range(-n, n, s):
                for z in range(-n, n, s):
                    if z == 0 and x == 0:
                        continue
                    else:
                        random_leaf = random.choice(['leaf1', 'leaf2', 'leaf3', 'leaf4'])
                        random_trunk = "TrunkPine" if random_leaf == 'leaf4' else 'Trunk'
                        x_pos = x + random.uniform(0, 1)
                        z_pos = z + random.uniform(0, 2)
                        add(Trunk(app, pos=(x_pos, -2, z_pos), tex_id=random_trunk))
                        add(Leaves(app, pos=(x_pos, -2, z_pos), tex_id=random_leaf))
                        self.app.Position.append((x_pos, z_pos))
            self.app.var = False
        else:
            for i in range(0, len(app.Position)):
                add(Trunk(app, pos=(app.Position[i][0], -2, app.Position[i][1])))
                add(Leaves(app, pos=(app.Position[i][0], -2, app.Position[i][1]),
                           tex_id=random.choice(['leaf1', 'leaf2', 'leaf3', 'leaf4'])))
            for i in range(0, len(app.position_grass)):
                add(Grass(app, pos=(app.position_grass[i][0], -1, app.position_grass[i][1])))

        if self.app.is_day:
            # Añadir el primer frame de Old_Lantern
            Old_Lantern_class = globals()['frame_1']
            Old_Lantern_class1 = globals()['frame_1']
            Fox = globals()['Fox_1']
            Bird = globals()['Bird_1']
            self.old_lantern = Old_Lantern_class(app, pos=(0, 3, 0), tex_id='frame_1')
            self.old_lantern1 = Old_Lantern_class1(app, pos=(0, 3, 0), tex_id='frame_2')
            self.bird = Bird(app, pos=(0, -1, 0), tex_id='bird')
            self.Fox = Fox(app, pos=(0, 2, 0))
            add(self.old_lantern)
            add(self.old_lantern1)
            add(self.Fox)
            add(self.bird)

        else:
            add(self.app.moving_lamp)

    def update(self, pos):
        global Old_Lantern_class, Old_Lantern_class1, Fox_animation, Bird_animation
        self.index = self.index + 1 if (self.index + 1) < 25 else 1
        self.index2 = self.index2 + 1 if (self.index2 + 1) < 25 else 1
        self.index_Fox = self.index_Fox + 1 if (self.index_Fox + 1) < 15 else 1
        self.index_Bird = self.index_Bird + 1 if (self.index_Bird + 1) < 104 else 1
        self.rain()
        if self.app.is_day:
            Old_Lantern_class = globals()[f'frame_{self.index}']
            Old_Lantern_class1 = globals()[f'frame_{self.index2}']
            Fox_animation = globals()[f'Fox_{self.index_Fox}']
            Bird_animation = globals()[f'Bird_{self.index_Bird}']

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
            if self.second_lantern is not None:
                self.remove_object(self.second_lantern)
            if self.Fox is not None:
                self.remove_object(self.Fox)
            if self.bird is not None:
                self.remove_object(self.bird)

            # Crea y añade el nuevo objeto con la nueva posición
            self.old_lantern = Old_Lantern_class(self.app, pos=self.app.position_lamp, tex_id='frame_1')
            self.second_lantern = Old_Lantern_class1(self.app, pos=self.app.position_lamp + glm.vec3(0.5, 0.2, 0.2),
                                                     tex_id='frame_2')
            self.bird = Bird_animation(self.app, pos=(0, -0.9, 0), tex_id='bird')
            if self.app.bool_fox:
                if self.app.position_fox[0] < 12.5:
                    self.app.position_fox[0] += 0.2
                    self.app.rot_fox = 280
                else:
                    if self.app.position_fox[2] < 12.5:
                        self.app.position_fox[2] += 0.2
                        self.app.rot_fox = 180
                    else:
                        self.app.bool_fox = False
            else:
                if (self.app.position_fox[0] - 0.2) > -12.5:
                    self.app.position_fox[0] -= 0.2
                    self.app.rot_fox = 90
                else:
                    if (self.app.position_fox[2] - 0.2) > -12.5:
                        self.app.position_fox[2] -= 0.2
                        self.app.rot_fox = 0
                    else:
                        self.app.bool_fox = True

            self.Fox = Fox_animation(self.app, pos=self.app.position_fox, rot=(0, self.app.rot_fox, 0))

            self.add_object(self.old_lantern)
            self.add_object(self.second_lantern)
            self.add_object(self.bird)
            self.add_object(self.Fox)

            self.old_lantern.render()
            self.second_lantern.render()
            self.Fox.render()
            self.bird.render()
        else:
            self.app.moving_lamp.pos = self.app.position_lamp

        # Actualiza la lámpara móvil si es de noche
        if not self.app.is_day:
            self.app.light = Light(self.app, False, self.app.position_lamp)
            Scene(self.app)
            # Recargar renderer
            SceneRenderer(self.app)

    def rain(self):
        add = self.add_object

        for item in self.array:
            # Aplicar las operaciones específicas para cada elemento
            item['y_rain'] = item['y_rain'] - 0.3 if item['y_rain'] > 0 else random.uniform(10, 5)

            # Suponer que tenemos métodos y atributos definidos para self.app y Water

            if 'Rain' in item and item['Rain'] is not None:
                self.remove_object(item['Rain'])

            item['Rain'] = Water(self.app, pos=(item['x_rain'], item['y_rain'], item['z_rain']))
            add(item['Rain'])
