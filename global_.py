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
# References (for Neat Python tutorial):
    # Python Pong AI Tutorial - Using NEAT, Tech With Tim, https://www.youtube.com/watch?v=2f6TmKm7yx0
    # Python Flappy Bird AI Tutorial (with NEAT) - NEAT Configuration and Explanation, Tech With Tim,
    # https://www.youtube.com/watch?v=MPFWsRjDmnU&t=747s

# This file holds all the global variables
# Defining colors

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PALE_COLOR = (255, 223, 145)
DARK_BROWN = (51, 39, 10)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GOLD = (255, 223, 0)
SILVER = (192, 192, 192)

# Creating the board
NUM_ROWS = 8
NUM_COLS = 8

# Initializing surface (400 x 400)
SURFACE_WIDTH = NUM_COLS * 50
SURFACE_HEIGHT = NUM_ROWS * 50

CIRCLE_RAD = int((SURFACE_WIDTH/NUM_COLS)/2)
game_over = False
red_wins = False
black_wins = False

sprite_count = 0

extra_space_for_score = SURFACE_WIDTH * 6/8 # (300)

surface = pygame.display.set_mode((SURFACE_WIDTH + extra_space_for_score, SURFACE_HEIGHT))

buttons = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
squares_list = pygame.sprite.Group()
current_click_sprite_list = pygame.sprite.Group()

red_pieces_coords = []
black_pieces_coords = []
brown_board_square_coords = []
black_board_square_coords = []
winning_board_square_silver_coords = []
winning_board_square_gold_coords = []

silver_top_occupied = None
silver_bottom_occupied = None
gold_top_occupied = None
gold_bottom_occupied = None

