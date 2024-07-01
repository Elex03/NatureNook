import pygame as pg


class Control:
    def __init__(self, app):
        clock = pg.time.Clock()
        pg.joystick.init()
        joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

        if joysticks:
            for joystick in joysticks:
                joystick.init()
                print(f'Joystick conectado: {joystick.get_name()}')
                self.joystick = joysticks[0]
        else:
            print('No hay controles conectados.')

    def vibration(self):
        if hasattr(self.joystick, 'rumble'):
            self.joystick.rumble(1, 1, 100)
        else:
            print('El control no soporta rumble.')

