import numpy as np
import pygame
import random
import math
import sys
from Connect4Chess import global_
from global_ import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_color, width, height):
        super(Sprite, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(sprite_color)

        self.color = sprite_color

        self.name = "Sprite " + str(global_.sprite_count)
        global_.sprite_count += 1

        self.rect = self.image.get_rect()

    def mouse_click_check(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            if self.color == RED:
                provide_legal_moves(self.rect.x, self.rect.y, RED)
                return True
            elif self.color == BLACK:
                provide_legal_moves(self.rect.x, self.rect.y, BLACK)
                return True

            return False

    def move(self, sprite_color, x_location, y_location):
        print("Received", x_location, y_location)
        strict_x_locations = [CIRCLE_RAD / 2, SURFACE_WIDTH / 8 + CIRCLE_RAD / 2,
                              2 * SURFACE_WIDTH / 8 + CIRCLE_RAD / 2, 3 * SURFACE_WIDTH / 8 + CIRCLE_RAD / 2,
                              4 * SURFACE_WIDTH / 8 + CIRCLE_RAD / 2, 5 * SURFACE_WIDTH / 8 + CIRCLE_RAD / 2,
                              6 * SURFACE_WIDTH / 8 + CIRCLE_RAD / 2, 7 * SURFACE_WIDTH / 8 + CIRCLE_RAD / 2]
        strict_y_locations = [CIRCLE_RAD / 2, SURFACE_HEIGHT / 8 + CIRCLE_RAD / 2,
                              2 * SURFACE_HEIGHT / 8 + CIRCLE_RAD / 2, 3 * SURFACE_HEIGHT / 8 + CIRCLE_RAD / 2,
                              4 * SURFACE_HEIGHT / 8 + CIRCLE_RAD / 2, 5 * SURFACE_HEIGHT / 8 + CIRCLE_RAD / 2,
                              6 * SURFACE_HEIGHT / 8 + CIRCLE_RAD / 2, 7 * SURFACE_HEIGHT / 8 + CIRCLE_RAD / 2]

        list_x = np.asarray(strict_x_locations)
        index_x = (np.abs(list_x - x_location)).argmin()

        list_y = np.asarray(strict_y_locations)
        index_y = (np.abs(list_y - y_location)).argmin()

        if sprite_color == RED:
            # Check for opponent's color? (Implementing Capture)
            if surface.get_at((int(x_location), int(y_location))) == BLACK:

                self.rect.x = list_x[index_x]
                self.rect.y = list_y[index_y]
            else:
                self.rect.x = list_x[index_x]
                self.rect.y = list_y[index_y]
        elif sprite_color == BLACK:
            # Check for opponent's color? (Implementing Capture)
            if surface.get_at((int(x_location), int(y_location))) == RED:
                self.rect.x = list_x[index_x]
                self.rect.y = list_y[index_y]
            else:
                self.rect.x = list_x[index_x]
                self.rect.y = list_y[index_y]





class Button(pygame.sprite.Sprite):
    def __init__(self, state, color, pos, size=(32, 16), image=None):
        super(Button, self).__init__()
        if image is None:
            self.rect = pygame.Rect(pos, size)
            self.image = pygame.Surface(size)
        else:
            self.image = pygame.Surface([28, 28])
            self.image.fill(color)
            self.rect = image.get_rect(topleft=pos)

        self.state = state
        self.pressed = False

    # def update(self):
    #     mouse_pos = pygame.mouse.get_pos()
    #     mouse_clicked = pygame.mouse.get_pressed()[0]
    #     if self.rect.collidepoint(*mouse_pos) and mouse_clicked:
    #         print("BUTTON PRESSED!")
    #         self.kill()  # Will remove itself from all pygame groups.
    #         surface.fill(WHITE)
    #         pygame.display.flip()


class BoardSquare(pygame.sprite.Sprite):
    def __init__(self, square_color, width, height):
        super(BoardSquare, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(square_color)

        self.color = square_color

        self.rect = self.image.get_rect()


image = pygame.Surface((100, 40))
image.fill((255, 0, 0))


# Legal moves are "jumping" over another piece in front of your piece. Pieces with no other pieces in
# front will have no legal moves.
def provide_legal_moves(x, y, color):

    print("Showing legal move: ", x, y, color)
    if color == BLACK:
        # The Black pieces start on the bottom and move upwards (negative y direction)

        # Bounds check (Check for out of bounds for top of the board)
        if y - 2 * CIRCLE_RAD > 0:
            if surface.get_at((int(x), int(y - 2 * CIRCLE_RAD))) == BLACK:
                # Jump over own piece
                buttons.add(Button("Vertical", GREEN, pos=(x, y - 4 * CIRCLE_RAD), image=image))
                print("Black checker in front!")
            elif surface.get_at((int(x), int(y - 2 * CIRCLE_RAD))) == RED and \
                    surface.get_at((int(x), int(y - 4 * CIRCLE_RAD))) != RED and \
                    surface.get_at((int(x), int(y - 4 * CIRCLE_RAD))) != BLACK:
                # Capture opponent piece only possible if there is an "empty" landing square

                buttons.add(Button("Vertical", GREEN, pos=(x, y - 4 * CIRCLE_RAD), image=image))
                print("Red checker in front!")

            if x - 2 * CIRCLE_RAD > 0 and \
                    surface.get_at((int(x - 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == BLACK:
                # Jump over own piece
                buttons.add(Button("Left Diagonal", GREEN, pos=(x - 4 * CIRCLE_RAD, y - 4 * CIRCLE_RAD), image=image))
                print("Black checker in left diagonal!")
            elif x - 2 * CIRCLE_RAD > 0 and \
                    surface.get_at((int(x - 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == RED and \
                    surface.get_at((int(x - 4), int(y - 4 * CIRCLE_RAD))) != RED and \
                    surface.get_at((int(x - 4), int(y - 4 * CIRCLE_RAD))) != BLACK:
                # Capture opponent piece only possible if there is an "empty" landing square

                buttons.add(Button("Left Diagonal", GREEN, pos=(x - 4 * CIRCLE_RAD, y - 4 * CIRCLE_RAD), image=image))
                print("Red checker in left diagonal!")

            if x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                    surface.get_at((int(x + 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == BLACK:
                # Jump over own piece
                buttons.add(Button("Right Diagonal", GREEN, pos=(x + 4 * CIRCLE_RAD, y - 4 * CIRCLE_RAD), image=image))
                print("Black checker in right diagonal!")
            elif x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                    surface.get_at((int(x + 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == RED and \
                    surface.get_at((int(x + 4), int(y - 4 * CIRCLE_RAD))) != RED and \
                    surface.get_at((int(x + 4), int(y - 4 * CIRCLE_RAD))) != BLACK:
                # Capture opponent piece only possible if there is an "empty" landing square

                buttons.add(Button("Right Diagonal", GREEN, pos=(x + 4 * CIRCLE_RAD, y - 4 * CIRCLE_RAD), image=image))
                print("Red checker in right diagonal!")

    elif color == RED:
        # The Red pieces start on the top and move downwards (positive y direction)

        # Bounds check (Check for out of bounds for bottom of the board)
        if y + 2 * CIRCLE_RAD < SURFACE_HEIGHT:
            if surface.get_at((int(x), int(y + 2 * CIRCLE_RAD))) == RED:
                # Jump over own piece
                buttons.add(Button("Vertical", BLUE, pos=(x, y + 4 * CIRCLE_RAD), image=image))
                print("Red checker in front!")
            elif surface.get_at((int(x), int(y + 2 * CIRCLE_RAD))) == BLACK and \
                    surface.get_at((int(x), int(y + 4 * CIRCLE_RAD))) != RED and \
                    surface.get_at((int(x), int(y + 4 * CIRCLE_RAD))) != BLACK:
                # Capture opponent piece only possible if there is an "empty" landing square:

                buttons.add(Button("Vertical", BLUE, pos=(x, y + 4 * CIRCLE_RAD), image=image))
                print("Black checker in front!")

            if x - 2 * CIRCLE_RAD > 0 and \
                    surface.get_at((int(x - 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == RED:
                # Jump over own piece
                buttons.add(Button("Left Diagonal", BLUE, pos=(x - 4 * CIRCLE_RAD, y + 4 * CIRCLE_RAD), image=image))
                print("Red checker in left diagonal!")
            elif x - 2 * CIRCLE_RAD > 0 and \
                    surface.get_at((int(x - 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == BLACK and \
                    surface.get_at((int(x - 4), int(y + 4 * CIRCLE_RAD))) != RED and \
                    surface.get_at((int(x - 4), int(y + 4 * CIRCLE_RAD))) != BLACK:
                # Capture opponent piece only possible if there is an "empty" landing square

                buttons.add(Button("Left Diagonal", BLUE, pos=(x - 4 * CIRCLE_RAD, y + 4 * CIRCLE_RAD), image=image))
                print("Black checker in left diagonal!")

            if x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                    surface.get_at((int(x + 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == RED:
                # Jump over own piece
                buttons.add(Button("Right Diagonal", BLUE, pos=(x + 4 * CIRCLE_RAD, y + 4 * CIRCLE_RAD), image=image))
                print("Red checker in right diagonal!")
            elif x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                    surface.get_at((int(x + 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == BLACK and \
                    surface.get_at((int(x + 4), int(y + 4 * CIRCLE_RAD))) != RED and \
                    surface.get_at((int(x + 4), int(y + 4 * CIRCLE_RAD))) != BLACK:
                # Capture opponent piece only possible if there is an "empty" landing square
                buttons.add(Button("Right Diagonal", BLUE, pos=(x + 4 * CIRCLE_RAD, y + 4 * CIRCLE_RAD), image=image))
                print("Black checker in right diagonal!")

