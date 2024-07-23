import pygame
from logic.states.gameState import GameState
from settings import *

pygame.font.init()
font = pygame.font.Font("graphics/Sterion-BLLld.ttf", 48)

game_over_text = font.render("Game Over", True, (255, 255, 255))
game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

button_font = pygame.font.Font("graphics/SterionItalic-R99PA.ttf", 36)

play_text = button_font.render("Play again", True, (255, 255, 255))
play_text_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

exit_text = button_font.render("Exit", True, (255, 255, 255))
exit_text_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

def handle_gameover_events_mouse(game, button, mouse_pos):
    if play_text_rect.collidepoint(mouse_pos) and button == 1:
        game.game_state = GameState.GAMEPLAY
        game.alpha_surface.set_alpha(GAMEPLAY_ALPHA_VALUE)
        game.last_hyperspace_travel_time = pygame.time.get_ticks()
        game.last_attack_time = pygame.time.get_ticks()

def render_gameover_menu(game):
    game.fake_screen.fill((0, 0, 0))
    game.hyperspace_starfield.draw()
    game.fake_screen.blit(game_over_text,  game_over_text_rect)
    game.fake_screen.blit(play_text, play_text_rect)
