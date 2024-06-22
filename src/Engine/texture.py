import pygame as pg
import moderngl as mgl
import glm


class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {1: self.get_texture(path='resources/models/textures/diamond_mineral.jpg'),
                         0: self.get_texture(path='resources/models/textures/grass1.jpg')}
        self.get_texture_skybox = app.scene_skybox[0] if app.is_day else app.scene_skybox[1]
        self.textures['trunk'] = self.get_texture(path='resources/models/textures/Trunk.jpg')
        self.textures['Old_Lantern'] = self.get_texture(path='resources/models/textures/Lantern_baseColor.jpeg')
        self.textures['leaves'] = self.get_texture(path='resources/models/textures/leaf.jpg')
        self.textures['grass'] = self.get_texture(path='resources/models/textures/grass.png')
        self.textures['skybox'] = self.get_texture_cube(dir_path='resources/textures/'+self.get_texture_skybox+'/', ext='png')
        self.textures['depth_texture'] = self.get_depth_texture()

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
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
        # Cargar la imagen con soporte para canal alfa
        texture = pg.image.load(path).convert_alpha()

        # Voltear la imagen en el eje y
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)

        # Convertir la imagen a una cadena de caracteres incluyendo el canal alfa ('RGBA')
        texture_data = pg.image.tostring(texture, 'RGBA')

        # Crear la textura con 4 componentes (RGBA)
        texture = self.ctx.texture(size=texture.get_size(), components=4, data=texture_data)

        # Generar mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        # Anisotropic filtering
        texture.anisotropy = 32.0

        return texture
    def destroy(self):
        [tex.release() for tex in self.textures.values()]
