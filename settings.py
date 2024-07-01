import pygame

RESOLUTION = WIDTH, HEIGTH = (800, 600)
FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
MAX_FPS = 60

NUM_STARS = 500
vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3
CENTER = vec2(WIDTH // 2, HEIGTH // 2)
COLORS = 'red green blue yellow cyan magenta white'.split()
Z_DISTANCE = 40
SCALE_POS = 35