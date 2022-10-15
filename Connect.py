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
PALE_COLOR = (255, 223, 145)
DARK_BROWN = (51, 39, 10)

# Creating the board
NUM_ROWS = 8
NUM_COLS = 8

# Initializing surface
SURFACE_WIDTH = 400
SURFACE_HEIGHT = 400
surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))

CIRCLE_RAD = (SURFACE_WIDTH/8)/2
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
    num = 0

    # Black Pieces
    for row in range(NUM_ROWS):
        num = num + 1
        for col in range(NUM_COLS):
            num = num + 1
            if num % 2 == 1:
                pygame.draw.rect(surface, DARK_BROWN,
                pygame.Rect(row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8,
                SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8))
            else:
                pygame.draw.rect(surface, PALE_COLOR,
                pygame.Rect(row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8,
                SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8))

            # Red Pieces
            if col == 0 or col == 1:
                pygame.draw.circle(surface, RED, (row * SURFACE_WIDTH / 8 + CIRCLE_RAD,
                                                  col * SURFACE_HEIGHT / 8 + CIRCLE_RAD), CIRCLE_RAD)

            # Black Pieces
            if col == NUM_COLS-1 or col == NUM_COLS-2:
                pygame.draw.circle(surface, BLACK, (row * SURFACE_WIDTH / 8 + CIRCLE_RAD,
                                                    col * SURFACE_HEIGHT / 8 + CIRCLE_RAD), CIRCLE_RAD)







# Initializing Pygame
pygame.init()


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












