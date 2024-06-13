
class Collisions:
    def _init_(self, app):
        self.app = app
        self.positions_models = (7, 7)
        self.limits = (5, -5)

    def check_limits(self):
        print(self.app.position)
        bool_x1 = self.positions_models[0] + self.limits[0] > self.app.x > self.positions_models[0] - self.limits[0]
        bool_x2 = self.positions_models[1] + self.limits[0] > self.app.x > self.positions_models[1] - self.limits[0]

        bool_z1 = self.positions_models[0] + self.limits[1] < self.app.z < self.positions_models[0] - self.limits[1]
        bool_z2 = self.positions_models[1] + self.limits[1] < self.app.z < self.positions_models[1] - self.limits[1]
        if (bool_x1 and bool_x2) and (bool_z1 and bool_z2):
            return False
        else:
            return True

        # we use this because we need reduce the for

    '''
        quadrant_position = (True, True) if self.app.position[0] > 0 and self.app.position[2] > 0 else (False, True) if \
            self.app.position[0] < 1 and self.app.position[2] > 0 else (True, False) if \
            self.app.position[0] > 1 > self.app.position[2] else (False, False)

        if quadrant_position == self.quadrants[0]:
            print("you are in the first quadrant")
        if quadrant_position == self.quadrants[1]:
            print("you are in the second quadrant")
        if quadrant_position == self.quadrants[2]:
            print("you are in the third quadrant")
        if quadrant_position == self.quadrants[3]:
            print("you are in the fourth quadrant")

    '''