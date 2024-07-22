from logic.game import Game
from logic.starfield import Starfield
from logic.DEMO_starfield import DemoStarfield

game = Game()
starfield = Starfield(game)
game.set_starfield(starfield)
demo_starfield = DemoStarfield(game)
game.set_demo_starfield(demo_starfield)
game.run()