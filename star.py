import random, math, pygame
from settings import *

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

class Star:
    def __init__(self, game):
        self.screen = game.screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.size = 10
        self.screen_pos = vec2(0, 0)

    def get_pos3d(self):
        angle = random.uniform (0, 2 * math.pi)
        radius = random.randrange(HEIGTH // SCALE_POS, HEIGTH) * SCALE_POS
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE / sFelf.pos3d.z)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))