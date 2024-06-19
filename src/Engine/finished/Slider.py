import pygame as pg

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pg.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.sliding = False

    def draw(self, surface):
        # Draw the slider background (full bar)
        pg.draw.rect(surface, (255, 255, 255), self.rect)

        # Draw the filled part of the slider
        filled_rect = self.rect.copy()
        filled_rect.width = (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pg.draw.rect(surface, (0, 255, 255), filled_rect)  # Celeste color

        # Draw the slider knob (point)
        knob_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pg.draw.circle(surface, (0, 0, 0), (int(knob_x), self.rect.centery), self.rect.height // 2)  # Black color

        # Draw the percentage text on the slider
        font = pg.font.SysFont("arial", 18)
        percentage_text = f"{int(self.val)}%"
        text_surf = font.render(percentage_text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 20))
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.sliding = True
                self.update_value(event.pos[0])
        elif event.type == pg.MOUSEBUTTONUP:
            self.sliding = False
        elif event.type == pg.MOUSEMOTION:
            if self.sliding:
                self.update_value(event.pos[0])

    def update_value(self, pos_x):
        rel_x = pos_x - self.rect.x
        self.val = (rel_x / self.rect.width) * (self.max_val - self.min_val) + self.min_val
        self.val = max(self.min_val, min(self.max_val, self.val))
        print(f"Sound: {int(self.val)}%")

    def adjust_value(self, delta):
        self.val += delta
        self.val = max(self.min_val, min(self.max_val, self.val))
        print(f"Sound: {int(self.val)}%")

    def get_value(self):
        return self.val
