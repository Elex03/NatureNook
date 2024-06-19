import pygame as pg
import sys
import time

class Menu:
    def __init__(self, font, text_color, button_manager, background_img):
        self.font = font
        self.text_color = text_color
        self.button_manager = button_manager
        self.background_img = background_img
        self.menu_state = "main"
        self.start_time = time.time()

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.text_color)
        screen = pg.display.get_surface()
        screen.blit(img, (x, y))

    def draw_menu(self):
        screen = pg.display.get_surface()
        screen.blit(self.background_img, (0, 0))
        current_time = time.time()
        if current_time - self.start_time < 0.2:
            self.draw_text("", 160, 250)
        else:
            if self.menu_state == "main":
                if self.button_manager.draw_button("resume", screen):
                    return "resume"
                if self.button_manager.draw_button("options", screen):
                    self.menu_state = "options"
                if self.button_manager.draw_button("quit", screen):
                    pg.quit()
                    sys.exit()
            elif self.menu_state == "options":
                if self.button_manager.draw_button("video", screen):
                    print("Video Settings")
                if self.button_manager.draw_button("audio", screen):
                    print("Audio Settings")
                if self.button_manager.draw_button("keys", screen):
                    print("Change Key Bindings")
                if self.button_manager.draw_button("back", screen):
                    self.menu_state = "main"
        pg.display.flip()
        return "main"
