from settings import *
from star import Star

class Starfield:
    def __init__(self, game):
        self.stars = [Star(game) for _ in range(NUM_STARS)]
        game.set_starfield(self)

    def run(self):
        [star.update() for star in self.stars] #Update all before drawing to have consistent movement
        self.stars.sort(key=lambda star: star.pos3d.z, reverse = True) #Painter's algorithm
        [star.draw() for star in self.stars]