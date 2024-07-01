from vao import VAO
from texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app)

    def update(self):
        self.texture = Texture(self.app)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()
