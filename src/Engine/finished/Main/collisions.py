class Collisions:
    def __init__(self, app):
        self.app = app
        self.limits = (0.5, 2, 4)
        self.position_rock = (100, 100)

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
        if collisionFound and self.verify():
            return True
        else:
            return False
# finished

    def verify(self):
        vertices = ([

            [4.77, 1.04],
            [4.53, 5.63],
            [-3.21, 5.86],
            [-3.21, -3.37],
            [4.31, -3.37],
            [4.57, -1.97],
            [6.14, -2.53],
            [6.28, -1.49],
            [3.73, -1.05],
            [3.17, -1.89],
            [-1.72, -1.73],
            [-1.72, 0.53],
            [0.43, 0.60],
            [0.36, 4.31],
            [3.19, 4.21],
            [2.98, 0.42]

        ])

        # Definir el punto a verificar
        P = ([self.app.x, self.app.z])

        # Función para verificar si un punto está dentro de un polígono
        def is_point_in_polygon(point, vertices):
            n = len(vertices)
            inside = False
            x, z = point
            p1x, p1z = vertices[0]
            for i in range(n + 1):
                p2x, p2z = vertices[i % n]
                if z > min(p1z, p2z):
                    if z <= max(p1z, p2z):
                        if x <= max(p1x, p2x):
                            if p1z != p2z:
                                xinters = (z - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1z = p2x, p2z
            return inside

        # Verificar si el punto está dentro del hexágono en el plano 'xz'
        if is_point_in_polygon(P, vertices):
            return False
        else:
            return True

    def verify_isHouse(self):
        vertices = ([

            [3.9, 5.83],
            [-3.11, 5.93],
            [-3.11, -3.90],
            [4.24, -4.04]


        ])

        # Definir el punto a verificar
        P = ([self.app.x, self.app.z])

        # Función para verificar si un punto está dentro de un polígono
        def is_point_in_polygon(point, vertices):
            n = len(vertices)
            inside = False
            x, z = point
            p1x, p1z = vertices[0]
            for i in range(n + 1):
                p2x, p2z = vertices[i % n]
                if z > min(p1z, p2z):
                    if z <= max(p1z, p2z):
                        if x <= max(p1x, p2x):
                            if p1z != p2z:
                                xinters = (z - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1z = p2x, p2z
            return inside

        # Verificar si el punto está dentro del hexágono en el plano 'xz'
        if is_point_in_polygon(P, vertices):
            return False
        else:
            return True