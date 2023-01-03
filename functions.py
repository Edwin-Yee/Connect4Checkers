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
                brown_board_square_coords.append((row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            else:
                black_board_square_coords.append((row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            if col == 0 or col == 1:
                # Generate red piece coordinates for the sprite
                red_pieces_coords.append((row * SURFACE_WIDTH / NUM_COLS + CIRCLE_RAD, col * SURFACE_HEIGHT / NUM_ROWS + CIRCLE_RAD))
            if col == NUM_COLS-1 or col == NUM_COLS-2:
                # Generate black piece coordinates for the sprite
                black_pieces_coords.append((row * SURFACE_WIDTH / NUM_COLS + CIRCLE_RAD, col * SURFACE_HEIGHT / NUM_ROWS + CIRCLE_RAD))

    # Create the sprites
    red_game_pieces = {}
    for count, coord in enumerate(red_pieces_coords):
        red_game_pieces["red_piece%d" % count] = Sprite(RED, CIRCLE_RAD * 2, CIRCLE_RAD * 2)
        red_game_pieces["red_piece%d" % count].rect.x = coord[0]
        red_game_pieces["red_piece%d" % count].rect.y = coord[1]

    black_game_pieces = {}
    for count, coord in enumerate(black_pieces_coords):
        black_game_pieces["black_piece%d" % count] = Sprite(BLACK, CIRCLE_RAD * 2, CIRCLE_RAD * 2)
        black_game_pieces["black_piece%d" % count].rect.x = coord[0]
        black_game_pieces["black_piece%d" % count].rect.y = coord[1]

    brown_squares = {}
    for count, coord in enumerate(brown_board_square_coords):
        brown_squares["brown_square%d" % count] = BoardSquare(DARK_BROWN, SURFACE_WIDTH / NUM_COLS, SURFACE_HEIGHT / NUM_ROWS)
        brown_squares["brown_square%d" % count].rect.x = coord[0]
        brown_squares["brown_square%d" % count].rect.y = coord[1]

    black_squares = {}
    for count, coord in enumerate(black_board_square_coords):
        black_squares["black_square%d" % count] = BoardSquare(PALE_COLOR, SURFACE_WIDTH / NUM_COLS, SURFACE_HEIGHT / NUM_ROWS)
        black_squares["black_square%d" % count].rect.x = coord[0]
        black_squares["black_square%d" % count].rect.y = coord[1]

    winning_squares_silver = {}
    for count, coord in enumerate(winning_board_square_silver_coords):
        winning_squares_silver["winning_square_silver%d" % count] = BoardSquare(SILVER, SURFACE_WIDTH / NUM_COLS, SURFACE_HEIGHT / NUM_ROWS)
        winning_squares_silver["winning_square_silver%d" % count].rect.x = coord[0]
        winning_squares_silver["winning_square_silver%d" % count].rect.y = coord[1]

    winning_squares_gold = {}
    for count, coord in enumerate(winning_board_square_gold_coords):
        winning_squares_gold["winning_square_gold%d" % count] = BoardSquare(GOLD, SURFACE_WIDTH / NUM_COLS, SURFACE_HEIGHT / NUM_ROWS)
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


def remove_buttons():
    for inner_button in buttons:
        inner_button.kill()
        pygame.display.flip()


def remove_captured_sprite(button, inner_all_sprites_list, inner_player_state):
    button_x = button.get_position()[0]
    button_y = button.get_position()[1]
    sprite_x = 0
    sprite_y = 0

    if get_current_player(inner_player_state) == 'Red':  # Red on the top
        if button.get_state() == "Vertical Capture":
            sprite_x = button_x
            sprite_y = button_y - 4 * CIRCLE_RAD 
        elif button.get_state() == "Left Diagonal Capture":
            sprite_x = button_x + 4 * CIRCLE_RAD
            sprite_y = button_y - 4 * CIRCLE_RAD
        elif button.get_state() == "Right Diagonal Capture":
            sprite_x = button_x - 4 * CIRCLE_RAD
            sprite_y = button_y - 4 * CIRCLE_RAD
    elif get_current_player(inner_player_state) == 'Black':  # Black on the bottom
        if button.get_state() == "Vertical Capture":
            sprite_x = button_x
            sprite_y = button_y + 4 * CIRCLE_RAD
        elif button.get_state() == "Left Diagonal Capture":
            sprite_x = button_x + 4 * CIRCLE_RAD
            sprite_y = button_y + 4 * CIRCLE_RAD
        elif button.get_state() == "Right Diagonal Capture":
            sprite_x = button_x - 4 * CIRCLE_RAD
            sprite_y = button_y + 4 * CIRCLE_RAD

    for inner_sprite in inner_all_sprites_list:
        # print(inner_sprite.rect.x, inner_sprite.rect.y, sprite_x, sprite_y)
        if inner_sprite.rect.x == sprite_x and inner_sprite.rect.y == sprite_y:
            print(get_current_player(inner_player_state), "Removed sprite located at:", sprite_x, sprite_y)
            inner_all_sprites_list.remove(inner_sprite)

    return inner_all_sprites_list


def check_silver_gold_squares(silver_top_occupied_inner, silver_bottom_occupied_inner, gold_top_occupied_inner,
                              gold_bottom_occupied_inner, game_over_inner, red_wins_inner, black_wins_inner):
    # Note: register after landing (have to stay there for until opponent's turn finishes)

    # Check Silver and Gold squares
    if surface.get_at((int(winning_board_square_silver_coords[0][0] + CIRCLE_RAD * 2/2), int(winning_board_square_silver_coords[0][1] + CIRCLE_RAD * 2/2)))[:3] == RED:
        silver_top_occupied_inner = 'Red'
        print("LANDED ON TOP LEFT SILVER RED")
    elif surface.get_at((int(winning_board_square_silver_coords[0][0] + CIRCLE_RAD * 2/2), int(winning_board_square_silver_coords[0][1] + CIRCLE_RAD * 2/2)))[:3] == BLACK:
        silver_top_occupied_inner = 'Black'
        print("LANDED ON TOP LEFT SILVER BLACK")
    else:
        silver_top_occupied_inner = None

    if surface.get_at((int(winning_board_square_silver_coords[1][0] + CIRCLE_RAD * 2/2), int(winning_board_square_silver_coords[1][1] + CIRCLE_RAD * 2/2)))[:3] == RED:
        silver_bottom_occupied_inner = 'Red'
        print("LANDED ON BOTTOM RIGHT SILVER RED")
    elif surface.get_at((int(winning_board_square_silver_coords[1][0] + CIRCLE_RAD * 2/2), int(winning_board_square_silver_coords[1][1] + CIRCLE_RAD * 2/2)))[:3] == BLACK:
        silver_bottom_occupied_inner = 'Black'
        print("LANDED ON BOTTOM RIGHT SILVER BLACK")
    else:
        silver_bottom_occupied_inner = None

    if surface.get_at((int(winning_board_square_gold_coords[0][0] + CIRCLE_RAD * 2 / 2),
                       int(winning_board_square_gold_coords[0][1] + CIRCLE_RAD * 2 / 2)))[:3] == RED:
        gold_top_occupied_inner = 'Red'
    elif surface.get_at((int(winning_board_square_gold_coords[0][0] + CIRCLE_RAD * 2 / 2),
                       int(winning_board_square_gold_coords[0][1] + CIRCLE_RAD * 2 / 2)))[:3] == BLACK:
        gold_top_occupied_inner = 'Black'
    else:
        gold_top_occupied_inner = None

    if surface.get_at((int(winning_board_square_gold_coords[1][0] + CIRCLE_RAD * 2 / 2),
                       int(winning_board_square_gold_coords[1][1] + CIRCLE_RAD * 2 / 2)))[:3] == RED:
        gold_bottom_occupied_inner = 'Red'
    elif surface.get_at((int(winning_board_square_gold_coords[1][0] + CIRCLE_RAD * 2 / 2),
                       int(winning_board_square_gold_coords[1][1] + CIRCLE_RAD * 2 / 2)))[:3] == BLACK:
        gold_bottom_occupied_inner = 'Black'
    else:
        gold_bottom_occupied_inner = None

    # Check winning connect (All 4 middle winning squares are occupied)
    if silver_top_occupied == 'Red' and silver_bottom_occupied == 'Red' and gold_top_occupied == 'Red' and \
            gold_bottom_occupied == 'Red':
        game_over_inner = True
        red_wins_inner = True

    elif silver_top_occupied == 'Black' and silver_bottom_occupied == 'Black' and gold_top_occupied == 'Black' and \
            gold_bottom_occupied == 'Black':
        game_over_inner = True
        black_wins_inner = True

    return silver_top_occupied_inner, silver_bottom_occupied_inner, gold_top_occupied_inner, \
           gold_bottom_occupied_inner, game_over_inner, red_wins_inner, black_wins_inner

