# Example file showing a circle moving on screen

import pygame
from pygame import Vector2

from Ship import Ship
from SpriteSheet import SpriteSheet

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True
dt = 0

sheet = SpriteSheet('pirate.png', (255, 255, 255))
sheet_n = SpriteSheet('navy.png', (0, 0, 0))


pirate = Ship(sheet, Vector2(screen.get_width()/3, screen.get_height()/2))
navy = Ship(sheet_n, Vector2(screen.get_width()/3*2, screen.get_height()/2))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")

    keys = pygame.key.get_pressed()

    pirate.update(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d], screen, dt)
    navy.update(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d], screen, dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(60) / 1000

pygame.quit()
