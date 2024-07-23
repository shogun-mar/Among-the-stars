import pygame
import random, math
from settings import SCREEN_HEIGHT , Z_DISTANCE, CENTER, ROTATION_VELOCITY, SCALE_POS, MAX_NUM_PROJECTILES_SCREEN
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

        if pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
            # Rotate
            self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_VELOCITY)
            # Mouse control
            self.mouse_offset = pygame.math.Vector2(pygame.mouse.get_pos()) - CENTER

        if (random.random() < 0.01) and self.can_shoot(): # Random chance to shoot at the player
            self.shoot_at_player()

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def can_shoot(self):
        #Checks in order if the entity is withing the frame, if the number of projectiles is lower than the maximum and if the entity is not at the bottom of the screen
        return self.rect.colliderect(self.screen_rect) and (len(self.game.game_starfield.projectiles) < MAX_NUM_PROJECTILES_SCREEN) and (self.rect.midbottom[1] < SCREEN_HEIGHT - 20)

    def shoot_at_player(self):
        # Create a projectile aimed at the player's position
        projectile = Projectile(self.rect.midbottom, self) # Create a projectile
        self.game.game_starfield.projectiles.append(projectile) # Add the projectile to the projectiles list in game_starfield

        