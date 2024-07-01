import pygame

RESOLUTION = WIDTH, HEIGTH = (1600, 900)
FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
MAX_FPS = 60

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3
CENTER = vec2(WIDTH // 2, HEIGTH // 2)
SCALE_POS = 35


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