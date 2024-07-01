# button.py

import pygame as pg

class Button:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pg.Rect(x, y, width, height)
        try:
            self.image = pg.image.load(image_path).convert_alpha()
        except Exception as e:
            print(f"Error loading image from '{image_path}': {e}")
            raise
        self.image = pg.transform.scale(self.image, (width, height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        # Dibujar un borde rojo alrededor del botón
        pg.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
