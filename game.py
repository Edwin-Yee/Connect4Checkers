import pygame
from global_ import RED, BLACK, CIRCLE_RAD
from board import Board
# code adapted from https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/game.py
class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

