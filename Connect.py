import numpy as np
import pygame
import random
import math
import sys

# References (for Python sprites):
    # https://realpython.com/lessons/creating-sprites/
    # https://www.geeksforgeeks.org/pygame-creating-sprites/

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

CIRCLE_RAD = (SURFACE_WIDTH/8)/2
game_over = False

# Initializing Pygame
pygame.init()
surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_color, width, height):
        super(Sprite, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(sprite_color)

        self.color = sprite_color

        self.rect = self.image.get_rect()

    def mouse_click_check(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            if self.color == RED:
                provide_legal_moves(self.rect.x, self.rect.y, RED)
            elif self.color == BLACK:
                provide_legal_moves(self.rect.x, self.rect.y, BLACK)

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

    red_pieces_coords = []
    black_pieces_coords = []

    for row in range(NUM_ROWS):
        num = num + 1
        for col in range(NUM_COLS):
            num = num + 1

            # Drawing the game board visuals
            if num % 2 == 1:
                pygame.draw.rect(surface, DARK_BROWN,
                pygame.Rect(row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8,
                SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8))
            else:
                pygame.draw.rect(surface, PALE_COLOR,
                pygame.Rect(row * SURFACE_WIDTH / 8, col * SURFACE_HEIGHT / 8,
                SURFACE_WIDTH / 8, SURFACE_HEIGHT / 8))

            if col == 0 or col == 1:
                # Generate coordinates for the sprite pieces
                # Red pieces coordinates
                red_pieces_coords.append((row * SURFACE_WIDTH / 8 + CIRCLE_RAD, col * SURFACE_HEIGHT / 8 + CIRCLE_RAD))

                # pygame.draw.circle(surface, RED, (row * SURFACE_WIDTH / 8 + CIRCLE_RAD,
                #                                    col * SURFACE_HEIGHT / 8 + CIRCLE_RAD), CIRCLE_RAD)

            # # Creating the Black Pieces as sprites
            if col == NUM_COLS-1 or col == NUM_COLS-2:
                # Generate coordinates for the sprite pieces
                # Black pieces coordinates
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
        red_game_pieces["black_piece%d" % count] = Sprite(BLACK, CIRCLE_RAD, CIRCLE_RAD)
        red_game_pieces["black_piece%d" % count].rect.x = coord[0] - CIRCLE_RAD/2
        red_game_pieces["black_piece%d" % count].rect.y = coord[1] - CIRCLE_RAD/2

    for i in red_game_pieces:
        all_sprites_list.add(red_game_pieces[i])

    for j in black_game_pieces:
        all_sprites_list.add(black_game_pieces[j])


# Legal moves are "jumping" over another piece in front of your piece. Pieces with no other pieces in
# front will have no legal moves.
def provide_legal_moves(x, y, color):
    print(x, y, color)
    if color == BLACK:
        if y - 2 * CIRCLE_RAD > 0 and surface.get_at((int(x), int(y - 2 * CIRCLE_RAD))) == BLACK:
            print("Legal move: ", (x, y - 2 * CIRCLE_RAD))
        if y - 2 * CIRCLE_RAD > 0 and x - 2 * CIRCLE_RAD > 0 and \
                surface.get_at((int(x - 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == BLACK:
            print("Legal move: ", (x - 2 * CIRCLE_RAD, y - 2 * CIRCLE_RAD))
        if y - 2 * CIRCLE_RAD > 0 and x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                surface.get_at((int(x + 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == BLACK:
            print("Legal move: ", (x + 2 * CIRCLE_RAD, y - 2 * CIRCLE_RAD))

    elif color == RED:
        if y + 2 * CIRCLE_RAD < SURFACE_HEIGHT and surface.get_at((int(x), int(y + 2 * CIRCLE_RAD))) == RED:
            print("Legal move: ", (x, y + 2 * CIRCLE_RAD))
        if y + 2 * CIRCLE_RAD < SURFACE_HEIGHT and x - 2 * CIRCLE_RAD > 0 and \
                surface.get_at((int(x - 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == RED:
            print("Legal move: ", (x - 2 * CIRCLE_RAD, y + 2 * CIRCLE_RAD))
        if y + 2 * CIRCLE_RAD < SURFACE_HEIGHT and x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                surface.get_at((int(x + 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == RED:
            print("Legal move: ", (x + 2 * CIRCLE_RAD, y + 2 * CIRCLE_RAD))



all_sprites_list = pygame.sprite.Group()

# Initializing the board
draw_board()
pygame.display.flip()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_position, y_position = pygame.mouse.get_pos()

            for sprite in all_sprites_list:
                sprite.mouse_click_check(x_position, y_position)

            pygame.display.flip()

    all_sprites_list.update()
    all_sprites_list.draw(surface)

    pygame.display.flip()