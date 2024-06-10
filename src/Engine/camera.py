import glm


import pygame as pg

FOV = 50  # deg
NEAR = 0.1
FAR = 100
SPEED = 0.030
SENSITIVITY = 0.08


class Camera:
    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        self.Limits = glm.vec2(20, -20)

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d] or keys[pg.K_w]:
            print(self.position)
        if keys[pg.K_w]:
            z = self.position[2] + self.forward[2] * velocity
            x = self.position[0] + self.forward[0] * velocity
            if self.Limits[0] > z > self.Limits[1] and self.Limits[0] > x > self.Limits[1]:
                self.position[2] = z
                self.position[0] = x
        if keys[pg.K_s]:
            z = self.position[2] - self.forward[2] * velocity
            x = self.position[0] - self.forward[0] * velocity
            if self.Limits[1] < z < self.Limits[0] and self.Limits[1] < x < self.Limits[0]:
                self.position[2] = z
                self.position[0] = x
        if keys[pg.K_a]:
            x = self.position[0] - self.right[0] * velocity
            z = self.position[2] - self.right[2] * velocity
            if self.Limits[1] < x < self.Limits[0] and self.Limits[1] < z < self.Limits[0]:
                self.position[0] = x
                self.position[2] = z
        if keys[pg.K_d]:
            x = self.position[0] + self.right[0] * velocity
            z = self.position[2] + self.right[2] * velocity
            if self.Limits[0] > x > self.Limits[1] and self.Limits[0] > z > self.Limits[1]:
                self.position[0] = x
                self.position[2] = z
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)