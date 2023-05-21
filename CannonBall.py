import math

import pygame
from pygame import Vector2


class CannonBall(pygame.sprite.Sprite):

    hypot = 65
    def __init__(self, sender_ship, target_ship):
        super().__init__()
        self.image = pygame.image.load("cannonball.png")
        self.pos = Vector2((2*sender_ship.player_pos.x+sender_ship.w)/2, (2*sender_ship.player_pos.y+sender_ship.h)/2)
        self.heading = sender_ship.heading
        self.pos.x += math.cos(math.radians(self.heading + 90)) * self.hypot
        self.pos.y -= math.sin(math.radians(self.heading + 90)) * self.hypot
        self.rad = 15
        self.target = target_ship
        self.image = pygame.transform.scale(self.image, (self.rad * 2, self.rad * 2))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

    def update(self, _, __, ___, ____, screen, dt):
        self.pos.x +=math.cos(math.radians(self.heading + 90)) * dt * 300
        self.pos.y -= math.sin(math.radians(self.heading + 90)) * dt * 300

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

        if self.pos.x - self.rad < 0:
            self.kill()
        if self.pos.x + self.rad > screen.get_width():
            self.kill()
        if self.pos.y < 0:
            self.kill()
        if self.pos.y - self.rad > screen.get_height():
            self.kill()

        if pygame.Rect.colliderect(self.rect, self.target.rect):
            self.kill()
            self.target.hp -= 1

        self.image = pygame.transform.scale(self.image, (self.rad*2, self.rad*2))