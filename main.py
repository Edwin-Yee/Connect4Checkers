import numpy as np
import pygame
import random
import math
import sys
import neat
import os


from global_ import *
from classes import Sprite
from classes import BoardSquare
from classes import ShopButton
from functions import draw_board
from functions import show_score_and_turn
from player_functions import *

# Initializing Pygame
pygame.init()

# Initializing the board
draw_board()
squares_list.update()
squares_list.draw(surface)

upgrade_button_red = ShopButton(textX + 50, red_textY + 20, upgrade_img, 1)
upgrade_button_black = ShopButton(textX + 50, black_textY + 20, upgrade_img, 1)
cancel_button = ShopButton(textX, black_textY + 100, cancel_img, 1)
confirm_button = ShopButton(textX + 100, black_textY + 100, confirm_img, 1)

show_score_and_turn(player_red_score, player_black_score, surface, player_state, smaller_font, textX, textY, red_textY, black_textY, extra_space_for_score)

pygame.display.flip()

num_click = 0
isButtonPressed = False
isSpriteClicked = False


# class ConnectGame:
#     def __init__(self, window, width, height):
#         self.game = Game(window, width, height)
# TODO put game into separate class with initialization


def remove_buttons():
    for inner_button in buttons:
        inner_button.kill()
        pygame.display.flip()


def remove_captured_sprite(button):
    button_x = button.get_position()[0]
    button_y = button.get_position()[1]
    sprite_x = 0
    sprite_y = 0

    if get_current_player(player_state) == 'Red':  # Red on the top
        if button.get_state() == "Vertical Capture":
            sprite_x = button_x
            sprite_y = button_y - 2 * CIRCLE_RAD
        elif button.get_state() == "Left Diagonal Capture":
            sprite_x = button_x + 2 * CIRCLE_RAD
            sprite_y = button_y - 2 * CIRCLE_RAD
        elif button.get_state() == "Right Diagonal Capture":
            sprite_x = button_x - 2 * CIRCLE_RAD
            sprite_y = button_y - 2 * CIRCLE_RAD
    elif get_current_player(player_state) == 'Black':  # Black on the bottom
        if button.get_state() == "Vertical Capture":
            sprite_x = button_x
            sprite_y = button_y + 2 * CIRCLE_RAD
        elif button.get_state() == "Left Diagonal Capture":
            sprite_x = button_x + 2 * CIRCLE_RAD
            sprite_y = button_y + 2 * CIRCLE_RAD
        elif button.get_state() == "Right Diagonal Capture":
            sprite_x = button_x - 2 * CIRCLE_RAD
            sprite_y = button_y + 2 * CIRCLE_RAD

    for inner_sprite in all_sprites_list:
        # print(loop_sprite.rect.x, loop_sprite.rect.y, "vs", sprite_x, sprite_y)
        if inner_sprite.rect.x == sprite_x and inner_sprite.rect.y == sprite_y:
            print("Removed sprite located at:", sprite_x, sprite_y)
            all_sprites_list.remove(inner_sprite)


def check_silver_gold_squares():
    # Note: register after landing (have to stay there for until opponent's turn finishes)
    global silver_top_occupied
    global silver_bottom_occupied
    global gold_top_occupied
    global gold_bottom_occupied
    global game_over
    global red_wins
    global black_wins

    # Check Silver and Gold squares
    if surface.get_at((int(winning_board_square_silver_coords[0][0] + CIRCLE_RAD/2), int(winning_board_square_silver_coords[0][1] + CIRCLE_RAD/2)))[:3] == RED:
        silver_top_occupied = 'Red'
        print("LANDED ON TOP LEFT SILVER RED")
    elif surface.get_at((int(winning_board_square_silver_coords[0][0] + CIRCLE_RAD/2), int(winning_board_square_silver_coords[0][1] + CIRCLE_RAD/2)))[:3] == BLACK:
        silver_top_occupied = 'Black'
        print("LANDED ON TOP LEFT SILVER BLACK")
    else:
        silver_top_occupied = None

    if surface.get_at((int(winning_board_square_silver_coords[1][0] + CIRCLE_RAD/2), int(winning_board_square_silver_coords[1][1] + CIRCLE_RAD/2)))[:3] == RED:
        silver_bottom_occupied = 'Red'
        print("LANDED ON BOTTOM RIGHT SILVER RED")
    elif surface.get_at((int(winning_board_square_silver_coords[1][0] + CIRCLE_RAD/2), int(winning_board_square_silver_coords[1][1] + CIRCLE_RAD/2)))[:3] == BLACK:
        silver_bottom_occupied = 'Black'
        print("LANDED ON BOTTOM RIGHT SILVER BLACK")
    else:
        silver_bottom_occupied = None

    if surface.get_at((int(winning_board_square_gold_coords[0][0] + CIRCLE_RAD / 2),
                       int(winning_board_square_gold_coords[0][1] + CIRCLE_RAD / 2)))[:3] == RED:
        gold_top_occupied = 'Red'
    elif surface.get_at((int(winning_board_square_gold_coords[0][0] + CIRCLE_RAD / 2),
                       int(winning_board_square_gold_coords[0][1] + CIRCLE_RAD / 2)))[:3] == BLACK:
        gold_top_occupied = 'Black'
    else:
        gold_top_occupied = None

    if surface.get_at((int(winning_board_square_gold_coords[1][0] + CIRCLE_RAD / 2),
                       int(winning_board_square_gold_coords[1][1] + CIRCLE_RAD / 2)))[:3] == RED:
        gold_bottom_occupied = 'Red'
    elif surface.get_at((int(winning_board_square_gold_coords[1][0] + CIRCLE_RAD / 2),
                       int(winning_board_square_gold_coords[1][1] + CIRCLE_RAD / 2)))[:3] == BLACK:
        gold_bottom_occupied = 'Black'
    else:
        gold_bottom_occupied = None

    # Check winning connect (All 4 middle winning squares are occupied)
    if silver_top_occupied == 'Red' and silver_bottom_occupied == 'Red' and gold_top_occupied == 'Red' and \
            gold_bottom_occupied == 'Red':
        game_over = True
        red_wins = True

    elif silver_top_occupied == 'Black' and silver_bottom_occupied == 'Black' and gold_top_occupied == 'Black' and \
            gold_bottom_occupied == 'Black':
        game_over = True
        black_wins = True


