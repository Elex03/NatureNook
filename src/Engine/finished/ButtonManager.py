import pygame as pg
from button import Button  # Importa la clase Button desde el archivo button.py

class ButtonManager:
    def __init__(self, image_loader):
        self.image_loader = image_loader
        self.buttons = {}
        self.selected_index = 0

    def create_button(self, name, x, y, img_name, scale, menu):
        img = self.image_loader.load_image(img_name)
        if menu not in self.buttons:
            self.buttons[menu] = []
        self.buttons[menu].append(Button(x, y, img, scale, name))

    def draw_buttons(self, surface, menu):
        for i, button in enumerate(self.buttons.get(menu, [])):
            if i == self.selected_index:
                pg.draw.rect(surface, (255, 0, 0), button.rect.inflate(10, 10), 3)  # Inflar el rectángulo
            button.draw(surface)

    def move_selection_up(self, menu):
        self.selected_index = (self.selected_index - 1) % len(self.buttons.get(menu, []))

    def move_selection_down(self, menu):
        self.selected_index = (self.selected_index + 1) % len(self.buttons.get(menu, []))

    def get_selected_button(self, menu):
        if menu in self.buttons:
            return self.buttons[menu][self.selected_index].name
        return None

    def check_mouse_click(self, pos, menu):
        for button in self.buttons.get(menu, []):
            if button.rect.collidepoint(pos) and not button.clicked:
                button.clicked = True
                return button.name
        return None

    def reset_buttons(self):
        self.buttons = {}
        self.selected_index = 0

    def handle_event(self, event, menu):pass