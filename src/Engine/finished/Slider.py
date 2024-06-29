import pygame as pg


class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pg.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.sliding = False
        self.sound_updated = False  # Variable para controlar si se ha impreso el mensaje de actualización del sonido

    def draw(self, surface):
        # Calculate the position and dimensions for the filled part of the slider
        line_y = self.rect.y + self.rect.h // 2
        knob_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.w
        filled_width = knob_x - self.rect.x

        # Draw the slider line (background)
        pg.draw.line(surface, (200, 200, 200), (self.rect.x, line_y), (self.rect.x + self.rect.w, line_y), 5)

        # Draw the filled part of the slider
        filled_rect = pg.Rect(self.rect.x, line_y - 2, int(filled_width), 5)
        pg.draw.rect(surface, (0, 0, 255), filled_rect)

        # Draw outer white circle
        pg.draw.circle(surface, (255, 255, 255), (int(knob_x), line_y), self.rect.h // 2)
        # Draw inner blue circle
        pg.draw.circle(surface, (0, 0, 255), (int(knob_x), line_y), self.rect.h // 2 - 4)

        # Draw the percentage text
        font = pg.font.SysFont("arialblack", 20)
        text_surface = font.render(f"{int(self.val)}%", True, (255, 255, 255))
        surface.blit(text_surface, (self.rect.x + self.rect.w + 10, self.rect.y))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.sliding = True
                self.sound_updated = False
        elif event.type == pg.MOUSEBUTTONUP:
            if self.sliding and not self.sound_updated:
                print("Sound:", int(self.val))
                self.sound_updated = True
            self.sliding = False
        elif event.type == pg.MOUSEMOTION:
            if self.sliding:
                rel_x = event.pos[0] - self.rect.x
                self.val = (rel_x / self.rect.w) * (self.max_val - self.min_val) + self.min_val
                self.val = max(self.min_val, min(self.max_val, self.val))

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.adjust_value(-1)
            elif event.key == pg.K_d:
                self.adjust_value(1)

    def get_value(self):
        return self.val

    def adjust_value(self, amount):
        self.val += amount
        self.val = max(self.min_val, min(self.max_val, self.val))
        print("Sound:",
              int(self.val))