while not game_over:

    if upgrade_button_red.draw():
        print("Red Upgrade: True")
        red_upgrade_state = True

    if upgrade_button_black.draw():
        print("Black Upgrade: True")
        black_upgrade_state = True

    if cancel_button.draw():
        print("Cancelled")
        red_upgrade_state = False
        black_upgrade_state = False
        is_confirmed = False

    if confirm_button.draw():
        if len(confirmation_sprite.sprites()) > 0:
            if confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].get_color() == RED:
                if player_red_score >= 3:
                    print("Confirmed - RED upgrade")
                    player_red_score -= 3
                    confirmation_sprite.sprites()[0].upgrade()
                    red_upgrade_state = False
                    confirmation_sprite.empty()
                else:
                    print("RED - You do not have enough gold to purchase an upgrade!")
            elif confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].get_color() == BLACK:
                if player_black_score >= 3:
                    print("Confirmed - BLACK upgrade")
                    player_black_score -= 3
                    confirmation_sprite.sprites()[0].upgrade()
                    black_upgrade_state = False
                    confirmation_sprite.empty()
                else:
                    print("BLACK - You do not have enough gold to purchase an upgrade!")

            show_score_and_turn(player_red_score, player_black_score, surface, player_state, smaller_font, textX, textY,
                                red_textY, black_textY, extra_space_for_score)

        else:
            print("There are no sprites selected for an upgrade")

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        elif game_over:
            print("GAME OVER!")
            if black_wins:
                print("BLACK WINS!")
            elif red_wins:
                print("RED WINS!")
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_position, y_position = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]

            if red_upgrade_state and get_current_player(player_state) == 'Red':
                for sprite in all_sprites_list:
                    if sprite.mouse_click_check(x_position, y_position):
                        confirmation_sprite.add(sprite)
                        print("Sprite selected for upgrade - RED")

            elif black_upgrade_state and get_current_player(player_state) == 'Black':
                for sprite in all_sprites_list:
                    if sprite.mouse_click_check(x_position, y_position):
                        confirmation_sprite.add(sprite)
                        print("Sprite selected for upgrade - BLACK")

            else:
                check_silver_gold_squares()

                print("It is", get_current_player(player_state), "'s turn")

                # x_position, y_position = pygame.mouse.get_pos()
                # mouse_clicked = pygame.mouse.get_pressed()[0]
                # print(surface.get_at(pygame.mouse.get_pos()))
                if get_current_player(player_state) == 'Black' and surface.get_at(pygame.mouse.get_pos()) != RED \
                    or get_current_player(player_state) == 'Red' and surface.get_at(pygame.mouse.get_pos()) != BLACK:
                    for sprite in all_sprites_list:
                        if sprite.mouse_click_check(x_position, y_position):
                            if num_click % 2 == 0:
                                current_click_sprite_list.add(sprite)
                                print("Added sprite", sprite.name, "to current_click_sprite_list")
                                isSpriteClicked = True
                            else:
                                # re-clicked on sprite, ignore action (remove sprites stored in the list)
                                # no update to player state, still the same player's turn
                                print("Re-clicked on sprite")
                                current_click_sprite_list.empty()
                                remove_buttons()

                    print("--------")
                    if len(buttons) == 3:
                        button_1 = buttons.sprites()[0]  # Middle Button
                        button_2 = buttons.sprites()[1]  # Left Button
                        button_3 = buttons.sprites()[2]  # Right Button

                        if button_1.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 1 PRESSED!")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].color
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_1.get_state())

                            if button_1.get_state() == "Vertical Capture":
                                print("WORKING CAPTURE VERTICAL")
                                player_black_score, player_red_score = player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                remove_captured_sprite(button_1)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif button_2.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 2 PRESSED!")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].color
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_2.get_state())

                            if button_2.get_state() == "Left Diagonal Capture":
                                print("WORKING CAPTURE LEFT DIAGONAL")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                remove_captured_sprite(button_2)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif button_3.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 3 PRESSED!")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].color
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_3.get_state())

                            if button_3.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE RIGHT DIAGONAL")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                remove_captured_sprite(button_3)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif not button_1.rect.collidepoint(x_position, y_position) \
                                and not button_2.rect.collidepoint(x_position, y_position) \
                                and not button_3.rect.collidepoint(x_position, y_position) \
                                and not isSpriteClicked and mouse_clicked and num_click % 2 == 1:
                            # no update to player state, still the same player's turn
                            print("No Button has been pressed")
                            current_click_sprite_list.empty()
                            remove_buttons()

                    elif len(buttons) == 2:

                        button_1 = buttons.sprites()[0]  # Some Button
                        button_2 = buttons.sprites()[1]  # Some Button

                        if button_1.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 1 PRESSED! (EDGE CASE)")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].color
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_1.get_state())

                            if button_1.get_state() == "Vertical Capture" or button_1.get_state() == "Left Diagonal Capture" \
                                    or button_1.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE 2 BUTTON")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                remove_captured_sprite(button_1)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif button_2.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 2 PRESSED! (EDGE CASE)")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].color
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_2.get_state())

                            if button_2.get_state() == "Vertical Capture" or button_2.get_state() == "Left Diagonal Capture" \
                                    or button_2.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE 2 BUTTON")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                remove_captured_sprite(button_2)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif not button_1.rect.collidepoint(x_position, y_position) \
                                and not button_2.rect.collidepoint(x_position, y_position) \
                                and not isSpriteClicked and mouse_clicked and num_click % 2 == 1:
                            # no update to player state, still the same player's turn
                            print("No Button has been pressed")
                            current_click_sprite_list.empty()
                            remove_buttons()

                    elif len(buttons) == 1:

                        button_1 = buttons.sprites()[0]  # Some Button

                        if button_1.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 1 PRESSED! (ONLY 1 EDGE CASE)")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].color
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_1.get_state())

                            if button_1.get_state() == "Vertical Capture" or button_1.get_state() == "Left Diagonal Capture" \
                                    or button_1.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE - 1 BUTTON SHOWN")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                remove_captured_sprite(button_1)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif not button_1.rect.collidepoint(x_position, y_position) \
                                and not isSpriteClicked and mouse_clicked and num_click % 2 == 1:
                            # no update to player state, still the same player's turn
                            print("No Button has been pressed")
                            current_click_sprite_list.empty()
                            remove_buttons()

                    isSpriteClicked = False
                    num_click = num_click + 1

                    # Update the score and the turn
                    show_score_and_turn(player_red_score, player_black_score, surface, player_state, smaller_font, textX, textY, red_textY, black_textY, extra_space_for_score)
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




