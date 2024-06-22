class Collisions:
    def __init__(self, app):
        self.app = app
        self.limits = (0.5, 0.5)

    def check_limits(self, position):
        collisionFound = True
        return collisionFound
        '''
        length_positions = len(position)
        for i in range(length_positions):
            bool_x = position[i][0] - self.limits[0] < self.app.x < position[i][0] + self.limits[0]
            bool_z = position[i][1] - self.limits[0] < self.app.z < position[i][1] + self.limits[0]

            if bool_x and bool_z:
                collisionFound = False
                break
        if collisionFound:
            return True
        else:
            return False
        '''


# finished