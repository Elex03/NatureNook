import pygame as pg
import os

class ImageLoader:
    def __init__(self, img_folder):
        self.img_folder = img_folder

    def load_image(self, filename):
        return pg.image.load(os.path.join(self.img_folder, filename)).convert_alpha()

    def load_background(self, filename, win_size):
        img = pg.image.load(os.path.join(self.img_folder, filename)).convert()
        return pg.transform.scale(img, win_size)

