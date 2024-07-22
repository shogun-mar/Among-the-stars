import pygame, random, math
from settings import PROJECTILE_VELOCITY, vec2, SCREEN_HEIGHT, SCREEN_WIDTH

class Projectile:
    def __init__(self, pos, original_entity):
        self.original_entity = original_entity # The entity that shot the projectile
        self.sprite = pygame.image.load('graphics/projectile.png')
        self.rect = self.sprite.get_rect(midtop = pos)
        self.pos3d = self.get_pos3d()
        self.target_pos = pygame.math.Vector2((SCREEN_HEIGHT, SCREEN_WIDTH // 2))
        self.screen_pos = vec2(0, 0)
        self.vel = PROJECTILE_VELOCITY  # Projectile velocity
        

    def get_pos3d(self):
        return self.original_entity.pos3d
    
    def update(self):
        print(self.rect.midbottom)
        # Remove the projectile if it reaches the target
        if self.rect.midbottom == self.target_pos:
            #print("Projectile reached target")
            self.original_entity.game.life_points -= 1 # Remove a life point 
            self.original_entity.game.game_starfield.projectiles.remove(self) # Remove the projectile from the list
        else:
            # Otherwise move the projectile towards the target
            direction = (self.target_pos - self.rect.center).normalize()
            self.rect.center += direction * self.vel # Move the projectile

    def draw(self):
        self.original_entity.screen.blit(self.sprite, self.rect) #To avoid adding unnecessary lines of code i will use the original entity screen to draw the projectile