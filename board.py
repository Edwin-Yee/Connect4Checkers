import pygame
from global_ import NUM_ROWS, NUM_COLS, RED, BLACK, DARK_BROWN, PALE_COLOR, CIRCLE_RAD, SURFACE_WIDTH, SURFACE_HEIGHT, \
    winning_board_square_gold_coords, winning_board_square_silver_coords, brown_board_square_coords, \
    black_board_square_coords, red_pieces_coords, black_pieces_coords, all_sprites_list, squares_list, SILVER, GOLD
from classes import Sprite, BoardSquare

# code adapted from https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py

def draw_squares(window):
    window.fill(DARK_BROWN)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.rect(window, PALE_COLOR, (row * CIRCLE_RAD * 4, col * CIRCLE_RAD * 4, CIRCLE_RAD * 4, CIRCLE_RAD * 4))


def draw_board():
    num = 0

    for row in range(NUM_ROWS):
        num = num + 1
        for col in range(NUM_COLS):
            num = num + 1

            # Drawing the game board visuals
            if row == 3 and col == 3 or row == 4 and col == 4:
                winning_board_square_silver_coords.append(
                    (row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            elif row == 3 and col == 4 or row == 4 and col == 3:
                winning_board_square_gold_coords.append(
                    (row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            elif num % 2 == 1:
                brown_board_square_coords.append((row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            else:
                black_board_square_coords.append((row * SURFACE_WIDTH / NUM_COLS, col * SURFACE_HEIGHT / NUM_ROWS))
            if col == 0 or col == 1:
                # Generate red piece coordinates for the sprite
                red_pieces_coords.append(
                    (row * SURFACE_WIDTH / NUM_COLS + CIRCLE_RAD, col * SURFACE_HEIGHT / NUM_ROWS + CIRCLE_RAD))
            if col == NUM_COLS - 1 or col == NUM_COLS - 2:
                # Generate black piece coordinates for the sprite
                black_pieces_coords.append(
                    (row * SURFACE_WIDTH / NUM_COLS + CIRCLE_RAD, col * SURFACE_HEIGHT / NUM_ROWS + CIRCLE_RAD))

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
        brown_squares["brown_square%d" % count] = BoardSquare(DARK_BROWN, SURFACE_WIDTH / NUM_COLS,
                                                              SURFACE_HEIGHT / NUM_ROWS)
        brown_squares["brown_square%d" % count].rect.x = coord[0]
        brown_squares["brown_square%d" % count].rect.y = coord[1]

    black_squares = {}
    for count, coord in enumerate(black_board_square_coords):
        black_squares["black_square%d" % count] = BoardSquare(PALE_COLOR, SURFACE_WIDTH / NUM_COLS,
                                                              SURFACE_HEIGHT / NUM_ROWS)
        black_squares["black_square%d" % count].rect.x = coord[0]
        black_squares["black_square%d" % count].rect.y = coord[1]

    winning_squares_silver = {}
    for count, coord in enumerate(winning_board_square_silver_coords):
        winning_squares_silver["winning_square_silver%d" % count] = BoardSquare(SILVER, SURFACE_WIDTH / NUM_COLS,
                                                                                SURFACE_HEIGHT / NUM_ROWS)
        winning_squares_silver["winning_square_silver%d" % count].rect.x = coord[0]
        winning_squares_silver["winning_square_silver%d" % count].rect.y = coord[1]

    winning_squares_gold = {}
    for count, coord in enumerate(winning_board_square_gold_coords):
        winning_squares_gold["winning_square_gold%d" % count] = BoardSquare(GOLD, SURFACE_WIDTH / NUM_COLS,
                                                                            SURFACE_HEIGHT / NUM_ROWS)
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


class Board:
    def __init__(self):
        self.board = []

        # Two rows of pieces initialized for red and black
        self.red_remaining = NUM_COLS * 2
        self.black_remaining = NUM_COLS * 2

        self.red_lvl_2 = self.black_lvl_2 = 0
        self.red_lvl_3 = self.black_lvl_3 = 0
        self.red_lvl_4 = self.black_lvl_4 = 0
        self.red_lvl_5 = self.black_lvl_5 = 0
        self.draw_board()

    def evaluate_position(self):
        return self.red_remaining - self.black_remaining + 2 * (self.red_lvl_2 - self.black_lvl_2) + 3 * \
               (self.red_lvl_3 - self.black_lvl_3) + 4 * (self.red_lvl_4 - self.black_lvl_4) + 5 * \
               (self.red_lvl_5 - self.black_lvl_5)

    def get_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)








