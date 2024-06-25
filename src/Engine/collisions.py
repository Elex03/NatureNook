class Collisions:
    def __init__(self, app):
        self.app = app
        self.limits = (0.5, 2, 4)
        self.position_rock = (0, 0)

    def check_limits(self, position):
        collisionFound = True
        length_positions = len(position)

        for i in range(length_positions):
            bool_x = position[i][0] - self.limits[0] < self.app.x < position[i][0] + self.limits[0]
            bool_z = position[i][1] - self.limits[0] < self.app.z < position[i][1] + self.limits[0]

            if bool_x and bool_z:
                collisionFound = False
                break
        bool_x1 = self.position_rock[0] - self.limits[2] < self.app.x < self.position_rock[0] + self.limits[2]
        bool_z1 = self.position_rock[1] - self.limits[1] < self.app.z < self.position_rock[1] + self.limits[1]
        if bool_x1 and bool_z1:
            collisionFound = False
        if collisionFound:
            return True
        else:
            return False
# finished
