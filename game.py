import pygame
from os import environ
from sys import exit
from ctypes import windll
from settings import *

class Game:
    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1' #Center the Pygame window Comando di SDL per centrare la finestra
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION, FLAGS, vsync=1)
        self.fake_screen = self.screen.copy()
        window_icon = pygame.image.load("graphics/icon.png")
        pygame.display.set_icon(window_icon)
        pygame.display.set_caption("Among the stars")
        self.alpha_surface = pygame.Surface(RESOLUTION)
        self.alpha_surface.set_alpha(ALPHA_VALUE)
        self.clock = pygame.time.Clock()
        pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.QUIT, pygame.KEYDOWN, pygame.VIDEORESIZE]) # Allow only specific events (for performance reasons)

        #Starfield object
        self.starfield = None
        
        #Game variables
        self.score_font = pygame.font.Font("graphics/score_font.ttf", 36)
        self.score: int = 0
        self.rendered_score = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.rendered_score_rect = self.rendered_score.get_rect(center = (SCREEN_WIDTH // 2, 50))

        self.action_cooldown: int = 1000  # Cooldown in milliseconds
        self.last_action_time: int = 0  # Time of the last action

        # Get physical resolution
        self.hw_screen_width, self.hw_screen_height  = self.get_hw_resolution()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.quit_game()
                elif event.type == pygame.VIDEORESIZE: self.screen = pygame.display.set_mode((event.w, event.h), FLAGS, vsync=1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.quit_game() 
                    if event.key == FULLSCREEN_KEY:  #Toggle fullscreen (explores all possible configurations because some drivers may not support all)
                        if not(pygame.display.get_surface().get_size() == (self.hw_screen_width, self.hw_screen_height)): #Windowed borderless to increase probability of compatibility and so switching to other windows is easier
                            self.alpha_surface = pygame.transform.scale(self.alpha_surface, (self.hw_screen_width, self.hw_screen_height))
                            try:
                                self.screen = pygame.display.set_mode((self.hw_screen_width, self.hw_screen_height), FLAGS | pygame.NOFRAME | pygame.SCALED, vsync=1)
                            except Exception:
                                self.screen = pygame.display.set_mode((self.hw_screen_width, self.hw_screen_height), FLAGS | pygame.NOFRAME)
                        else:
                            self.alpha_surface = pygame.transform.scale(self.alpha_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
                            try:
                                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS | pygame.SCALED, vsync=1)         
                            except Exception:
                                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS)
            
            pygame.display.set_caption(f"PokèScrauso - FPS: {int(self.clock.get_fps())}") #Update window caption with current FPS

            self.fake_screen.blit(self.alpha_surface, (0,0)) 
            self.starfield.run()
            self.fake_screen.blit(self.rendered_score, self.rendered_score_rect)

            self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (0, 0)) #Scale the fake screen to the current screen size
            pygame.display.flip()
            self.clock.tick(MAX_FPS)

    def update_score(self, amount):
        self.score += amount
        self.rendered_score = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.rendered_score_rect = self.rendered_score.get_rect(center = (SCREEN_WIDTH // 2, 50))

    def set_starfield(self, starfield): #Not necessary if all classes were written in the same file but to better organize the code I separated each class into its own file
        self.starfield = starfield

    def check_collisions(self):
        if pygame.mouse.get_pressed()[0]:  # Separated the two conditions to call get_ticks only when needed
            current_time = pygame.time.get_ticks()
            if current_time - self.last_action_time > self.action_cooldown:
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                self.last_action_time = current_time  # Update last action time
                for enemy in list(self.starfield.enemies):  # Make a shallow copy for safe removal
                    if enemy.rect.collidepoint(mouse_pos):
                        self.starfield.enemies.remove(enemy)  # Correctly remove the enemy from the list
                        self.update_score(1)

    def quit_game(self):
        pygame.quit()
        quit()

    def get_hw_resolution(self):
        # Get a handle to the desktop window
        desktop = windll.user32.GetDesktopWindow()
        # Get a handle to the device context for the desktop window
        dc = windll.user32.GetWindowDC(desktop)
        # Get the physical resolution
        hw_screen_width = windll.gdi32.GetDeviceCaps(dc, 8)  # HORIZONTAL RES
        hw_screen_height = windll.gdi32.GetDeviceCaps(dc, 10)  # VERTICAL RES
        # Release the device context
        windll.user32.ReleaseDC(desktop, dc)

        return hw_screen_width, hw_screen_height   