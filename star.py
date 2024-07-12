import random, math, pygame
from settings import *

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

class Star:
    def __init__(self, game):
        self.screen = game.fake_screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.size = INITIAL_SIZE
        self.screen_pos = vec2(0, 0)
        self.mouse_offset = vec2(0, 0)  # New variable to track mouse offset

        self.is_rotating = False  # New variable to track rotation state
        self.rotation_amount = 0.0  # New variable to track cumulative rotation
        self.position_offset = vec2(0, 0)  # New variable to track cumulative position offset

    def get_pos3d(self):
        angle = random.uniform (0, 2 * math.pi)
        radius = random.randrange( SCREEN_HEIGHT // SCALE_POS,  SCREEN_HEIGHT) * SCALE_POS #For starfield
        #radius = random.randrange( SCREEN_HEIGHT // 4,  SCREEN_HEIGHT //3) * SCALE_POS #For hyperspace tunnel
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER + self.mouse_offset
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)

        self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_VELOCITY)  # Rotate the star

        if pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
            # Rotate
            self.pos3d.xy = self.pos3d.xy.rotate(0.1)
            # Mouse control
            self.mouse_offset = pygame.math.Vector2(pygame.mouse.get_pos()) - CENTER
            

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))