import glm
import random
from model import *
from light import Light
from scene_renderer import SceneRenderer


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self._pos = glm.vec3(pos)
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = glm.vec3(scale)
        self.m_model = self.get_model_matrix()
        self._tex_id = tex_id
        self._texture = None
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

        # Set initial texture
        self.set_texture(tex_id)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        self._pos = glm.vec3(new_pos)
        self.m_model = self.get_model_matrix()

    @property
    def tex_id(self):
        return self._tex_id

    @tex_id.setter
    def tex_id(self, new_tex_id):
        self._tex_id = new_tex_id
        self.set_texture(new_tex_id)

    def set_texture(self, tex_id):
        self._texture = self.app.mesh.texture.textures.get(tex_id)
        if self._texture is None:
            raise ValueError(f"Texture ID '{tex_id}' not found in textures dictionary")
        if isinstance(self._texture, dict):
            self._texture = self._texture[0]

    def update(self):
        pass

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self._pos)
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.shadow_program = None
        self.shadow_vao = None
        self.depth_texture = None
        self.on_init()

    def update(self):
        if self._texture:
            self._texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        self.program['m_view_light'].write(self.app.light.m_view_light)

    def update_shadow(self):
        if self.shadow_program:
            self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        if self.shadow_program and self.shadow_vao:
            self.update_shadow()
            self.shadow_vao.render()

    def on_init(self):
        try:
            self.program['m_view_light'].write(self.app.light.m_view_light)
            self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))

            texture_data = self.app.mesh.texture.textures.get(self.tex_id)
            if texture_data is None:
                raise ValueError(f"Texture ID '{self.tex_id}' not found in textures dictionary")

            if isinstance(texture_data, dict):
                self._texture = texture_data[0]
            else:
                self._texture = texture_data

            self.depth_texture = self.app.mesh.texture.textures['depth_texture']
            self.program['shadowMap'] = 1
            self.depth_texture.use(location=1)

            self.shadow_vao = self.app.mesh.vao.vaos.get('shadow_' + self.vao_name)
            if self.shadow_vao:
                self.shadow_program = self.shadow_vao.program
                self.shadow_program['m_proj'].write(self.camera.m_proj)
                self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
                self.shadow_program['m_model'].write(self.m_model)

            self.program['u_texture_0'] = 0
            if (self._texture):
                self._texture.use(location=0)

            self.program['m_proj'].write(self.camera.m_proj)
            self.program['m_view'].write(self.camera.m_view)
            self.program['m_model'].write(self.m_model)

            self.program['light.position'].write(self.app.light.position)
            self.program['light.Ia'].write(self.app.light.Ia)
            self.program['light.Id'].write(self.app.light.Id)
            self.program['light.Is'].write(self.app.light.Is)
        except KeyError as e:
            print(f"KeyError: {e}")
        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class MovingCube(Cube):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        self.m_model = self.get_model_matrix()
        super().update()


class Trunk(ExtendedBaseModel):
    def __init__(self, app, vao_name='trunk', tex_id='trunk',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


# Crear clases para cada frame de Old_Lantern
for i in range(1, 26):
    class_name = f'frame_{i}'
    vao_name = class_name

    def create_class(vao_name):
        return type(class_name, (ExtendedBaseModel,), {
            '__init__': lambda self, app, tex_id='frame_1', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1):
                ExtendedBaseModel.__init__(self, app, vao_name, tex_id, pos, rot, scale)
        })

    globals()[class_name] = create_class(vao_name)

for i in range(1, 15):
    class_name = f'Fox_{i}'
    vao_name = class_name

    def create_class(vao_name):
        return type(class_name, (ExtendedBaseModel,), {
            '__init__': lambda self, app, tex_id='Fox', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1):
                ExtendedBaseModel.__init__(self, app, vao_name, tex_id, pos, rot, scale)
        })


    globals()[class_name] = create_class(vao_name)
for i in range(1, 104):
    class_name = f'Bird_{i}'
    vao_name = class_name

    def create_class(vao_name):
        return type(class_name, (ExtendedBaseModel,), {
            '__init__': lambda self, app, tex_id='bird', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1):
                ExtendedBaseModel.__init__(self, app, vao_name, tex_id, pos, rot, scale)
        })

    globals()[class_name] = create_class(vao_name)
for i in range(1, 109):
    class_name = f'deer_({i})'
    vao_name = class_name

    def create_class(vao_name):
        return type(class_name, (ExtendedBaseModel,), {
            '__init__': lambda self, app, tex_id='deer', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1):
                ExtendedBaseModel.__init__(self, app, vao_name, tex_id, pos, rot, scale)
        })

    globals()[class_name] = create_class(vao_name)


class Leaves(ExtendedBaseModel):
    def __init__(self, app, vao_name='leaves', tex_id='leaves1',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Water(ExtendedBaseModel):
    def __init__(self, app, vao_name='water', tex_id='water',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class WaterSplash(ExtendedBaseModel):
    def __init__(self, app, vao_name='waterSplash', tex_id='water',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Grass(ExtendedBaseModel):
    def __init__(self, app, vao_name='grass', tex_id='grass',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class fireFly(ExtendedBaseModel):
    def __init__(self, app, vao_name='fireFly', tex_id='fireFly',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class rock(ExtendedBaseModel):
    def __init__(self, app, vao_name='rock', tex_id='rock',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self._texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self._texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self._texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self._texture.use(location=0)
