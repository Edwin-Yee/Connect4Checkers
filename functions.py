import numpy as np
import pygame
import random
import math
import sys
from Connect4Chess import global_
from classes import Sprite
from classes import BoardSquare
from player_functions import *
from global_ import *

def initialize_board():
    game_board = np.zeros((NUM_ROWS, NUM_COLS))
    return game_board


def is_valid_position(game_board, row, col):
    if row >= NUM_ROWS or col >= NUM_COLS or row < 0 or col < 0:
        return False  # Out of Bounds
    if game_board[row, col] == 1:
        return False  # Occupied space
    else:
        return True  # Not occupied


def draw_board():
    num = 0

    for row in range(NUM_ROWS):
        num = num + 1
        for col in range(NUM_COLS):
            num = num + 1

            # Drawing the game board visuals
            if row == 3 and col == 3 or row == 4 and col == 4:
                winning_board_square_silver_coords.append((row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            elif row == 3 and col == 4 or row == 4 and col == 3:
                winning_board_square_gold_coords.append((row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            elif num % 2 == 1:
                brown_board_square_coords.append((row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8))
                # pygame.draw.rect(surface, DARK_BROWN,
                # pygame.Rect(row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8,
                # SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8))
            else:
                black_board_square_coords.append((row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8))
                # pygame.draw.rect(surface, PALE_COLOR,
                # pygame.Rect(row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8,
                # SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8))

            if col == 0 or col == 1:
                # Generate red piece coordinates for the sprite
                red_pieces_coords.append((row * SURFACE_WIDTH / 8 + CIRCLE_RAD, col * SURFACE_HEIGHT / 8 + CIRCLE_RAD))

                # pygame.draw.circle(surface, RED, (row * SURFACE_WIDTH / 8 + CIRCLE_RAD,
                #                                    col * SURFACE_HEIGHT / 8 + CIRCLE_RAD), CIRCLE_RAD)

            if col == NUM_COLS-1 or col == NUM_COLS-2:
                # Generate black piece coordinates for the sprite
                black_pieces_coords.append((row * SURFACE_WIDTH / 8 + CIRCLE_RAD, col * SURFACE_HEIGHT / 8 + CIRCLE_RAD))

                # pygame.draw.circle(surface, BLACK, (row * SURFACE_WIDTH / 8 + CIRCLE_RAD,
                #                                     col * SURFACE_HEIGHT / 8 + CIRCLE_RAD), CIRCLE_RAD)

    # Create the sprites
    red_game_pieces = {}
    for count, coord in enumerate(red_pieces_coords):
        red_game_pieces["red_piece%d" % count] = Sprite(RED, CIRCLE_RAD, CIRCLE_RAD)
        red_game_pieces["red_piece%d" % count].rect.x = coord[0] - CIRCLE_RAD/2
        red_game_pieces["red_piece%d" % count].rect.y = coord[1] - CIRCLE_RAD/2

    black_game_pieces = {}
    for count, coord in enumerate(black_pieces_coords):
        black_game_pieces["black_piece%d" % count] = Sprite(BLACK, CIRCLE_RAD, CIRCLE_RAD)
        black_game_pieces["black_piece%d" % count].rect.x = coord[0] - CIRCLE_RAD/2
        black_game_pieces["black_piece%d" % count].rect.y = coord[1] - CIRCLE_RAD/2

    brown_squares = {}
    for count, coord in enumerate(brown_board_square_coords):
        brown_squares["brown_square%d" % count] = BoardSquare(DARK_BROWN, SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8)
        brown_squares["brown_square%d" % count].rect.x = coord[0]
        brown_squares["brown_square%d" % count].rect.y = coord[1]

    black_squares = {}
    for count, coord in enumerate(black_board_square_coords):
        black_squares["black_square%d" % count] = BoardSquare(PALE_COLOR, SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8)
        black_squares["black_square%d" % count].rect.x = coord[0]
        black_squares["black_square%d" % count].rect.y = coord[1]

    winning_squares_silver = {}
    for count, coord in enumerate(winning_board_square_silver_coords):
        winning_squares_silver["winning_square_silver%d" % count] = BoardSquare(SILVER, SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8)
        winning_squares_silver["winning_square_silver%d" % count].rect.x = coord[0]
        winning_squares_silver["winning_square_silver%d" % count].rect.y = coord[1]

    winning_squares_gold = {}
    for count, coord in enumerate(winning_board_square_gold_coords):
        winning_squares_gold["winning_square_gold%d" % count] = BoardSquare(GOLD, SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8)
        winning_squares_gold["winning_square_gold%d" % count].rect.x = coord[0]
        winning_squares_gold["winning_square_gold%d" % count].rect.y = coord[1]

    for i in red_game_pieces:
        all_sprites_list.add(red_game_pieces[i])

    for j in black_game_pieces:
        all_sprites_list.add(black_game_pieces[j])

    for k in brown_squares:
        squares_list.add(brown_squares[k])

    for p in black_squares:
        squares_list.add(black_squares[p])

    for t in winning_squares_silver:
        squares_list.add(winning_squares_silver[t])

    for m in winning_squares_gold:
        squares_list.add(winning_squares_gold[m])

