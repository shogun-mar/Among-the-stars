import pygame
from gameState import GameState
from settings import *

def handle_gameplay_events(game, key):
    if key == pygame.K_p:
        game.game_state = GameState.PAUSE

def handle_gameplay_events_mouse(game, button):
    if button == 1: #Left mouse button
        game.check_collisions()

def render_gameplay(game):
    game.fake_screen.blit(game.alpha_surface, (0,0)) 
    game.starfield.draw()
    game.fake_screen.blit(game.rendered_score, game.rendered_score_rect)