# def eval_genomes(genomes, config):
#     # Genomes is a list of tuples
#     # Every AI playing against every other AI (cut by i+1)
#     width, height = SURFACE_WIDTH, SURFACE_HEIGHT
#     window = pygame.display.set_mode((width, height))
#
#     for i, (genome_id1, genome1) in enumerate(genomes):
#
#         # Check out of bounds
#         if i + 1 == len(genomes):
#             break
#
#         genome1.fitness = 0     # initialize fitness level
#         for genome_id2, genome2 in genomes[i+1:]:
#             if genome2.fitness is None:
#                 genome2.fitness = 0     # initialize fitness if not set before
#
#             game = thegame()
#             game.train_ai(genome1, genome2, config) # TODO
# def run_neural_network(config):
#     # example usage
#     # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-2')
#     population = neat.Population(config)
#
#     # See generations, data
#     population.add_reporter(neat.StdOutReporter(True))
#     statistics = neat.StatisticsReporter()
#     population.add_reporter(statistics)
#
#     # Save a checkpoint after x generations, currently set to 1
#     population.add_reporter(neat.Checkpointer(1))
#
#     # Max gen: set to 50
#     best_winner = population.run(eval_genomes, 50)
#
#
# if __name__ == "__main__":
#     local_directory = os.path.dirname(__file__)
#     config_path = os.path.join(local_directory, "config.txt")
#
#     # load config file
#     config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_path)
#
#     run_neural_network(config)

