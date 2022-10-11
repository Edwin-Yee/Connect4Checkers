import numpy as np
import pygame
import random
import math
import sys

# Defining colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Creating the board
NUM_ROWS = 8
NUM_COLS = 8

# Initializing surface
SURFACE_WIDTH = 400
SURFACE_HEIGHT = 400
surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))

game_over = False

def initialize_board():
    game_board = np.zeros((NUM_ROWS, NUM_COLS))
    return game_board


def is_valid_position(game_board, row, col):
    if row >= 8 or col >= 8 or row < 0 or col < 0:
        return False  # Out of Bounds
    if game_board[row, col] == 1:
        return False  # Occupied space
    else:
        return True  # Not occupied


def draw_board():
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.rect(surface, GREEN,
            pygame.Rect(row*SURFACE_WIDTH/8, col*SURFACE_HEIGHT/8, SURFACE_WIDTH/8, SURFACE_HEIGHT/8))

# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((400, 300))

# Initialing Color
color = (255, 0, 0)

# Initializing the board
draw_board()
pygame.display.flip()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_position, y_position = pygame.mouse.get_pos()
            rect_width = 60
            rect_height = 60

            pygame.draw.rect(surface, RED, (x_position, y_position, rect_width, rect_height))
            pygame.display.flip()












