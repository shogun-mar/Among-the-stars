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
        self.scale_multiplier = 1
        self.vel = random.uniform(0.05, 0.25)
        self.sprite = pygame.image.load('graphics/spaceship_enemy.png')
        self.rect = self.sprite.get_rect(topleft = (0, 0))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
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
        self.rect.topleft = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER + self.mouse_offset # Update the rect position

        if pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
            self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_VELOCITY) # Rotate
            self.mouse_offset = pygame.math.Vector2(pygame.mouse.get_pos()) - CENTER

        # Calculate scale multiplier based on z-distance
        self.scale_multiplier = round(1 / max(self.pos3d.z, 1), 2) # Avoid division by zero or negative values
        print(self.scale_multiplier)
        # Update the sprite size based on the scale multiplier
        scaled_width = int(self.sprite_width * self.scale_multiplier)
        scaled_height = int(self.sprite_height * self.scale_multiplier)
        self.sprite = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
        # Update the rect size and position
        self.rect.size = self.sprite.get_size()
        self.rect.topleft = vec2(self.pos3d.x, self.pos3d.y) / max(self.pos3d.z, 1) + CENTER + self.mouse_offset

        if (random.random() < 0.01) and self.can_shoot(): self.shoot_at_player() # Random chance to shoot at the player

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def can_shoot(self):
        #Checks in order if the entity is withing the frame, if the number of projectiles is lower than the maximum and if the entity is not at the bottom of the screen
        return self.rect.colliderect(self.screen_rect) and (len(self.game.game_starfield.projectiles) < MAX_NUM_PROJECTILES_SCREEN-1) and (self.rect.midbottom[1] < SCREEN_HEIGHT - 20)

    def shoot_at_player(self):
        projectile = Projectile(self.rect.midbottom, self) # Create a projectile aimed at the player's position
        self.game.game_starfield.projectiles.append(projectile) # Add the projectile to the projectiles list in game_starfield

        