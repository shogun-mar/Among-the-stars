import pygame
import random, math
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, Z_DISTANCE, CENTER, ROTATION_VELOCITY, SCALE_POS, MAX_NUM_PROJECTILES_SCREEN, SCALE_MULTIPLIER_LINEAR_FACTOR
from logic.projectile import Projectile

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

class Enemy:
    def __init__(self, game, player_reference):
        self.game = game
        self.player = player_reference
        self.screen = game.fake_screen
        self.screen_rect = self.screen.get_rect()
        self.pos3d = self.get_pos3d()
        self.scale_multiplier: float = 1
        self.vel = random.uniform(0.05, 0.25)
        self.original_sprite = pygame.image.load('graphics/spaceship_enemy.png').convert_alpha()
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(topleft = (0, 0))
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.mouse_offset = vec2(0, 0)  # New variable to track mouse offset
        self.last_shot_time = 0

        self.resize_cooldown_duration = 3000 #Expressed in seconds
        self.last_resize_cooldown_time = 0 

    @property
    def screen_pos(self): #Used to get the screen position of the entity
        return self.rect.center

    @property
    def shooting_points_coords(self):
        return self.rect.midbottom

    def get_pos3d(self):
        angle = random.uniform (0, 2 * math.pi)
        radius = random.randrange( SCREEN_HEIGHT // SCALE_POS,  SCREEN_HEIGHT) * SCALE_POS
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        if self.pos3d.z < 1:
            self.pos3d = self.get_pos3d()
            #self.sprite = pygame.transform.rotate(self.original_sprite, self.get_angle())
            #self.rect.size = self.sprite.get_size()

        self.rect.topleft = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER + self.mouse_offset # Update the rect position

        if pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
            self.pos3d.xy = self.pos3d.xy.rotate(ROTATION_VELOCITY) # Rotate
            self.mouse_offset = pygame.math.Vector2(pygame.mouse.get_pos()) - CENTER

        if self.is_on_screen() and self.can_be_resized(): #Temporarly disabled
            self.scale_multiplier = round(1 + SCALE_MULTIPLIER_LINEAR_FACTOR * (Z_DISTANCE - self.pos3d.z), 2)
            self.scale_multiplier = min(self.scale_multiplier, 2) # Limit the scale multiplier to 2
            print("Scale Multiplier = ", self.scale_multiplier, "Z Distance = ", self.pos3d.z)
            # Update the sprite size based on the scale multiplier
            scaled_width = int(self.sprite_width * self.scale_multiplier)
            scaled_height = int(self.sprite_height * self.scale_multiplier)
            self.sprite = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
            # Update the rect size and position
            self.rect.size = self.sprite.get_size()
            self.rect.topleft = vec2(self.pos3d.x, self.pos3d.y) / max(self.pos3d.z, 1) + CENTER + self.mouse_offset

        if (random.random() <= 0.25) and self.can_shoot(): self.shoot_at_player() # Random chance to shoot at the player

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def can_shoot(self):
        #Checks in order if the entity is withing the frame, if the number of projectiles is lower than the maximum and if the entity is not at the bottom of the screen and if the cooldown has expired
        current_time = pygame.time.get_ticks()
        has_cooldown_expired = False
        if current_time - self.last_shot_time > 5000:
            has_cooldown_expired = True
            self.last_shot_time = current_time
        return self.rect.colliderect(self.screen_rect) \
        and (len(self.game.game_starfield.projectiles) < MAX_NUM_PROJECTILES_SCREEN-1) \
        and (self.rect.midbottom[1] < SCREEN_HEIGHT * 0.8) \
        and has_cooldown_expired

    def shoot_at_player(self):
        projectile = Projectile(original_entity=self, target_pos=self.player.rect.midtop, is_enemy=True, game=self.game) # Create a projectile aimed at the player's position
        self.game.game_starfield.projectiles.append(projectile) # Add the projectile to the projectiles list in game_starfield

    def is_on_screen(self):
        return False
        return self.rect.colliderect(self.screen_rect)

    def can_be_resized(self):
        return pygame.time.get_ticks() - self.last_resize_cooldown_time > self.resize_cooldown_duration

    def get_angle(self):
        return vec2(self.shooting_points_coords).angle_to(vec2(self.player.screen_pos)) * -1