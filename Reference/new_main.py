import pygame
from global_ import CIRCLE_RAD, SURFACE_WIDTH, SURFACE_HEIGHT, RED
from Connect4Chess.Reference.game import Game

# Code adapted from https://github.com/techwithtim/Python-Checkers-AI/blob/master/main.py

FPS = 60

window = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
pygame.display.set_caption("Connect4Checkers Game")


def get_row_col_from_mouse(position):
    x, y = position
    row = y // (CIRCLE_RAD * 4)
    col = y // (CIRCLE_RAD * 4)
    return row, col


def main():
    game_over = False
    clock = pygame.time.Clock()
    game = Game(window)

    while not game_over:
        clock.tick(FPS)

        if game.turn == RED:
            print("AI RED turn")
            # value, new_board = minimax(game.get_board(), 4, RED, game)
            # game.ai_move(new_board)

        if game.winner() is not None:
            # There is a winner
            print(game.winner())
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(position)
                game.select(row, col)

        game.update()

    pygame.quit()


main()



