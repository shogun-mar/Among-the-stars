from states.gameState import GameState
from settings import *

def handle_hyperspace_events(game, key):
    if key == HYPERSPACE_KEY:
        game.game_state = GameState.GAMEPLAY
        game.alpha_surface.set_alpha(GAMEPLAY_ALPHA_VALUE)

def render_hyperspace(game):
    game.fake_screen.blit(game.alpha_surface, (0, 0))
    game.hyperspace_starfield.draw()