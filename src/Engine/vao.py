from vbo import VBO
from shader_program import ShaderProgram


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
            ('skybox', 'skybox', 'skybox'),
            ('advanced_skybox', 'advanced_skybox', 'advanced_skybox'),
        ]

        for i in range(1, 26):
            frame_name = f'frame_{i}'
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