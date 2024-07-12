from settings import *
from star import Star
from enemy import Enemy

class Starfield:
    def __init__(self, game):
        self.game = game
        self.stars = [Star(game) for _ in range(NUM_STARS)]
        self.enemies = [Enemy(game) for _ in range(NUM_ENEMIES)]
        self.surf_to_draw = self.stars + self.enemies
        self.game.set_starfield(self)

    def update(self):
        #if pygame.mouse.get_pressed()[0]: self.game.check_collisions() #Before updating the positions to correctly check with the last frames positions
        [star.update() for star in self.stars] #Update all before drawing to have consistent movement
        [enemy.update() for enemy in self.enemies] #Update all before drawing to have consistent movement

    def draw(self):
        self.surf_to_draw.sort(key=lambda surf: surf.pos3d.z, reverse = True) #Painter's algorithm
        [surf.draw() for surf in self.surf_to_draw] #Draw the now sorted surfaces
        