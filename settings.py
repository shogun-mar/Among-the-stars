import pygame

RESOLUTION = SCREEN_WIDTH,  SCREEN_HEIGHT = (1200, 500)
FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
MAX_FPS = 60

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3
CENTER = vec2(SCREEN_WIDTH // 2,  SCREEN_HEIGHT // 2)
SCALE_POS = 35
INITIAL_SIZE = 5
MAX_NUM_ENEMIES_SCREEN = 4
ENEMY_RESPAWN_COOLDOWN = 3 #Expressed in seconds

#Keybinds
FULLSCREEN_KEY = pygame.K_f

#Game variables
ROTATION_VELOCITY = 0.1

#For starfield
NUM_STARS = 1500
COLORS = 'red green blue yellow cyan magenta white'.split()
Z_DISTANCE = 40
ALPHA_VALUE = 128

#For hyperspace tunnel 
# COLORS = 'blue cyan skyblue purple magenta'.split()
# Z_DISTANCE = 140
# ALPHA_VALUE = 30
# NUM_STARS = 2000