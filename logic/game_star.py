import random, math, pygame
from settings import *

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

class Star:
    def __init__(self, game):
        self.screen = game.fake_screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.sprite = pygame.image.load("graphics/star.png").convert_alpha()
        self.current_rotation_angle = random.randint(0, 360)
        self.sprite = pygame.transform.rotate(self.sprite, self.current_rotation_angle) # Random rotation
        self.screen_pos = vec2(0, 0)
        self.rect = self.sprite.get_rect(topleft = self.screen_pos)
        self.mouse_offset = vec2(0, 0)  # New variable to track mouse offset

    def get_pos3d(self):
        angle = random.uniform (0, 2 * math.pi)
        radius = random.randrange( SCREEN_HEIGHT // SCALE_POS,  SCREEN_HEIGHT) * SCALE_POS
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER + self.mouse_offset
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
        self.rect.topleft = self.screen_pos #Update rect position

        if pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
            # Rotate
            self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_VELOCITY)
            # Mouse control
            self.mouse_offset = pygame.math.Vector2(pygame.mouse.get_pos()) - CENTER 

    def draw(self):
        self.screen.blit(self.sprite, self.screen_pos)