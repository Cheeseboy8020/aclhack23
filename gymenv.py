import math

import numpy as np
import pygame
from gym.spaces.multi_binary import MultiBinary
from gym.spaces.box import Box
from stable_baselines3 import PPO
import gym

from SpriteSheet import SpriteSheet
from Ship import Ship
from CannonBall import CannonBall
from pygame import Vector2
class PiratesEnv(gym.Env):
    def __init__(self, render_mode):
        self.action_space = MultiBinary(5)
        self.observation_space = Box(low=-2, high=1000, shape=(11, ), dtype=np.float64)
        self.render_mode = render_mode
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        pygame.init()
        self.sheet = SpriteSheet('pirate.png', (255, 255, 255))
        self.sheet_n = SpriteSheet('navy.png', (0, 0, 0))
        self.pirate = Ship(self.sheet, Vector2(self.screen.get_width() / 3 - 150, self.screen.get_height() / 2 - 150))
        self.navy = Ship(self.sheet_n, Vector2(self.screen.get_width() / 3 * 2, self.screen.get_height() / 2 - 150))
        self.last = pygame.time.get_ticks()
        self.group = pygame.sprite.Group()
        self.pirate_model = PPO.load("pirate_model")
        self.last_p = self.pirate.hp
        self.last_n = self.navy.hp
        self.obs = np.array([self.pirate.player_pos.x, self.pirate.player_pos.y, self.navy.player_pos.x, self.navy.player_pos.y, -1, -1, -1, -1, -1, -1, 270])
        self.steps = 0

    def step(self, action):
        self.pirate_model = PPO.load("pirate_model")
        if action[0] == 1:
            acc0 = True
        else:
            acc0 = False
        if action[1] == 1:
            acc1 = True
        else:
            acc1 = False
        if action[2] == 1:
            acc2 = True
        else:
            acc2 = False
        if action[3] == 1:
            acc3 = True
        else:
            acc3 = False

        p_action, _states = self.pirate_model.predict(self.obs)
        #p_action = [0, 0, 0, 0, 0]

        self.pirate.update(p_action[0], p_action[1], p_action[2], p_action[3], self.screen, self.dt)
        self.navy.update(acc0, acc1, acc2, acc3, self.screen, self.dt)
        self.group.update(0, 0, 0, 0, self.screen, self.dt)
        if action[4] == 1:
            if pygame.time.get_ticks() - self.last > 500:
                self.last = pygame.time.get_ticks()
                self.group.add(CannonBall(self.navy, self.pirate))
        if p_action[4] == 1:
            if pygame.time.get_ticks() - self.last > 500:
                self.last = pygame.time.get_ticks()
                self.group.add(CannonBall(self.pirate, self.navy))


        p_obs = np.array([
            [self.pirate.player_pos.x, self.pirate.player_pos.y],
            [self.navy.player_pos.x, self.navy.player_pos.y],
        ])
        for c in self.group:
            if(p_obs.shape[0] < 10 and c.target == self.pirate):
                p_obs = np.append(p_obs, c.pos.x)
                p_obs = np.append(p_obs, c.pos.y)
            else:
                break
        if(p_obs.shape[0] < 10):
            for i in range(10-p_obs.shape[0]):
                p_obs = np.append(p_obs, -1)

        target = math.atan2(self.navy.player_pos.y - self.pirate.player_pos.y,
                            self.navy.player_pos.x - self.pirate.player_pos.x)

        target = math.degrees(target) + 180
        # find difference between target and current angle
        try:
            diff = 360 % abs(target - self.pirate.heading)
        except:
            diff = 0
        self.obs = p_obs[0:10]
        self.obs = np.append(self.obs, diff)


        obs = np.array([
            [self.navy.player_pos.x, self.navy.player_pos.y],
            [self.pirate.player_pos.x, self.pirate.player_pos.y],
        ])
        for c in self.group:
            if(obs.shape[0] < 10 and c.target == self.navy):
                obs = np.append(obs, [[c.pos.x, c.pos.y]], axis=0)
            else:
                break

        if(obs.shape[0] < 10):
            for i in range(10-obs.shape[0]-2):
                obs = np.append(obs, -1)

        reward = 0

        if self.last_n>self.navy.hp:
            self.last_n = self.navy.hp
            reward -= 10

        if self.last_p>self.pirate.hp:
            self.last_p = self.pirate.hp
            reward += 10
        else:
            reward -= 1

        target = math.atan2(self.pirate.player_pos.y - self.navy.player_pos.y, self.pirate.player_pos.x - self.navy.player_pos.x)

        target = math.degrees(target)+180
        #find difference between target and current angle
        try:
            diff = 360%abs(target - self.navy.heading)
        except:
            diff = 0



        reward += 1 - diff/180

        self.dt = self.clock.tick(60) / 1000

        self.render()
        done = False
        if(self.steps > 500):
            done = True
            self.steps = 0
        self.steps += 1

        obs = obs[0:10]
        obs = np.append(obs, target)
        #print(self.steps)
        return obs, reward, done, {}
    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill("blue")
        self.screen.blit(self.pirate.image, self.pirate.rect)
        self.screen.blit(self.navy.image, self.navy.rect)
        self.group.draw(self.screen)
        pygame.display.flip()

    def reset(self):
        self.pirate = Ship(self.sheet, Vector2(self.screen.get_width() / 3 - 150, self.screen.get_height() / 2 - 150))
        self.navy = Ship(self.sheet_n, Vector2(self.screen.get_width() / 3 * 2, self.screen.get_height() / 2 - 150))
        self.last = pygame.time.get_ticks()
        self.pirate.hp = 10
        self.navy.hp = 10
        self.group.empty()
        self.last_p = self.pirate.hp
        self.last_n = self.navy.hp
        return np.asarray([self.navy.player_pos.x, self.navy.player_pos.y,
                           self.pirate.player_pos.x, self.pirate.player_pos.y,
                           -1, -1,
                           -1, -1,
                           -1, -1,
                           90], dtype=np.float64)