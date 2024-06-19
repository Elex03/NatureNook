import sys
import pygame as pg
import time
from Slider import Slider

class Menu:
    def __init__(self, font, text_color, button_manager, background_img):
        self.font = font
        self.text_color = text_color
        self.button_manager = button_manager
        self.background_img = background_img
        self.menu_state = "main"
        self.start_time = time.time()

        # Initialize slider for audio settings
        self.volume_slider = Slider(150, 250, 500, 20, 0, 100, 50) #volumen configuracion basg

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.text_color)
        screen = pg.display.get_surface()
        screen.blit(img, (x, y))

    def draw_menu(self):
        screen = pg.display.get_surface()
        screen.blit(self.background_img, (0, 0))
        current_time = time.time()
        if current_time - self.start_time < 0:
            self.draw_text("Press SPACE to pause", 160, 250)
        else:
            self.button_manager.draw_buttons(screen, self.menu_state)
            if self.menu_state == "audio":
                self.draw_text("Sound", 320, 120)  # Draw the "Sound" text above the slider
                self.volume_slider.draw(screen)
                self.button_manager.create_button("back", 150, 350, "button_back.png", 1, "audio")
                self.button_manager.draw_buttons(screen, "audio")  # Draw the "Back" button
        pg.display.flip()
        return self.menu_state

    def handle_selection(self, input_type='keyboard'):
        if input_type == 'mouse':
            selected_button = self.mouse_selected_button
        else:
            selected_button = self.button_manager.get_selected_button(self.menu_state)

        if selected_button == "resume":
            return "resume"
        elif selected_button == "options":
            self.menu_state = "options"
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
            if self.menu_state == "audio":
                self.menu_state = "options"
            else:
                self.menu_state = "main"
        return "main"

    def handle_event(self, event):
        self.button_manager.handle_event(event, self.menu_state)
        if self.menu_state == "audio":
            self.volume_slider.handle_event(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    self.volume_slider.adjust_value(-1)
                elif event.key == pg.K_d:
                    self.volume_slider.adjust_value(1)
                elif event.key == pg.K_b:  # Handle 'b' key to go back
                    self.menu_state = "options"
            # Set the volume of the sounds in your program
            volume = self.volume_slider.get_value() / 100
            pg.mixer.music.set_volume(volume)
