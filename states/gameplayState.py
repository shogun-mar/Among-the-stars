import pygame
from states.gameState import GameState
from settings import *

def handle_gameplay_events(game, key):
    if key == PAUSE_KEY:
        game.game_state = GameState.PAUSE
    elif key == HYPERSPACE_KEY:
        current_time = pygame.time.get_ticks()
        temp_hyperspace_travel_time = current_time - game.last_hyperspace_travel_time
        if temp_hyperspace_travel_time > 0:
            game.game_state = GameState.HYPERSPACE
            game.last_hyperspace_travel_time = current_time
            game.hyperspace_travel_duration = temp_hyperspace_travel_time if temp_hyperspace_travel_time < game.hyperspace_travel_maximum_duration else game.hyperspace_travel_maximum_duration
            print(f"Travel time: {game.hyperspace_travel_duration}")
            game.alpha_surface.set_alpha(HYPERSPACE_ALPHA_VALUE)

def handle_gameplay_events_mouse(game, button, mouse_pos):
    if button == 1: #Left mouse button
        game.check_collisions(mouse_pos)

def render_gameplay(game):
    game.fake_screen.blit(game.alpha_surface, (0,0)) 
    game.game_starfield.draw()
    render_hyperspace_cooldown_bar(game)
    game.fake_screen.blit(game.rendered_score, game.rendered_score_rect)

def render_hyperspace_cooldown_bar(game):
    cooldown_percentage = (pygame.time.get_ticks() - game.last_hyperspace_travel_time) / game.hyperspace_travel_maximum_duration
    cooldown_width = int(SCREEN_WIDTH * cooldown_percentage)
    pygame.draw.rect(game.fake_screen, (255, 255, 255), (0, 0, cooldown_width, 10))
