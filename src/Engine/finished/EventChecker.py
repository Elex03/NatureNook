import sys
import pygame as pg

class EventChecker:
    def __init__(self, menu, button_manager, engine):
        self.menu = menu
        self.button_manager = button_manager
        self.engine = engine

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            #if event.type == pg.KEYDOWN:

              #  if event.key == pg.K_ESCAPE:
               #     pg.quit()
               #     sys.exit()
                if event.key == pg.K_SPACE:
                    self.engine.game_paused = not self.engine.game_paused
                    self.engine.set_mode()
                if event.key == pg.K_w:
                    self.menu.button_manager.move_selection_up(self.menu.menu_state)
                if event.key == pg.K_s:
                    self.menu.button_manager.move_selection_down(self.menu.menu_state)
                if event.key == pg.K_RETURN:
                    action = self.menu.handle_selection()
                    if action == "resume":
                        self.engine.game_paused = False
                        self.engine.set_mode()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo del mouse
                    pos = pg.mouse.get_pos()
                    selected_button = self.button_manager.check_mouse_click(pos, self.menu.menu_state)
                    if selected_button:
                        self.menu.mouse_selected_button = selected_button
                        action = self.menu.handle_selection(input_type='mouse')
                        if action == "resume":
                            self.engine.game_paused = False
                            self.engine.set_mode()
            self.menu.handle_event(event)
