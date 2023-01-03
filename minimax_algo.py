import pygame
from copy import deepcopy
from global_ import RED, BLACK
# code adapted from https://github.com/techwithtim/Python-Checkers-AI/blob/master/minimax/algorithm.py


def minimax(position, depth, maximize_player, game):
    # position as a board object, given a board provide the best possible board after a single move
    # depth is how far the tree extends, recursive call, depth - 1
    # maximize_player is boolean val telling if we want to maximize the value or minimizing the value
    # game is the game object from the main.py

    if depth == 0 or position.winner() is not None:
        # if we have reached the last node of the tree or if we have a winner in the given position \
        return position.evaluate(), position

    if maximize_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves

def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)