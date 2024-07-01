from src.Engine.finished.Main.vao import VAO
from src.Engine.finished.Main.texture import Texture


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
