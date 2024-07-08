import pygame
from sys import exit
from starfield import Starfield
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION, FLAGS, vsync=1)
        pygame.display.set_caption("Among the stars")
        self.alpha_surface = pygame.Surface(RESOLUTION)
        self.alpha_surface.set_alpha(ALPHA_VALUE)
        self.clock = pygame.time.Clock()

        self.starfield = None
        self.score_font = pygame.font.Font("graphics/score_font.ttf", 36)
        self.score: int = 0
        self.rendered_score = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.rendered_score_rect = self.rendered_score.get_rect(center = (WIDTH // 2, 50))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            
            self.screen.blit(self.alpha_surface, (0,0)) 
            self.starfield.run()
            self.screen.blit(self.rendered_score, self.rendered_score_rect)

            pygame.display.flip()
            self.clock.tick(MAX_FPS)

    def update_score(self, amount):
        self.score += amount
        self.rendered_score = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.rendered_score_rect = self.rendered_score.get_rect(center = (WIDTH // 2, 50))

    def set_starfield(self, starfield): #Not necessary if all classes were written in the same file but to better organize the code I separated each class into its own file
        self.starfield = starfield