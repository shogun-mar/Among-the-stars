import pygame
from sys import exit
from starfield import Starfield
from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(RESOLUTION, FLAGS, vsync=1)
        pygame.display.set_caption("Among the stars")
        self.alpha_surface = pygame.Surface(RESOLUTION)
        self.alpha_surface.set_alpha(ALPHA_VALUE)
        self.clock = pygame.time.Clock()
        self.starfield = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            
            self.screen.blit(self.alpha_surface, (0,0)) 
            self.starfield.run()

            pygame.display.flip()
            self.clock.tick(MAX_FPS)

    def set_starfield(self, starfield):
        self.starfield = starfield