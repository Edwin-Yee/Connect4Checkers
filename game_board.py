import pygame
from global_ import NUM_ROWS, NUM_COLS, RED, BLACK, SURFACE_WIDTH, SURFACE_HEIGHT, CIRCLE_RAD, PALE_COLOR, DARK_BROWN

# background_color = (0, 0, 0)
# screen = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
# pygame.display.set_caption("AI Move Screen")
# screen.fill(background_color)
# pygame.display.flip()
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False


class Board:

    def __init__(self, all_sprites_list, ai_possible_moves):
        self.red_remaining = self.black_remaining = 0
        self.red_lvl_2 = self.black_lvl_2 = 0
        self.red_lvl_3 = self.black_lvl_3 = 0
        self.red_lvl_4 = self.black_lvl_4 = 0
        self.red_lvl_5 = self.black_lvl_5 = 0

        for sprite in all_sprites_list:
            if sprite.get_color() == RED:
                if sprite.get_level() == 2:
                    self.red_lvl_2 += 1
                elif sprite.get_level() == 3:
                    self.red_lvl_3 += 1
                elif sprite.get_level() == 4:
                    self.red_lvl_4 += 1
                elif sprite.get_level() == 4:
                    self.red_lvl_4 += 1

                self.red_remaining += 1
            else:
                if sprite.get_level() == 2:
                    self.black_lvl_2 += 1
                elif sprite.get_level() == 3:
                    self.black_lvl_3 += 1
                elif sprite.get_level() == 4:
                    self.black_lvl_4 += 1
                elif sprite.get_level() == 4:
                    self.black_lvl_4 += 1

                self.black_remaining += 1

        print("Red remaining:", self.red_remaining)
        print("Black remaining:", self.black_remaining)

        # Try move and evaluate position?
        print("Evaluation - AI: ", self.evaluate_position())

    def evaluate_position(self):
        # Evaluate the current position's "score".
        # Higher score means better position. Lower score means worse position.
        return self.red_remaining - self.black_remaining + 2 * (self.red_lvl_2 - self.black_lvl_2) + 3 * \
               (self.red_lvl_3 - self.black_lvl_3) + 4 * (self.red_lvl_4 - self.black_lvl_4) + 5 * \
               (self.red_lvl_5 - self.black_lvl_5)

    def draw_squares(self, window):
        window.fill(DARK_BROWN)
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                pygame.draw.rect(window, PALE_COLOR,
                                 (row * CIRCLE_RAD * 4, col * CIRCLE_RAD * 4, CIRCLE_RAD * 4, CIRCLE_RAD * 4))