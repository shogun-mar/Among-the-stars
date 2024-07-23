import pygame
from os import environ
from random import randint
from sys import exit
from ctypes import windll
from settings import *
from states.gameState import GameState
from states.gameplayState import *
from states.startMenuState import *
from states.hyperspaceState import *
from states.helpMenuState import *

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
        self.alpha_surface.set_alpha(HYPERSPACE_ALPHA_VALUE)
        self.clock = pygame.time.Clock()
        pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL, pygame.QUIT, pygame.KEYDOWN, pygame.VIDEORESIZE]) # Allow only specific events (for performance reasons)

        #Starfield objects
        self.game_starfield = None
        self.hyperspace_starfield = None
        
        #Game variables
        self.game_state = GameState.STARTMENU
        self.darkened_surface = pygame.Surface(self.fake_screen.get_size())

        self.score_font = pygame.font.Font("graphics/score_font.ttf", 36)
        self.score: int = 0
        self.rendered_score = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.rendered_score_rect = self.rendered_score.get_rect(center = (SCREEN_WIDTH // 2, 50))

        self.attack_cooldown: int = ATTACK_COOLDOWN
        self.last_attack_time: int = 0  # Time of the last action

        self.hyperspace_travel_maximum_duration: int = 5000 #Maximum time for the hyperspace travel in milliseconds
        self.hyperspace_travel_duration: int = 0 #Duration of the hyperspace travel in milliseconds
        self.last_hyperspace_travel_time: int = 0 #Time of the last hyperspace travel
        self.last_exit_from_hyperspace_time: int = 0 #Time of the last exit from hyperspace

        self.life_points: int = 3

        #Help menu stuff
        self.decoration_sprite = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("graphics/spaceship_enemy.png").convert_alpha(), 90), (250, 250))
        self.decoration_sprite_rect = self.decoration_sprite.get_rect(topleft = (30, 30))

        self.decoration_projectile = pygame.transform.rotate(pygame.image.load("graphics/projectile.png").convert_alpha(), 90)
        self.decoration_projectile_rect = self.decoration_projectile.get_rect(midleft = (self.decoration_sprite_rect.midright[0] + 10, self.decoration_sprite_rect.midright[1]))

        # Get physical resolution
        self.hw_screen_width, self.hw_screen_height  = self.get_hw_resolution()

    def run(self):
        while True:
            self.handle_events()
            self.update_logic()
            self.render()
            
    def handle_events(self):
        for event in pygame.event.get():
                #General events
                if event.type == pygame.QUIT: self.quit_game()
                elif event.type == pygame.VIDEORESIZE: self.screen = pygame.display.set_mode((event.w, event.h), FLAGS, vsync=1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.quit_game() 
                    elif event.key == FULLSCREEN_KEY:  #Toggle fullscreen (explores all possible configurations because some drivers may not support all)
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
                
                    #Gamestate specific events
                    elif self.game_state == GameState.GAMEPLAY:
                        handle_gameplay_events(self, event.key)
                    
                    elif self.game_state == GameState.STARTMENU:
                        handle_start_menu_events(self, event.key)

                    elif self.game_state == GameState.HYPERSPACE:
                        handle_hyperspace_events(self, event.key)
                    
                    elif self.game_state == GameState.HELPMENU:
                        handle_help_menu_events(self, event.key)

                #Mouse related events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == GameState.GAMEPLAY: handle_gameplay_events_mouse(self, event.button, pygame.mouse.get_pos())
                    elif self.game_state == GameState.STARTMENU: handle_start_menu_events_mouse(self, event.button, pygame.mouse.get_pos())           
                    elif self.game_state == GameState.HELPMENU: handle_help_menu_events_mouse(self, event.button, pygame.mouse.get_pos())

    def update_logic(self):
        pygame.display.set_caption(f"Among the stars - FPS: {int(self.clock.get_fps())}") #Update window caption with current FPS
        if self.game_state == GameState.GAMEPLAY:
            self.game_starfield.update(self)
            
            #if self.life_points == 0: self.quit_game()

        elif self.game_state == GameState.STARTMENU:
            self.hyperspace_starfield.update(self)
        elif self.game_state == GameState.HYPERSPACE:
            self.hyperspace_starfield.update(self)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hyperspace_travel_time > self.hyperspace_travel_duration:
                self.last_exit_from_hyperspace_time = current_time
                exit_from_hyperspace(self)
        elif self.game_state == GameState.HELPMENU:
            self.decoration_sprite_rect.midright = self.decoration_sprite_rect.midright[0] + 5, self.decoration_sprite_rect.midright[1]
            if self.decoration_sprite_rect.midright[0] > SCREEN_WIDTH - 25: self.decoration_sprite_rect.midleft = 25, self.decoration_sprite_rect.midright[1]

            self.decoration_projectile_rect.midleft = self.decoration_sprite_rect.midright[0] + 10, self.decoration_sprite_rect.midright[1]
            if self.decoration_projectile_rect.midleft[0] > SCREEN_WIDTH - 25: self.decoration_projectile_rect.midleft = 25, self.decoration_projectile_rect.midright[1]



    def render(self):
        if self.game_state == GameState.GAMEPLAY: render_gameplay(self)
        elif self.game_state == GameState.STARTMENU: render_start_menu(self)
        elif self.game_state == GameState.HYPERSPACE: render_hyperspace(self)
        elif self.game_state == GameState.HELPMENU: render_help_menu(self)
        elif self.game_state == GameState.PAUSE:
            pass

        self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (0, 0)) #Scale the fake screen to the current screen size
        pygame.display.flip()
        self.clock.tick(MAX_FPS)

    def update_score(self, amount):
        self.score += amount
        self.rendered_score = self.score_font.render(f"Score:{self.score}", True, (255, 255, 255))
        self.rendered_score_rect = self.rendered_score.get_rect(center = (SCREEN_WIDTH // 2, 50))

    def quit_game(self):
        pygame.quit()
        exit()

    def set_starfield(self, game_starfield): #Not necessary if all classes were written in the same file but to better organize the code I separated each class into its own file
        self.game_starfield = game_starfield

    def set_hyperspace_starfield(self, hyperspace_starfield): #Not necessary if all classes were written in the same file but to better organize the code I separated each class into its own file
        self.hyperspace_starfield = hyperspace_starfield

    def get_hw_resolution(self):
        # Get a handle to the desktop window
        desktop = windll.user32.GetDesktopWindow()
        # Get a handle to the device context for the desktop window
        dc = windll.user32.GetWindowDC(desktop)
        # Get the physical resolution
        hw_screen_width = windll.gdi32.GetDeviceCaps(dc, 8) # HORIZONTAL RES
        hw_screen_height = windll.gdi32.GetDeviceCaps(dc, 10) # VERTICAL RES
        # Release the device context
        windll.user32.ReleaseDC(desktop, dc)

        return hw_screen_width, hw_screen_height   