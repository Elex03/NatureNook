import glm


class Light:
    def __init__(self, app, toUse, pos):
        self.app = app
        if toUse:
            self.light((10, 50, 20))
        else:
            self.light(pos)

    def light(self, position):
        self.color = glm.vec3(self.app.color[0]) if self.app.is_day else glm.vec3(self.app.color[1])
        self.position = glm.vec3(position)
        self.direction = glm.vec3(0, 0, 0)

        # intensities
        if self.app.is_day:
            self.Ia = 0.2 * self.color
            self.Id = 0.6 * self.color
            self.Is = 1.2 * self.color
        else:
            # Configuración para una luciérnaga
            self.Ia = 0.05 * self.color  # Luz ambiental baja
            self.Id = 0.1 * self.color  # Luz difusa baja
            self.Is = 0.3 * self.color  # Luz especular moderada

            # Opcional: Puedes agregar un efecto de parpadeo para simular el comportamiento de una luciérnaga
            self.Ia *= glm.sin(self.app.time * 3.0) * 0.5 + 0.5  # Oscilación suave
            self.Id *= glm.sin(self.app.time * 3.0) * 0.5 + 0.5
            self.Is *= glm.sin(self.app.time * 3.0) * 0.5 + 0.5
        # view matrix
        self.m_view_light = self.get_view_matrix()
        
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))
