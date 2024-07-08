from settings import *
from star import Star
from enemy import Enemy

class Starfield:
    def __init__(self, game):
        self.stars = [Star(game) for _ in range(NUM_STARS)]
        self.enemies = [Enemy(game) for _ in range(NUM_ENEMIES)]
        self.surf_to_draw = self.stars + self.enemies
        game.set_starfield(self)

    def run(self):
        self.update()
        self.draw()

    def update(self):
        [star.update() for star in self.stars] #Update all before drawing to have consistent movement
        [enemy.update() for enemy in self.enemies] #Update all before drawing to have consistent movement

    def draw(self):
        self.surf_to_draw.sort(key=lambda surf: surf.pos3d.z, reverse = True) #Painter's algorithm
        [surf.draw() for surf in self.surf_to_draw] #Draw the now sorted surfaces

    
        