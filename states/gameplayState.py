import pygame
from states.gameState import GameState
from settings import *

def handle_gameplay_events(game, key):
    if key == PAUSE_KEY:
        game.game_state = GameState.PAUSE
    elif key == HYPERSPACE_KEY:
        game.game_state = GameState.HYPERSPACE
        game.alpha_surface.set_alpha(HYPERSPACE_ALPHA_VALUE)

def handle_gameplay_events_mouse(game, button, mouse_pos):
    if button == 1: #Left mouse button
        game.check_collisions(mouse_pos)

def render_gameplay(game):
    game.fake_screen.blit(game.alpha_surface, (0,0)) 
    game.game_starfield.draw()
    game.fake_screen.blit(game.rendered_score, game.rendered_score_rect)