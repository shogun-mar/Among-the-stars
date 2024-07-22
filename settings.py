import pygame

RESOLUTION = SCREEN_WIDTH,  SCREEN_HEIGHT = (1600, 900)
FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
MAX_FPS = 60

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3
CENTER = vec2(SCREEN_WIDTH // 2,  SCREEN_HEIGHT // 2)
SCALE_POS = 35
STAR_ROTATION_VELOCITY = 2
MAX_NUM_ENEMIES_SCREEN = 4
ENEMY_RESPAWN_COOLDOWN = 3 #Expressed in seconds

DEMO_STARS_NUM = 1000
DEMO_STAR_INITIAL_SIZE = 5
START_MENU_ALPHA_VALUE = 128

#Keybinds
FULLSCREEN_KEY = pygame.K_f

#Game variables
ROTATION_VELOCITY = 0.1

#For starfield
NUM_STARS = 350
STARFIELD_COLORS = 'red green blue yellow cyan magenta white'.split()
Z_DISTANCE = 40
ALPHA_VALUE = 128

#For hyperspace tunnel 
TUNNEL_COLORS = 'blue cyan skyblue purple magenta'.split()
# Z_DISTANCE = 140
# ALPHA_VALUE = 30
# NUM_STARS = 2000