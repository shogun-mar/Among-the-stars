from settings import *
from logic.game_star import Star
from logic.enemy import Enemy
from logic.powerup import PowerUp

class Starfield:
    def __init__(self, game):
        self.game = game
        self.stars = [Star(game) for _ in range(NUM_STARS)]
        self.enemies = []
        self.powerups = []
        self.last_enemy_respawn_time = 0
        self.last_powerup_respawn_time = 0
        self.surf_to_draw = self.stars + self.enemies + self.powerups

    def update(self, game):
        current_time = pygame.time.get_ticks()
        if len(self.enemies) < MAX_NUM_ENEMIES_SCREEN: #Checks if the number of enemies on screen is lower than the maximum
            if current_time - self.last_enemy_respawn_time > ENEMY_RESPAWN_COOLDOWN: #Spawns the enemy only if the cooldown has passed
                self.last_enemy_respawn_time = current_time
                self.enemies.append(Enemy(game))
                self.surf_to_draw = self.stars + self.enemies + self.powerups
        if len(self.powerups) < MAX_NUM_POWERUPS_SCREEN:
            if current_time - self.last_powerup_respawn_time > POWERUP_RESPAWN_COOLDOWN:
                self.last_powerup_respawn_time = current_time
                self.powerups.append(PowerUp(game))
                self.surf_to_draw = self.stars + self.enemies + self.powerups

        [star.update() for star in self.stars] #Update all before drawing to have consistent movement
        [enemy.update() for enemy in self.enemies] #Update all before drawing to have consistent movement

    def draw(self):
        self.surf_to_draw.sort(key=lambda surf: surf.pos3d.z, reverse = True) #Painter's algorithm
        [surf.draw() for surf in self.surf_to_draw] #Draw the now sorted surfaces
        