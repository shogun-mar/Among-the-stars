import pygame
from settings import PROJECTILE_VELOCITY, vec2, SCREEN_HEIGHT, SCREEN_WIDTH

class Projectile:
    def __init__(self, original_entity, target, game):
        self.game = game
        self.original_entity = original_entity
        self.target_pos = target.screen_pos
        self.pos3d = self.original_entity.pos3d
        self.vel = PROJECTILE_VELOCITY  # Projectile velocity
        self.sprite = pygame.image.load('graphics/projectile.png').convert_alpha()
        self.rect = self.sprite.get_rect(midtop = self.original_entity.shooting_points_coords)
        self.sprite = pygame.transform.rotate(self.sprite, self.get_angle()) #Rotate the projectile sprite to face the target

    def update(self):
        # Calculate direction vector (from projectile to target)
        direction = self.target_pos - pygame.math.Vector2(self.rect.center)
        distance = direction.length()  # Calculate the distance to the target

        if distance <= self.vel: # If close enough, place the projectile directly at the target position
            self.rect.center = self.target_pos
        else: # Normalize the direction vector and move the projectile towards the target
            direction.normalize_ip() #Adjust the direction vector to have a length of 1 withouth changing the direction
            self.rect.center += direction * self.vel

        if self.rect.center == self.target_pos:
             # Removing the projectile, subtracting life points
            self.game.current_life_points -= 1
            self.game.game_starfield.objects_to_remove.append(self)

    def draw(self):
        self.game.fake_screen.blit(self.sprite, self.rect) #To avoid adding unnecessary lines of code i will use the original entity screen to draw the projectile

    def get_angle(self):
        return vec2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2).angle_to(vec2(self.target_pos)) * (-1)
        #return vec2(self.target_pos).angle_to(vec2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) * (-1)