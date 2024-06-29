import glm

from math import sqrt
from collisions import Collisions
import pygame as pg
from control import Control

FOV = 50  # deg
NEAR = 0.1
FAR = 200
SPEED = 0.010
SENSITIVITY = 0.08


class Camera:
    def __init__(self, app, position=(12.5, 2, 0), yaw=-90, pitch=0):
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
        self.Limits = glm.vec2(100, -100)
        self.Pos_Radio = glm.vec3(15, 2, 7)
        # auxiliar
        self.x = 0
        self.z = 0
        # control
        self.control = Control(self)
        # coalitions
        self.collisions = Collisions(self)


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

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        print(self.position)
        if keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d] or keys[pg.K_w]:
            distance = sqrt((self.position[0] - self.Pos_Radio[0]) ** 2 + (self.position[2] - self.Pos_Radio[2]) ** 2)
            if distance < 20:
                volume = round(distance) / 20
                # volume_normalized = abs(volume - 1)
                # self.app.sound_music.set_volume(volume_normalized)
                # print('Volume: ', self.app.sound_music.get_volume())

        if keys[pg.K_w]:
            self.z = self.position[2] + self.forward[2] * velocity
            self.x = self.position[0] + self.forward[0] * velocity
            bool_collisions = self.collisions.check_limits(self.app.Position)
            if self.Limits[0] > self.z > self.Limits[1] and self.Limits[0] > self.x > self.Limits[1] and bool_collisions:
                self.position[2] = self.z
                self.position[0] = self.x
        if keys[pg.K_s]:
            self.z = self.position[2] - self.forward[2] * velocity
            self.x = self.position[0] - self.forward[0] * velocity
            bool_collisions = self.collisions.check_limits(self.app.Position)
            if self.Limits[1] < self.z < self.Limits[0] and self.Limits[1] < self.x < self.Limits[0] and bool_collisions:
                self.position[2] = self.z
                self.position[0] = self.x
        if keys[pg.K_a]:
            self.x = self.position[0] - self.right[0] * velocity
            self.z = self.position[2] - self.right[2] * velocity
            bool_collisions = self.collisions.check_limits(self.app.Position)
            if self.Limits[1] < self.x < self.Limits[0] and self.Limits[1] < self.z < self.Limits[0] and bool_collisions:
                self.position[0] = self.x
                self.position[2] = self.z
        if keys[pg.K_d]:
            self.x = self.position[0] + self.right[0] * velocity
            self.z = self.position[2] + self.right[2] * velocity
            bool_collisions = self.collisions.check_limits(self.app.Position)
            if self.Limits[0] > self.x > self.Limits[1] and self.Limits[0] > self.z > self.Limits[1] and bool_collisions:
                self.position[0] = self.x
                self.position[2] = self.z

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)