# Example file showing a circle moving on screen
import math

import numpy as np
import pygame
from pygame import Vector2
from stable_baselines3 import PPO

from CannonBall import CannonBall
from Ship import Ship
from SpriteSheet import SpriteSheet


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True
dt = 0

sheet = SpriteSheet('pirate.png', (255, 255, 255))
sheet_n = SpriteSheet('navy.png', (0, 0, 0))


pirate = Ship(sheet, Vector2(screen.get_width()/3-150, screen.get_height()/2-150))
navy = Ship(sheet_n, Vector2(screen.get_width()/3*2, screen.get_height()/2-150))
n_model = PPO.load("pirate_model")
group = pygame.sprite.Group()
last = pygame.time.get_ticks()
last_n = pygame.time.get_ticks()

pygame.display.set_caption("Pirates vs Navy")
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")

    keys = pygame.key.get_pressed()

    obs = np.array([navy.player_pos.x, navy.player_pos.y, pirate.player_pos.x, pirate.player_pos.y])
    for c in group:
        if (obs.shape[0] < 10 and c.target == navy):
            obs = np.append(obs, [c.pos.x, c.pos.y], axis=0)
        else:
            break

    if (obs.shape[0] < 10):
        for i in range(10 - obs.shape[0]):
            obs = np.append(obs, -1)
    target = math.atan2(pirate.player_pos.y - navy.player_pos.y,
                        pirate.player_pos.x - navy.player_pos.x)

    target = math.degrees(target) + 180
    # find difference between target and current angle
    try:
        diff = 360 % abs(target - navy.heading)
    except:
        diff = 0

    obs = obs[0:10]
    obs = np.append(obs, target)
    print(obs)
    pirate.update(keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d], screen, dt)
    action = n_model.predict(obs)[0]
    navy.update(action[0] == 1, action[1] == 1, action[2] == 1, action[3] == 1, screen, dt)
    group.update(0, 0, 0, 0, screen, dt)
    group.draw(screen)

    pygame.draw.rect(screen, (255, 0, 0), (50, 50, 50, 10))
    pygame.draw.rect(screen, (0, 255, 0), (50, 50, 50 - (5 * (10 - pirate.hp)), 10))

    pygame.draw.rect(screen, (255, 0, 0), (screen.get_width()-100, 50, 50, 10))
    pygame.draw.rect(screen, (0, 255, 0), (screen.get_width()-100, 50, 50 - (5 * (10 - navy.hp)), 10))

    if pygame.mouse.get_pressed()[0]:
        if pygame.time.get_ticks() - last > 1500:
            last = pygame.time.get_ticks()
            group.add(CannonBall(pirate, navy))

    if action[4] == 1:
        if pygame.time.get_ticks() - last_n > 1500:
            last_n = pygame.time.get_ticks()
            group.add(CannonBall(navy, pirate))
    # flip() the display to put your work on screen

    screen.blit(pirate.image, pirate.rect)
    screen.blit(navy.image, navy.rect)
    group.draw(screen)
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(60) / 1000

pygame.quit()
