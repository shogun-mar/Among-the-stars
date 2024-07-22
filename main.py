from logic.game import Game
from logic.game_starfield import Starfield
from logic.hyperspace_starfield import HyperspaceStarfield

game = Game()
hyperspace_starfield = HyperspaceStarfield(game)
game.set_hyperspace_starfield(hyperspace_starfield)
game_starfield = Starfield(game)
game.set_starfield(game_starfield)
game.run()