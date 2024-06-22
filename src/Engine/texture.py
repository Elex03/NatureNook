import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.get_texture_skybox = app.scene_skybox[0] if app.is_day else app.scene_skybox[1]
        self.textures = {
            1: self.get_texture(path='resources/models/textures/diamond_mineral.jpg'),
            0: self.get_texture(path='resources/models/textures/grass1.jpg'),
            'trunk': self.get_texture(path='resources/models/textures/Trunk.jpg'),
            'Old_Lantern': self.get_texture(path='resources/models/textures/Lantern_baseColor.jpeg'),
            'leaves': self.get_texture(path='resources/models/textures/leaf.jpg'),
            'grass': {
                2: self.get_texture(path='resources/models/textures/grass_2.png'),
                1: self.get_texture(path='resources/models/textures/grass_1.png'),
                0: self.get_texture(path='resources/models/textures/grass.png')
            },
            'skybox': self.get_texture_cube(dir_path='resources/textures/' + self.get_texture_skybox + '/', ext='png'),
            'depth_texture': self.get_depth_texture()
        }

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom', 'back', 'front']
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert_alpha()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture_data = pg.image.tostring(texture, 'RGBA')
        texture = self.ctx.texture(size=texture.get_size(), components=4, data=texture_data)
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        for tex in self.textures.values():
            if isinstance(tex, dict):
                for sub_tex in tex.values():
                    sub_tex.release()
            else:
                tex.release()
