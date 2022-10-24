import numpy as np
import pygame
import random
import math
import sys

from Connect4Chess import global_
from global_ import *
from classes import Sprite
from classes import BoardSquare
from functions import draw_board

# Initializing Pygame
pygame.init()

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
                        # surface.fill(WHITE)
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

