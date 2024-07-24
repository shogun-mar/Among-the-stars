import pygame
from logic.states.gameState import GameState
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAMEPLAY_ALPHA_VALUE

pygame.font.init()
font = pygame.font.Font("graphics/Sterion-BLLld.ttf", 48)

pause_text = font.render("Pause", True, (255, 255, 255))
pause_text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

button_font = pygame.font.Font("graphics/SterionItalic-R99PA.ttf", 36)

play_text = button_font.render("Play", True, (255, 255, 255))
play_text_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))

exit_text = button_font.render("Exit", True, (255, 255, 255))
exit_text_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 100))

def handle_pause_menu_events_mouse(game, button, mouse_pos):
    if play_text_rect.collidepoint(mouse_pos) and button == 1:
        game.game_state = GameState.GAMEPLAY
        game.alpha_surface.set_alpha(GAMEPLAY_ALPHA_VALUE)
        game.last_hyperspace_travel_time = game.current_time
        game.last_attack_time = game.current_time
        game.last_shield_activation_time = game.current_time
    elif exit_text_rect.collidepoint(mouse_pos) and button == 1:
        game.quit_game()

def render_pause_menu(game):
    game.fake_screen.blit(game.alpha_surface, (0, 0))
    game.hyperspace_starfield.draw()
    game.fake_screen.blit(pause_text, pause_text_rect)
    game.fake_screen.blit(play_text, play_text_rect)
    game.fake_screen.blit(exit_text, exit_text_rect)