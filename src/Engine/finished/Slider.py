import pygame as pg

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pg.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.sliding = False

    def draw(self, surface):
        # Draw the slider background
        pg.draw.rect(surface, (255, 255, 255), self.rect)
        # Draw the filled part of the slider
        filled_rect = pg.Rect(self.rect.x, self.rect.y, (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.w, self.rect.h)
        pg.draw.rect(surface, (0, 255, 255), filled_rect)
        # Draw the slider knob
        knob_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.w
        pg.draw.circle(surface, (0, 0, 0), (int(knob_x), self.rect.centery), self.rect.h // 2)

        # Draw the percentage text
        font = pg.font.SysFont("arialblack", 20)
        text_surface = font.render(f"{int(self.val)}%", True, (255, 255, 255))
        surface.blit(text_surface, (self.rect.x + self.rect.w + 10, self.rect.y))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.sliding = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.sliding = False
        elif event.type == pg.MOUSEMOTION:
            if self.sliding:
                rel_x = event.pos[0] - self.rect.x
                self.val = (rel_x / self.rect.w) * (self.max_val - self.min_val) + self.min_val
                self.val = max(self.min_val, min(self.max_val, self.val))

    def get_value(self):
        return self.val

    def adjust_value(self, amount):
        self.val += amount
        self.val = max(self.min_val, min(self.max_val, self.val))
