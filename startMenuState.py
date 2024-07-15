import pygame
from gameState import GameState
from settings import *

pygame.font.init()
logo_font = pygame.font.Font("graphics/Sterion-BLLld.ttf", 36)
logo_text = logo_font.render("Among the stars", True, (255, 255, 255))
logo_text_rect = logo_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT //2 - 50))

button_font = pygame.font.Font("graphics/Sterion-BLLld.ttf", 24)
play_text = button_font.render("Play", True, (255, 255, 255))
play_text_rect = play_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

help_text = button_font.render("Help", True, (255, 255, 255))
help_text_rect = help_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)) 

def handle_start_menu_events(game, key):
    pass

def handle_start_menu_events_mouse(game, button, mouse_pos):
    if play_text_rect.collidepoint(mouse_pos) and button == 1: #Left mouse button
        game.game_state = GameState.GAMEPLAY
    if help_text.collidepoint(mouse_pos) and button == 1:
        game.game_state = GameState.HELPMENU

def render_start_menu(game):
    game.fake_screen.fill((0, 0, 0))
    game.fake_screen.blit(logo_text, logo_text_rect)
    game.fake_screen.blit(play_text, play_text_rect)
    game.fake_screen.blit(help_text, help_text_rect)
