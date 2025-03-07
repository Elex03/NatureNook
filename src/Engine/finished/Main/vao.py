from src.Engine.finished.Main.vbo import VBO
from src.Engine.finished.Main.shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # Crear los VAOs para cada objeto y su sombra
        self.create_vaos()

    def create_vaos(self):
        vao_definitions = [
            ('cube', 'default', 'cube'),
            ('shadow_cube', 'shadow_map', 'cube'),
            ('trunk', 'default', 'trunk'),
            ('shadow_trunk', 'shadow_map', 'trunk'),
            ('leaves', 'default', 'leaves'),
            ('shadow_leaves', 'shadow_map', 'leaves'),
            ('grass', 'default', 'grass'),
            ('shadow_grass', 'shadow_map', 'grass'),
            ('flower', 'default', 'flower'),
            ('shadow_flower', 'shadow_map', 'flower'),
            ('fireFly', 'default', 'fireFly'),
            ('shadow_fireFly', 'shadow_map', 'fireFly'),
            ('rock', 'default', 'rock'),
            ('shadow_rock', 'shadow_map', 'rock'),
            ('radio', 'default', 'radio'),
            ('shadow_radio', 'shadow_map', 'radio'),
            ('cabin', 'default', 'cabin'),
            ('shadow_cabin', 'shadow_map', 'cabin'),
            ('deer', 'default', 'deer'),
            ('shadow_deer', 'shadow_map', 'deer'),
            ('bodyM', 'default', 'bodyM'),
            ('shadow_bodyM', 'shadow_map', 'bodyM'),
            ('cupM', 'default', 'cupM'),
            ('shadow_cupM', 'shadow_map', 'cupM'),
            ('water', 'default', 'water'),
            ('shadow_water', 'shadow_map', 'water'),
            ('waterSplash', 'default', 'waterSplash'),
            ('shadow_waterSplash', 'shadow_map', 'waterSplash'),
            ('skybox', 'skybox', 'skybox'),
            ('advanced_skybox', 'advanced_skybox', 'advanced_skybox'),
        ]

        for i in range(1, 26):
            frame_name = f'frame_{i}'
            vao_definitions.append((frame_name, 'default', frame_name))
            vao_definitions.append((f'shadow_{frame_name}', 'shadow_map', frame_name))

        for i in range(1, 15):
            frame_name = f'Fox_{i}'
            vao_definitions.append((frame_name, 'default', frame_name))
            vao_definitions.append((f'shadow_{frame_name}', 'shadow_map', frame_name))

        for i in range(1, 104):
            frame_name = f'Bird_{i}'
            vao_definitions.append((frame_name, 'default', frame_name))
            vao_definitions.append((f'shadow_{frame_name}', 'shadow_map', frame_name))

        for i in range(1, 109):
            frame_name = f'deer_({i})'
            vao_definitions.append((frame_name, 'default', frame_name))
            vao_definitions.append((f'shadow_{frame_name}', 'shadow_map', frame_name))

        for i in range(1, 240):
            frame_name = f'Bee_({i})'
            vao_definitions.append((frame_name, 'default', frame_name))
            vao_definitions.append((f'shadow_{frame_name}', 'shadow_map', frame_name))

        for vao_name, program_name, vbo_name in vao_definitions:
            self.vaos[vao_name] = self.get_vao(
                program=self.program.programs[program_name],
                vbo=self.vbo.vbos[vbo_name]
            )

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()