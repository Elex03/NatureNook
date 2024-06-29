import pygame as pg

class Switch:
    def __init__(self, x, y, width, height, initial_state=False):
        self.rect = pg.Rect(x, y, width, height)
        self.state = initial_state
        self.font = pg.font.SysFont(None, 24)
        self.on_color = (0, 200, 0)
        self.off_color = (200, 200, 200)
        self.knob_color = (255, 255, 255)
        self.on_text = self.font.render('ON', True, (255, 255, 255))
        self.off_text = self.font.render('OFF', True, (255, 255, 255))

    def draw(self, screen):
        if self.state:
            pg.draw.rect(screen, self.on_color, self.rect)
            pg.draw.circle(screen, self.knob_color, self.rect.midright, self.rect.height // 2.7)
            screen.blit(self.on_text, (self.rect.x + 17, self.rect.y + 7))
        else:
            pg.draw.rect(screen, self.off_color, self.rect)
            pg.draw.circle(screen, self.knob_color, self.rect.midleft, self.rect.height // 2.9)
            screen.blit(self.off_text, (self.rect.x + 15, self.rect.y + 7))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                print('ON' if self.state else 'OFF')

    def get_state(self):
        return self.state
