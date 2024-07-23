import pygame
from logic.states.gameState import GameState
from settings import *

pygame.font.init()

font = pygame.font.Font("graphics/Sterion-BLLld.ttf", 20)

help_text = (
    "Your objective is to survive as long as possible.\n"
    "Shoot using the left mouse button.\n"
    "Rotate your spaceship with the right mouse button.\n"
    "Escape danger using hyperspace with the E key.\n"
    "At the cost of one life point and by pressing Q you can activate a shield\n"
    "which will reflected any projectiles coming your way.\n"
    "Shoot at red rocks to gain points, green ones to gain health \n"
    "and increase max life points if at the max and white ones to gain hyperspace energy.\n"
    "Pause with P, toggle fullscreen with F, and exit with ESCAPE.\n"
    "Good luck!"
)

rendered_help_text = font.render(help_text, True, (255, 255, 255))
rendered_help_text_rect = rendered_help_text.get_rect(center = (10, SCREEN_HEIGHT // 2))

button_font = pygame.font.Font("graphics/SterionItalic-R99PA.ttf", 36)

play_text = button_font.render("Play", True, (255, 255, 255))
play_text_rect = play_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300))

def handle_help_menu_events(game, key):
    pass

def handle_help_menu_events_mouse(game, button, mouse_pos):
    if button == 1 and play_text_rect.collidepoint(mouse_pos): # Check if the left mouse button is pressed and the mouse is over the play button
        game.game_state = GameState.GAMEPLAY
        game.alpha_surface.set_alpha(GAMEPLAY_ALPHA_VALUE)

def render_help_menu(game):
    game.fake_screen.fill((0, 0, 0))
    start_y = SCREEN_HEIGHT // 2 - (len(help_text.split('\n')) * 30) // 2  # Center the block of text vertically

    for i, line in enumerate(help_text.split('\n')):
        rendered_line = font.render(line, True, (255, 255, 255))
        line_rect = rendered_line.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 30))
        game.fake_screen.blit(rendered_line, line_rect)

    game.fake_screen.blit(play_text, play_text_rect)
    game.fake_screen.blit(game.decoration_sprite, game.decoration_sprite_rect)
    game.fake_screen.blit(game.decoration_projectile, game.decoration_projectile_rect)
    game.fake_screen.blit(game.decoration_powerups, game.decoration_powerups_rect)
    game.fake_screen.blit(game.decoration_hearts, game.decoration_hearts_rect)