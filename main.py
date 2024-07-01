from game import Game
from starfield import Starfield

game = Game()
starfield = Starfield(game)
game.set_starfield(starfield)
game.run()