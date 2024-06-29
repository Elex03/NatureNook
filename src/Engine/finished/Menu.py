import sys
import pygame as pg
import time
from Slider import Slider
from switch import Switch

class Menu:
    def __init__(self, font, text_color, button_manager, background_img):
        self.font = font
        self.text_color = text_color
        self.button_manager = button_manager
        self.background_img = background_img
        self.menu_state = "main"
        self.start_time = time.time()
        self.mouse_selected_button = None

        # Initialize slider for audio settings
        self.volume_slider = Slider(150, 250, 500, 20, 0, 100, 50)

        # Initialize switch for additional functionality
        self.some_switch = Switch(360, 300, 60, 30)

        # Create a transparent surface
        self.surface = pg.Surface((800, 600), pg.SRCALPHA)

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.text_color)
        screen = pg.display.get_surface()
        screen.blit(img, (x, y))

    def draw_menu(self):
        screen = pg.display.get_surface()
        # Fill the surface with a semi-transparent color
        self.surface.fill((0, 0, 0, 128))
        screen.blit(self.background_img, (0, 0))
        current_time = time.time()
        if self.menu_state == "audio":
            self.volume_slider.draw(self.surface)
            self.some_switch.draw(self.surface)
            self.button_manager.draw_buttons(self.surface, self.menu_state)  # Draw audio menu buttons, including "back"
            self.draw_text(f"Sound", 325, 190)
        elif current_time - self.start_time < 0:
            self.draw_text("Press P to pause", 160, 250)
        else:
            self.button_manager.draw_buttons(self.surface, self.menu_state)
        screen.blit(self.surface, (0, 0))
        pg.display.flip()

        return self.menu_state  # Ensure to return the menu state

    def handle_selection(self, input_type='keyboard'):
        if input_type == 'mouse':
            selected_button = self.mouse_selected_button
        else:
            selected_button = self.button_manager.get_selected_button(self.menu_state)

        if selected_button == "resume":
            self.menu_state = "main"
            return "resume"
        elif selected_button == "options":
            self.open_new_window()
        elif selected_button == "quit":
            pg.quit()
            sys.exit()
        elif selected_button == "video":
            print("Video Settings")
        elif selected_button == "audio":
            self.menu_state = "audio"
        elif selected_button == "keys":
            print("Change Key Bindings")
        elif selected_button == "back":
            self.menu_state = "main"
        return "main"

    def open_new_window(self):
        print("Nueva ventana abierta")

    def handle_event(self, event):
        self.button_manager.handle_event(event, self.menu_state)
        if self.menu_state == "audio":
            self.volume_slider.handle_event(event)
            self.some_switch.handle_event(event)
            volume = self.volume_slider.get_value() / 100
            pg.mixer.music.set_volume(volume)

    def adjust_volume_continuously(self):
        keys = pg.key.get_pressed()
        if self.menu_state == "audio":
            if keys[pg.K_a]:
                self.volume_slider.adjust_value(-1)
                volume = self.volume_slider.get_value() / 100
                pg.mixer.music.set_volume(volume)
            if keys[pg.K_d]:
                self.volume_slider.adjust_value(1)
                volume = self.volume_slider.get_value() / 100
                pg.mixer.music.set_volume(volume)
