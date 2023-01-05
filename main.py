from classes import ShopButton
from classes import get_ai_moves
from functions import *
from player_functions import *
from game_board import Board

# Initializing Pygame
pygame.init()

# Initializing the board
draw_board()
squares_list.update()
squares_list.draw(surface)

upgrade_button_red = ShopButton(textX, red_textY + score_red_text_height, upgrade_img, global_scalar)
upgrade_button_black = ShopButton(textX, black_textY + score_black_text_height, upgrade_img, global_scalar)
cancel_button = ShopButton(textX, textY + current_turn_text_red_height, cancel_img, global_scalar)
confirm_button = ShopButton(textX + confirm_img.get_width() * global_scalar, textY + current_turn_text_black_height, confirm_img, global_scalar)

show_score_and_turn(player_red_score, player_black_score, surface, player_state, smaller_font, textX, textY, red_textY, black_textY, extra_space_for_score)

pygame.display.flip()

num_click = 0
isButtonPressed = False
isSpriteClicked = False
FPS = 60
clock = pygame.time.Clock()

# class ConnectGame:
#     def __init__(self, window, width, height):
#         self.game = Game(window, width, height)
# TODO put game into separate class with initialization

while not game_over:
    clock.tick(FPS)

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
                if player_red_score >= 3 and confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].get_level() < 5:
                    print("Confirmed - RED upgrade")
                    player_red_score -= 3
                    confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].upgrade()
                    red_upgrade_state = False
                    confirmation_sprite.empty()
                elif player_red_score < 3 and confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].get_level() < 5:
                    print("RED - You do not have enough gold to purchase an upgrade!")
                else:
                    print("RED - Sprite is already at max level!")

            elif confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].get_color() == BLACK:
                if player_black_score >= 3 and confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].get_level() < 5:
                    print("Confirmed - BLACK upgrade")
                    player_black_score -= 3
                    confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].upgrade()
                    black_upgrade_state = False
                    confirmation_sprite.empty()
                elif player_black_score < 3 and confirmation_sprite.sprites()[len(confirmation_sprite.sprites()) - 1].get_level() < 5:
                    print("BLACK - You do not have enough gold to purchase an upgrade!")
                else:
                    print("BLACK - Sprite is already at max level!")

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if get_current_player(player_state) == 'Red':
                    # value, new_board = minimax(game.get_board(), 1, RED, game)
                    # game.ai_move(new_board)
                    print("It is the computer's turn to move")
                    all_possible_ai_moves = []

                    for sprite in all_sprites_list:
                        # Check if the sprite is red and that the move list is not empty
                        if sprite.get_color() == RED and get_ai_moves(sprite.rect.x, sprite.rect.y, sprite.get_level()):
                            # print("Possible move:", get_ai_moves(sprite.rect.x, sprite.rect.y, sprite.get_level()))
                            all_possible_ai_moves.append(get_ai_moves(sprite.rect.x, sprite.rect.y, sprite.get_level()))

                    board = Board(all_sprites_list, all_possible_ai_moves)

                    # TO-DO create a board object giving the locations of all the sprites
                    # print(minimax(all_possible_ai_moves, board))

                else:
                    print("It is the player's turn to move")

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
                silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, game_over, \
                red_wins, black_wins = check_silver_gold_squares(silver_top_occupied, silver_bottom_occupied,
                                                                 gold_top_occupied, gold_bottom_occupied, game_over,
                                                                 red_wins, black_wins)

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
                            curr_sprite_color = current_click_sprite_list.sprites()[0].get_color()
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_1.get_state())

                            if button_1.get_state() == "Vertical Capture":
                                print("WORKING CAPTURE VERTICAL")
                                player_black_score, player_red_score = player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                all_sprites_list = remove_captured_sprite(button_1, all_sprites_list, player_state)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif button_2.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 2 PRESSED!")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].get_color()
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_2.get_state())

                            if button_2.get_state() == "Left Diagonal Capture":
                                print("WORKING CAPTURE LEFT DIAGONAL")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                all_sprites_list = remove_captured_sprite(button_2, all_sprites_list, player_state)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif button_3.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 3 PRESSED!")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].get_color()
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_3.get_state())

                            if button_3.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE RIGHT DIAGONAL")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                all_sprites_list = remove_captured_sprite(button_3, all_sprites_list, player_state)

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
                            curr_sprite_color = current_click_sprite_list.sprites()[0].get_color()
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_1.get_state())

                            if button_1.get_state() == "Vertical Capture" or button_1.get_state() == "Left Diagonal Capture" \
                                    or button_1.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE 2 BUTTON")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                all_sprites_list = remove_captured_sprite(button_1, all_sprites_list, player_state)

                            player_black_score, player_red_score = give_silver_gold_reward(silver_top_occupied, silver_bottom_occupied, gold_top_occupied, gold_bottom_occupied, player_red_score, player_black_score)
                            player_state += 1

                        elif button_2.rect.collidepoint(x_position, y_position) and mouse_clicked:
                            print("BUTTON 2 PRESSED! (EDGE CASE)")
                            curr_sprite_color = current_click_sprite_list.sprites()[0].get_color()
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_2.get_state())

                            if button_2.get_state() == "Vertical Capture" or button_2.get_state() == "Left Diagonal Capture" \
                                    or button_2.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE 2 BUTTON")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                all_sprites_list = remove_captured_sprite(button_2, all_sprites_list, player_state)

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
                            curr_sprite_color = current_click_sprite_list.sprites()[0].get_color()
                            current_click_sprite_list.sprites()[0].move(curr_sprite_color, x_position, y_position)
                            current_click_sprite_list.empty()
                            remove_buttons()

                            print(button_1.get_state())

                            if button_1.get_state() == "Vertical Capture" or button_1.get_state() == "Left Diagonal Capture" \
                                    or button_1.get_state() == "Right Diagonal Capture":
                                print("WORKING CAPTURE - 1 BUTTON SHOWN")
                                player_black_score, player_red_score = increment_score(player_state, player_black_score, player_red_score)
                                all_sprites_list = remove_captured_sprite(button_1, all_sprites_list, player_state)

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


# clock.tick(FPS)
#
# if game.turn == WHITE:
#     value, new_board = minimax(game.get_board(), 4, WHITE, game)
#     game.ai_move(new_board)
#
# if game.winner() != None:
#     print(game.winner())
#     run = False
#
# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         run = False
#
#     if event.type == pygame.MOUSEBUTTONDOWN:
#         pos = pygame.mouse.get_pos()
#         row, col = get_row_col_from_mouse(pos)
#         game.select(row, col)
#
# game.update()




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

