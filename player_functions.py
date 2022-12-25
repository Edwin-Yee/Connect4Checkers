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
