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
# References (for checkers minimax algorithm):
    # https://www.youtube.com/watch?v=mYbrH1Cl3nw

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

# Creating the board (Default: 8 rows, 8 columns)
NUM_ROWS = 8
NUM_COLS = 8

# Initializing surface (Default: scalar = 1, 400 x 400 surface)
global_scalar = 1.2
SURFACE_WIDTH = NUM_COLS * 50 * global_scalar
SURFACE_HEIGHT = NUM_ROWS * 50 * global_scalar

# CIRCLE_RAD = (SURFACE_WIDTH/NUM_COLS) / 4 * global_scalar
CIRCLE_RAD = 12.5 * global_scalar

game_over = False
red_wins = False
black_wins = False

sprite_count = 0

extra_space_for_score = SURFACE_WIDTH * 7/8 # (300)

surface = pygame.display.set_mode((SURFACE_WIDTH + extra_space_for_score, SURFACE_HEIGHT))
pygame.display.set_caption('Connect4Checkers')

# load in the shop button images
upgrade_img = pygame.image.load('imgs/upgrade_img.png').convert_alpha()
cancel_img = pygame.image.load('imgs/cancel_img.png').convert_alpha()
confirm_img = pygame.image.load('imgs/confirm_img.png').convert_alpha()
confirmation_sprite = pygame.sprite.Group()

player_red_score = 0
player_black_score = 0
player_state = 0

pygame.init()

smaller_font = pygame.font.Font("freesansbold.ttf", int(18 * global_scalar))
font = pygame.font.Font("freesansbold.ttf", int(24 * global_scalar))

current_turn_text_red_width, current_turn_text_red_height = smaller_font.size("Player with Red Pieces Turn")
current_turn_text_black_width, current_turn_text_black_height = smaller_font.size("Player with Black Pieces Turn")
score_red_text_width, score_red_text_height = font.size("Player Red Score: x")
score_black_text_width, score_black_text_height = font.size("Player Black Score: x")

textX = surface.get_width() * 5/8
red_textY = SURFACE_HEIGHT * 1/8
black_textY = red_textY + score_black_text_height * global_scalar + upgrade_img.get_height()
textY = red_textY + score_black_text_height * global_scalar + upgrade_img.get_height() + score_red_text_height * global_scalar + upgrade_img.get_height()

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

red_upgrade_state = False
black_upgrade_state = False
