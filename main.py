import numpy as np
import pygame
import random
import math
import sys

from Connect4Chess import global_
from global_ import *
from classes import Sprite
from classes import BoardSquare

# Initializing Pygame
pygame.init()


def draw_board():
    num = 0

    red_pieces_coords = []
    black_pieces_coords = []
    brown_board_square_coords = []
    black_board_square_coords = []

    for row in range(NUM_ROWS):
        num = num + 1
        for col in range(NUM_COLS):
            num = num + 1

            # Drawing the game board visuals
            if num % 2 == 1:
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

    for i in red_game_pieces:
        all_sprites_list.add(red_game_pieces[i])

    for j in black_game_pieces:
        all_sprites_list.add(black_game_pieces[j])

    for k in brown_squares:
        squares_list.add(brown_squares[k])

    for p in black_squares:
        squares_list.add(black_squares[p])



all_sprites_list = pygame.sprite.Group()
current_click_sprite_list = pygame.sprite.Group()
squares_list = pygame.sprite.Group()

# Initializing the board
draw_board()
squares_list.update()
squares_list.draw(surface)

pygame.display.flip()

num_click = 0
isButtonPressed = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_position, y_position = pygame.mouse.get_pos()

            for sprite in all_sprites_list:
                if sprite.mouse_click_check(x_position, y_position):
                    current_click_sprite_list.add(sprite)
                    print("Added sprite", sprite.name, "to current_click_sprite_list")

            for button in buttons:
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicked = pygame.mouse.get_pressed()[0]
                if button.rect.collidepoint(mouse_pos) and mouse_clicked:
                    print("BUTTON PRESSED!")
                    current_click_sprite_list.sprites()[0].move(x_position, y_position)
                    isButtonPressed = True

                elif not isButtonPressed and num_click % 2 == 1 and not (
                        button.rect.collidepoint(*mouse_pos) and mouse_clicked):
                    print("Removed all buttons")
                    current_click_sprite_list.empty()
                    for button2 in buttons:
                        button2.kill()
                        surface.fill(WHITE)
                        pygame.display.flip()
            isButtonPressed = False
            num_click = num_click + 1
            pygame.display.flip()

    # Update the board squares
    squares_list.update()
    squares_list.draw(surface)

    # Draws all sprites to the given Surface.
    buttons.update()  # Calls the update method on every sprite in the group.
    buttons.draw(surface)
    all_sprites_list.update()
    all_sprites_list.draw(surface)

    pygame.display.update()

    pygame.display.flip()

