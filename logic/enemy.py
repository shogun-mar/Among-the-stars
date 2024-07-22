import pygame
import random, math
from settings import SCREEN_HEIGHT , SCREEN_WIDTH, Z_DISTANCE, CENTER, ROTATION_VELOCITY, SCALE_POS
from logic.projectile import Projectile

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

class Enemy:
    def __init__(self, game):
        self.screen = game.fake_screen
        self.screen_rect = self.screen.get_rect()
        self.game = game
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.sprite = pygame.image.load('graphics/spaceship_enemy.png')
        self.rect = self.sprite.get_rect(topleft = (0, 0))
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

        self.rect.topleft = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER + self.mouse_offset
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)

        if random.randint(1, 4) == 1 and self.is_sprite_in_frame(): # Random chance to shoot at the player
            self.shoot_at_player()

        if pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
            # Rotate
            self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_VELOCITY)
            # Mouse control
            self.mouse_offset = pygame.math.Vector2(pygame.mouse.get_pos()) - CENTER

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def is_sprite_in_frame(self):
        return self.rect.colliderect(self.screen_rect)

    def shoot_at_player(self):
        # Create a projectile aimed at the player's position
        projectile = Projectile(self.rect.midbottom, self) # Create a projectile
        self.game.game_starfield.projectiles.append(projectile) # Add the projectile to the projectiles list in game_starfield

        