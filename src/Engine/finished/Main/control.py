import pygame as pg


class Control:
    def __init__(self):
        clock = pg.time.Clock()
        pg.joystick.init()
        self.joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

        if self.joysticks:
            for joystick in self.joysticks:
                joystick.init()
                print(f'Joystick conectado: {joystick.get_name()}')
                self.joystick = self.joysticks[0]
        else:
            print('No hay controles conectados.')

    def vibration(self):
        if self.joysticks:
            if hasattr(self.joystick, 'rumble'):
                self.joystick.rumble(1, 1, 100)
            else:
                print('El control no soporta rumble.')

