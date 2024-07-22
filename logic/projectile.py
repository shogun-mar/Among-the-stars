import pygame, random, math
from settings import *

class Projectile:
    def __init__(self, pos, target_pos, original_entity):
        self.original_entity = original_entity # The entity that shot the projectile
        self.pos = pygame.math.Vector2(pos)
        self.pos3d = self.get_pos3d()
        self.target_pos = pygame.math.Vector2(target_pos)
        self.screen_pos = vec2(0, 0)
        self.vel = 1  # Projectile velocity
        self.sprite = pygame.image.load('graphics/projectile.png')
        self.rect = self.sprite.get_rect(center = self.pos)

    def get_pos3d(self):
        return self.original_entity.pos3d
    
    def update(self):
        # Move the projectile towards the target
        direction = (self.target_pos - self.pos).normalize()
        self.pos += direction * self.vel # Move the projectile
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)