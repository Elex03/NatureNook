from button import Button

class ButtonManager:
    def __init__(self, image_loader):
        self.image_loader = image_loader
        self.buttons = {}

    def create_button(self, name, x, y, img_name, scale):
        img = self.image_loader.load_image(img_name)
        self.buttons[name] = Button(x, y, img, scale)

    def draw_button(self, name, surface):
        if name in self.buttons:
            return self.buttons[name].draw(surface)
        return False
