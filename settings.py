import pygame
from pygame.locals import *

#Game Settings/Display Screen
WIDTH = 1000
HEIGHT = 650
TITLE = "Othello Game"

#Colors (r, g, b)
DARKTURQUOISE = (0, 206, 209)
DEEPPINK = (255, 20, 147)

#FONT
pygame.init()
FONT = pygame.font.SysFont("arialblack", 30)
player_color = 2 