from settings import *
from logic.hyperspace_star import HyperspaceStar

class HyperspaceStarfield:
    def __init__(self, game):
        self.game = game
        self.stars = [HyperspaceStar(game) for _ in range(DEMO_STARS_NUM)]
        self.game.set_starfield(self)

    def update(self, game):
        [star.update() for star in self.stars] #Update all before drawing to have consistent movement

    def draw(self):
        self.stars.sort(key=lambda surf: surf.pos3d.z, reverse = True) #Painter's algorithm
        [surf.draw() for surf in self.stars] #Draw the now sorted surfaces

    def switch(self):
        pass