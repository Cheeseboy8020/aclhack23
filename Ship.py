import math

import pygame
from pygame.math import Vector2

import SpriteSheet


class Ship(pygame.sprite.Sprite):
    def __init__(self, sheet: SpriteSheet, start_pos):
        super().__init__()
        self.player_pos = start_pos
        self.heading = 0
        self.sheet = sheet
        self.off = 0
        self.image = sheet.get_image(0, sheet.sprite_sheet.get_height()/4*3, sheet.sprite_sheet.get_width()/4, sheet.sprite_sheet.get_height()/4)
        self.rect = pygame.transform.rotate(self.image, self.heading-self.off).get_rect()
        self.rect.x = self.player_pos.x
        self.rect.y = self.player_pos.y

    def update(self, w, a, s, d, screen, dt):
        if 45 < self.heading < 135:
            self.image = self.sheet.get_image(0, 854 / 4, 712 / 4, 854 / 4)
            self.off = 90
        elif 135 <= self.heading <= 225:
            self.image = self.sheet.get_image(0, 0, 712 / 4, 854 / 4)
            self.off = 180
        elif 225 < self.heading < 315:
            self.image = self.sheet.get_image(0, 854 / 4 * 2, 712 / 4, 854 / 4)
            self.off = 270
        else:
            self.image = self.sheet.get_image(0, 854 / 4 * 3, 712 / 4, 854 / 4)
            self.off = 0

        if w:
            self.player_pos.x += math.cos(math.radians(self.heading + 90)) * dt * 100
            self.player_pos.y -= math.sin(math.radians(self.heading + 90)) * dt * 100
            # player_pos += Vector2.from_polar((1, heading-off)) * dt * 100
        if s:
            self.player_pos.x -= math.cos(math.radians(self.heading + 90)) * dt * 100
            self.player_pos.y += math.sin(math.radians(self.heading + 90)) * dt * 100
        if a:
            self.heading = (self.heading + (dt * 30) + 360) % 360
        if d:
            self.heading = (self.heading - (dt * 30) + 360) % 360

        self.rect = pygame.transform.rotate(self.image, self.heading-self.off).get_rect()
        self.rect.x = self.player_pos.x
        self.rect.y = self.player_pos.y

        if self.rect.left < 0:
            self.player_pos.x = 0
        if self.rect.right > screen.get_width():
            self.player_pos.x = screen.get_width() - self.rect.width
        if self.rect.top < 0:
            self.player_pos.y = 0

        if self.rect.bottom > screen.get_height():
            self.player_pos.y = screen.get_height() - self.rect.height

        screen.blit(pygame.transform.rotate(self.image, self.heading - self.off), (self.player_pos.x, self.player_pos.y))