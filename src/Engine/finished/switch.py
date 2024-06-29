import pygame as pg

class Switch:
    def __init__(self, x, y, width, height, initial_state=False):
        self.rect = pg.Rect(x, y, width, height)
        self.state = initial_state
        self.font = pg.font.SysFont(None, 24)
        self.on_color = (0, 200, 0)
        self.off_color = (200, 200, 200)
        self.knob_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0, 50)  # Adding shadow color with transparency
        self.knob_radius = self.rect.height // 2 - 2  # Knob radius with a small padding
        self.knob_pos_on = self.rect.midright[0] - self.knob_radius - 2
        self.knob_pos_off = self.rect.midleft[0] + self.knob_radius + 2
        self.knob_pos = self.knob_pos_on if self.state else self.knob_pos_off
        self.on_text = self.font.render('ON', True, (255, 255, 255))
        self.off_text = self.font.render('OFF', True, (255, 255, 255))

    def draw(self, screen):
        # Draw the background with rounded corners
        bg_color = self.on_color if self.state else self.off_color
        pg.draw.rect(screen, bg_color, self.rect, border_radius=self.rect.height // 2)

        # Draw shadow for knob
        shadow_rect = pg.Rect(self.knob_pos - self.knob_radius, self.rect.centery - self.knob_radius, self.knob_radius * 2, self.knob_radius * 2)
        shadow_rect.inflate_ip(4, 4)
        pg.draw.ellipse(screen, self.shadow_color, shadow_rect)

        # Draw the knob
        knob_rect = pg.Rect(self.knob_pos - self.knob_radius, self.rect.centery - self.knob_radius, self.knob_radius * 2, self.knob_radius * 2)
        pg.draw.ellipse(screen, self.knob_color, knob_rect)

        # Draw the text
        if self.state:
            text = self.on_text
            text_rect = text.get_rect(center=(self.rect.right - text.get_width() // 2 - self.knob_radius - 10, self.rect.centery))
        else:
            text = self.off_text
            text_rect = text.get_rect(center=(self.rect.left + text.get_width() // 2 + self.knob_radius + 10, self.rect.centery))
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                print('ON' if self.state else 'OFF')
                self.knob_pos = self.knob_pos_on if self.state else self.knob_pos_off

    def get_state(self):
        return self.state