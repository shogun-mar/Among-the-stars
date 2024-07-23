from logic.game import Game
from logic.game_starfield import Starfield
from logic.hyperspace_starfield import HyperspaceStarfield
from logic.player import Player
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

game = Game()
hyperspace_starfield = HyperspaceStarfield(game)
game.set_hyperspace_starfield(hyperspace_starfield)
game_starfield = Starfield(game)
game.set_starfield(game_starfield)
player = Player(game_reference=game, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT))
game.set_player(player)
game.run()