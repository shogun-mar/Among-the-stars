from settings import *
from logic.game_star import Star
from logic.enemy import Enemy
from logic.powerup import PowerUp
from logic.projectile import Projectile

class Starfield:
    def __init__(self, game):
        self.game = game
        self.stars = [Star(game) for _ in range(NUM_STARS)]
        self.enemies = []
        self.powerups = []
        self.projectiles = []
        self.objects_to_remove = []
        self.last_enemy_respawn_time = 0
        self.last_powerup_respawn_time = 0
        self.surf_to_draw = self.stars + self.enemies + self.powerups + self.projectiles

    def update(self, game):
        current_time = pygame.time.get_ticks()
        if len(self.enemies) < MAX_NUM_ENEMIES_SCREEN: #Checks if the number of enemies on screen is lower than the maximum
            if current_time - self.last_enemy_respawn_time > ENEMY_RESPAWN_COOLDOWN: #Spawns the enemy only if the cooldown has passed
                self.last_enemy_respawn_time = current_time
                self.enemies.append(Enemy(game))
                self.surf_to_draw = self.stars + self.enemies + self.powerups + self.projectiles
        if len(self.powerups) < MAX_NUM_POWERUPS_SCREEN:
            if current_time - self.last_powerup_respawn_time > POWERUP_RESPAWN_COOLDOWN:
                self.last_powerup_respawn_time = current_time
                self.powerups.append(PowerUp(game))
                self.surf_to_draw = self.stars + self.enemies + self.powerups + self.projectiles

        [surf.update() for surf in self.surf_to_draw] #Update all surfaces before drawing to have consistent movement

        # Iterate through the objects to remove and remove them from the respective lists
        # This is done to avoid modifying the list while iterating through it
        for object in self.objects_to_remove:
            if isinstance(object, Projectile) and object in self.projectiles:
                self.projectiles.remove(object)
            elif isinstance(object, Enemy) and object in self.enemies:
                self.enemies.remove(object)
            elif isinstance(object, PowerUp) and object in self.powerups:
                self.powerups.remove(object)

        self.objects_to_remove.clear()  # Clear the list of objects to remove

    """#Iterate through the objects to remove and remove them from the respective lists
        #This is done to avoid modifying the list while iterating through it
        for object in self.objects_to_remove:
            if isinstance(object, Projectile): self.projectiles.remove(object)
            elif isinstance(object, Enemy): self.enemies.remove(object)
            elif isinstance(object, PowerUp): self.powerups.remove(object) 
        
        self.objects_to_remove.clear() #Clear the list of objects to remove"""

    def draw(self):
        self.surf_to_draw.sort(key=lambda surf: surf.pos3d.z, reverse = True) #Painter's algorithm
        [surf.draw() for surf in self.surf_to_draw] #Draw the now sorted surfaces
        