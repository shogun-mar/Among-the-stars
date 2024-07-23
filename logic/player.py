from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from logic.game_star import vec2, vec3

class Player:
    def __init__(self, game_reference, pos):
        self.game = game_reference
        self.screen_pos = pos
        self.shooting_points_coords = vec2(SCREEN_WIDTH // 2, SCREEN_HEIGHT)
        self.pos3d = vec3(pos[0], pos[1], SCREEN_HEIGHT)
        
