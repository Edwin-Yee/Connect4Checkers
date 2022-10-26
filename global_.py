import numpy as np
import pygame
import random
import math
import sys

# References (for Python sprites):
    # https://realpython.com/lessons/creating-sprites/
    # https://www.geeksforgeeks.org/pygame-creating-sprites/
    # Button Sprite: https://stackoverflow.com/questions/39709065/making-pygame-sprites-disappear-in-python
# References (for closest number to k in list algorithm) used in Sprite move:
    # https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/

# This file holds all the global variables
# Defining colors

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PALE_COLOR = (255, 223, 145)
DARK_BROWN = (51, 39, 10)
WHITE = (255, 255, 255)

# Creating the board
NUM_ROWS = 8
NUM_COLS = 8

# Initializing surface
SURFACE_WIDTH = 400
SURFACE_HEIGHT = 400

CIRCLE_RAD = int((SURFACE_WIDTH/8)/2)
game_over = False
sprite_count = 0


surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))

buttons = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
squares_list = pygame.sprite.Group()
current_click_sprite_list = pygame.sprite.Group()
