import pygame as pg

class Switch:
    def __init__(self, x, y, width, height, initial_state=False, engine=None):
        self.rect = pg.Rect(x, y, width, height)
        self.state = initial_state
        self.font = pg.font.SysFont(None, 24)
        self.on_color = (0, 200, 0)
        self.off_color = (200, 200, 200)
        self.knob_color = (255, 255, 255)
        self.knob_radius = height // 2 - 2
        self.border_color = (100, 100, 100)
        self.on_text = self.font.render('ON', True, (255, 255, 255))
        self.off_text = self.font.render('OFF', True, (255, 255, 255))
        self.animation_speed = 10
        self.current_x = x if not initial_state else x + width - height
        self.engine = engine  # Referencia a la instancia de GraphicsEngine

    def draw(self, screen):
        # Draw the switch background with rounded corners
        pg.draw.rect(screen, self.on_color if self.state else self.off_color, self.rect, border_radius=self.knob_radius)

        # Draw the knob with border
        knob_x = self.rect.x + (self.rect.width - self.rect.height if self.state else 0)
        knob_rect = pg.Rect(knob_x + 2, self.rect.y + 2, self.rect.height - 4, self.rect.height - 4)
        pg.draw.ellipse(screen, self.knob_color, knob_rect)
        pg.draw.ellipse(screen, self.border_color, knob_rect, 2)

        # Draw the text
        if self.state:
            screen.blit(self.on_text, (self.rect.x + 10, self.rect.y + 7))  # Ajustar la posición del texto ON
        else:
            screen.blit(self.off_text, (self.rect.x + 15, self.rect.y + 7))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                self.target_x = self.rect.x if not self.state else self.rect.x + self.rect.width - self.rect.height

                # Cambiar el skybox según el estado del switch
                if self.engine:
                    self.engine.set_skybox(self.state)

    def update(self):
        if hasattr(self, 'target_x'):
            if self.state and self.current_x < self.target_x:
                self.current_x += self.animation_speed
                if self.current_x > self.target_x:
                    self.current_x = self.target_x
            elif not self.state and self.current_x > self.target_x:
                self.current_x -= self.animation_speed
                if self.current_x < self.target_x:
                    self.current_x = self.target_x

    def get_state(self):
        return self.state
