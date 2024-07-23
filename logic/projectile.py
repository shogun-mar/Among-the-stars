import pygame, random, math
from settings import PROJECTILE_VELOCITY, vec2, SCREEN_HEIGHT, SCREEN_WIDTH

class Projectile:
    def __init__(self, original_entity, origin_pos, target_pos, game):
        self.game = game
        self.original_entity = original_entity
        self.sprite = pygame.image.load('graphics/projectile.png')
        self.rect = self.sprite.get_rect(midtop = origin_pos)
        #self.pos3d = self.get_pos3d()
        self.target_pos = target_pos
        self.screen_pos = vec2(0, 0)
        self.vel = PROJECTILE_VELOCITY  # Projectile velocity
        
    def get_pos3d(self):
        return self.original_entity.pos3d
    
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
        self.original_entity.screen.blit(self.sprite, self.rect) #To avoid adding unnecessary lines of code i will use the original entity screen to draw the projectile