import random, math, pygame
from settings import *

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

class HyperspaceStar:
    def __init__(self, game):
        self.screen = game.fake_screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.45, 0.95)
        self.color = random.choice(DEMO_COLORS)
        self.size = DEMO_STAR_INITIAL_SIZE
        self.screen_pos = vec2(0, 0)

    def get_pos3d(self):
        angle = random.uniform (0, 2 * math.pi)
        radius = random.randrange( SCREEN_HEIGHT // 4,  SCREEN_HEIGHT //3) * SCALE_POS
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, DEMO_Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (DEMO_Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))