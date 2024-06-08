import glm


class Light:
    def __init__(self, app, position=(50, 50, -10)):
        self.color = glm.vec3(app.color[0]) if app.is_day else glm.vec3(app.color[1])
        self.position = glm.vec3(position)
        self.direction = glm.vec3(0, 0, 0)
        # intensities
        self.Ia = 0.6 * self.color  # ambient
        self.Id = 0.8 * self.color  # diffuse
        self.Is = 1.0 * self.color  # specular
        # view matrix
        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))
