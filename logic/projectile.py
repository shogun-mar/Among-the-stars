import pygame
from settings import PROJECTILE_VELOCITY, vec2

class Projectile:
    def __init__(self, original_entity, target_pos, game):
        self.game = game
        self.original_entity = original_entity
        self.target_pos = target_pos
        self.pos3d = self.original_entity.pos3d
        self.vel = PROJECTILE_VELOCITY  # Projectile velocity
        self.sprite = pygame.image.load('graphics/projectile.png').convert_alpha()
        self.rect = self.sprite.get_rect(midtop = self.original_entity.shooting_points_coords)
        self.sprite = pygame.transform.rotate(self.sprite, self.get_angle()) #Rotate the projectile sprite to face the target

    def update(self):
        # Calculate direction vector (from projectile to target)
        direction = self.target_pos - pygame.math.Vector2(self.rect.midbottom)
        distance = direction.length()  # Calculate the distance to the target

        if distance <= self.vel: # If close enough, place the projectile directly at the target position
            self.rect.midbottom = self.target_pos
        else: # Normalize the direction vector and move the projectile towards the target
            direction.normalize_ip() #Adjust the direction vector to have a length of 1 withouth changing the direction
            self.rect.midbottom += direction * self.vel

        if self.rect.midbottom == self.target_pos:
            self.game.game_starfield.objects_to_remove.append(self) 
            if not self.game.is_shield_active: #If the shield is not active the player will lose a life point
                if self.target_pos == self.game.player.rect.midtop: self.game.current_life_points -= 1
            else: #If the shield is active the projectile will go back to the enemy
                projectile = Projectile(original_entity=self.game.player, target_pos=self.original_entity.shooting_points_coords, game=self.game)
                self.game.game_starfield.projectiles.append(projectile)
            
    def draw(self):
        self.game.fake_screen.blit(self.sprite, self.rect) #To avoid adding unnecessary lines of code i will use the original entity screen to draw the projectile

    def get_angle(self):
        return vec2(self.original_entity.shooting_points_coords).angle_to(vec2(self.target_pos)) * -1