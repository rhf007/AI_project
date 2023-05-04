import pygame

WIDTH, HEIGHT = 700, 700

ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

BROWN = (80, 38, 17)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44,25))