import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from logic.game_star import vec3

class Player:
    def __init__(self, game_reference, pos):
        self.game = game_reference
        self.sprite = pygame.image.load("graphics/spaceship_player.png").convert_alpha()
        self.rect = self.sprite.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        self.screen_pos = pos
        self.pos3d = vec3(pos[0], pos[1], SCREEN_HEIGHT)        

    @property
    def shooting_points_coords(self):
        return self.rect.midtop