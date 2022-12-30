import pygame

def get_current_player(player_state_inner) -> str:
    if player_state_inner % 2 == 0:
        return 'Black'
    else:
        return 'Red'


def increment_score(player_state_inner, inner_player_black_score, inner_player_red_score) -> tuple:
    if player_state_inner % 2 == 0:
        # Player black's turn
        inner_player_black_score += 1

    else:
        # Player red's turn
        inner_player_red_score += 1

    return inner_player_black_score, inner_player_red_score


def give_silver_gold_reward(silver_top_occupied_inner, silver_bottom_occupied_inner, gold_top_occupied_inner, \
                            gold_bottom_occupied_inner, player_red_score, player_black_score):
    if silver_top_occupied_inner == 'Red':
        player_red_score += 1
    if silver_bottom_occupied_inner == 'Red':
        player_red_score += 1
    if gold_top_occupied_inner == 'Red':
        player_red_score += 2
    if gold_bottom_occupied_inner == 'Red':
        player_red_score += 2

    if silver_top_occupied_inner == 'Black':
        player_black_score += 1
    if silver_bottom_occupied_inner == 'Black':
        player_black_score += 1
    if gold_top_occupied_inner == 'Black':
        player_black_score += 2
    if gold_bottom_occupied_inner == 'Black':
        player_black_score += 2

    return player_black_score, player_red_score


def show_score_and_turn(inner_player_red_score, inner_player_black_score, surface, player_state, smaller_font, textX, textY, red_textY, black_textY, extra_space_for_score):
    font = pygame.font.Font("freesansbold.ttf", 24)
    score_red = font.render("Player Red Gold: " + str(inner_player_red_score), True, (255, 255, 255))
    score_black = font.render("Player Black Gold: " + str(inner_player_black_score), True, (255, 255, 255))

    # Draw a gray rectangle to cover up the previous score (not black because we are detecting for the black color
    # when showing the legal moves)
    pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(surface.get_width() - extra_space_for_score, 0, 500, 500))
    print("player_functions.py:", get_current_player(player_state))

    if get_current_player(player_state) == 'Red':
        current_turn = smaller_font.render("Player with Red Pieces Turn", True, (255, 255, 255))
        surface.blit(current_turn, (textX, textY))
    else:
        current_turn = smaller_font.render("Player with Black Pieces Turn", True, (255, 255, 255))
        surface.blit(current_turn, (textX, textY))

    surface.blit(score_red, (textX, red_textY))
    surface.blit(score_black, (textX, black_textY))