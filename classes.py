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

    def move(self, x_location, y_location):
        strict_x_locations = [0, SURFACE_WIDTH / 8, 2 * SURFACE_WIDTH / 8, 3 * SURFACE_WIDTH / 8, 4 * SURFACE_WIDTH / 8,
                              5 * SURFACE_WIDTH / 8, 6 * SURFACE_WIDTH / 8, 7 * SURFACE_WIDTH / 8]
        strict_y_locations = [0, SURFACE_HEIGHT / 8, 2 * SURFACE_HEIGHT / 8, 3 * SURFACE_HEIGHT / 8,
                              4 * SURFACE_HEIGHT / 8, 5 * SURFACE_HEIGHT / 8, 6 * SURFACE_HEIGHT / 8,
                              7 * SURFACE_HEIGHT / 8]

        list_x = np.asarray(strict_x_locations)
        index_x = (np.abs(list_x - x_location)).argmin()

        list_y = np.asarray(strict_y_locations)
        index_y = (np.abs(list_y - y_location)).argmin()

        self.rect.x = list_x[index_x] + CIRCLE_RAD / 2
        self.rect.y = list_y[index_y] + CIRCLE_RAD / 2



class Button(pygame.sprite.Sprite):
    def __init__(self, color, pos, size=(32, 16), image=None):
        super(Button, self).__init__()
        if image is None:
            self.rect = pygame.Rect(pos, size)
            self.image = pygame.Surface(size)
        else:
            self.image = pygame.Surface([28, 28])
            self.image.fill(color)
            self.rect = image.get_rect(topleft=pos)

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
        print(surface.get_at((int(x), int(y - 2 * CIRCLE_RAD))))
        if y - 2 * CIRCLE_RAD > 0 and surface.get_at((int(x), int(y - 2 * CIRCLE_RAD))) == BLACK:
            buttons.add(Button(GREEN, pos=(x, y - 4 * CIRCLE_RAD), image=image))
            print("Checker in front!")
        if y - 2 * CIRCLE_RAD > 0 and x - 2 * CIRCLE_RAD > 0 and \
                surface.get_at((int(x - 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == BLACK:
            buttons.add(Button(GREEN, pos=(x - 4 * CIRCLE_RAD, y - 4 * CIRCLE_RAD), image=image))
            print("Checker in left diagonal!")
        if y - 2 * CIRCLE_RAD > 0 and x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                surface.get_at((int(x + 2 * CIRCLE_RAD), int(y - 2 * CIRCLE_RAD))) == BLACK:
            buttons.add(Button(GREEN, pos=(x + 4 * CIRCLE_RAD, y - 4 * CIRCLE_RAD), image=image))
            print("Checker in right diagonal!")

    elif color == RED:
        if y + 2 * CIRCLE_RAD < SURFACE_HEIGHT and surface.get_at((int(x), int(y + 2 * CIRCLE_RAD))) == RED:
            buttons.add(Button(BLUE, pos=(x, y + 4 * CIRCLE_RAD), image=image))
        if y + 2 * CIRCLE_RAD < SURFACE_HEIGHT and x - 2 * CIRCLE_RAD > 0 and \
                surface.get_at((int(x - 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == RED:
            buttons.add(Button(BLUE, pos=(x - 4 * CIRCLE_RAD, y + 4 * CIRCLE_RAD), image=image))
        if y + 2 * CIRCLE_RAD < SURFACE_HEIGHT and x + 2 * CIRCLE_RAD < SURFACE_WIDTH and \
                surface.get_at((int(x + 2 * CIRCLE_RAD), int(y + 2 * CIRCLE_RAD))) == RED:
            buttons.add(Button(BLUE, pos=(x + 4 * CIRCLE_RAD, y + 4 * CIRCLE_RAD), image=image))
