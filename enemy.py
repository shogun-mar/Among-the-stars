import pygame
import random, math
from settings import *

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

class Enemy:
    def __init__(self, game):
        self.screen = game.screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.sprite = pygame.image.load('graphics/spaceship_enemy.png')
        self.rect = self.sprite.get_rect()
        self.size = INITIAL_SIZE
        self.screen_pos = vec2(0, 0)

    def get_pos3d(self):
        angle = random.uniform (0, 2 * math.pi)
        radius = random.randrange(HEIGTH // SCALE_POS, HEIGTH) * SCALE_POS #For starfield
        #radius = random.randrange(HEIGTH // 4, HEIGTH //3) * SCALE_POS #For hyperspace tunnel
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)

        #Rotate
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)
        #Mouse control
        mouse_pos = CENTER - vec2(pygame.mouse.get_pos())
        self.screen_pos += mouse_pos

    def draw(self):
        self.screen.blit(self.sprite, self.rect)