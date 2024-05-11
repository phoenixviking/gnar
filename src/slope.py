import pygame
from noise import Noise


# class implementing all the game logic
class Slope:
    # Render block_size x block_size pixel blocks
    # WARNING! Size 15 x 15 and below cause a really slow render.
    block_size = 20

    def __init__(self, screen, player):
        self.game_over = False
        self.screen_w = screen.get_width()
        self.screen_h = screen.get_height()
        self.screen = screen
        self.player = player
        self.screen_UL_pos = pygame.Vector2(self.player.get_pos_x() - self.screen.get_width() / 2,
                                            self.player.get_pos_y() + self.player.dist_from_top)

    def get_screen_UL_pos(self):
        return self.screen_UL_pos

    def get_screen_UL_pos_x(self):
        return self.screen_UL_pos.x

    def get_screen_UL_pos_y(self):
        return self.screen_UL_pos.y

    def get_game_over(self):
        return self.game_over

    # create cliffs, and set height to very low
    @staticmethod
    def get_slope_height(pos):
        raw_height = Noise.slope_noise(pos, 6000)

        return raw_height

    @staticmethod
    def block_has_tree(pos):
        rem_x = pos.x % Slope.block_size
        rem_y = pos.y % Slope.block_size
        block_UL = pygame.Vector2(pos.x - rem_x, pos.y + (Slope.block_size - rem_y))
        noise = Noise.trees_noise(block_UL, 800, 5000)
        has_tree = noise > 0.45
        return has_tree

    # make sure the screen is always framing the player at the same screen coord.
    def update_screen_UL_pos(self):
        self.screen_UL_pos.x = self.player.get_pos_x() - (self.screen_w / 2)
        self.screen_UL_pos.y = self.player.get_pos_y() + self.player.dist_from_top

    # check if player in the same bounding boxes as any of the obstacles currently on screen
    def player_collided(self):
        # check if the box that the two ski tips are in have trees
        # change this once angle stuff is implemented
        LL_pos = self.player.pos + pygame.Vector2(5, 0)
        LR_pos = self.player.pos + pygame.Vector2(15, 0)
        LL_has_tree = Slope.block_has_tree(LL_pos)
        LR_has_tree = Slope.block_has_tree(LR_pos)

        if LL_has_tree or LR_has_tree:
            return True
        else:
            return False

    # draw the block based on slope height
    def draw_slope_block(self, screen_x, screen_y, height):
        # decide the shading of the block
        # r_g_b = 150 * height + 105
        # paint the slope an icy-light blue-type color
        # https://imagecolorpicker.com/color-code/e4f7ff
        r = 18 * height + 237
        g = 13 * height + 242
        color = (r, g, 255)
        rect_w = Slope.block_size
        rect_h = Slope.block_size

        rect = pygame.Rect(screen_x, screen_y, rect_w, rect_h)
        pygame.draw.rect(self.screen, color, rect)

    # draw the tree
    def draw_tree(self, screen_x, screen_y):
        # gradient = random.random()
        dark_green = (19, 164, 51)
        brown = (160, 97, 46)

        # create the geometry
        branches_1 = pygame.Rect(screen_x + 8, screen_y + 1, 4, 18)
        branches_2 = pygame.Rect(screen_x + 1, screen_y + 8, 18, 4)
        branches_3 = pygame.Rect(screen_x + 4, screen_y + 4, 12, 12)
        bark = pygame.Rect(screen_x + 9, screen_y + 9, 2, 2)

        # draw the rectangles
        pygame.draw.rect(self.screen, dark_green, branches_1)
        pygame.draw.rect(self.screen, dark_green, branches_2)
        pygame.draw.rect(self.screen, dark_green, branches_3)
        pygame.draw.rect(self.screen, brown, bark)

    # draw the avalanche chasing the player
    def draw_avalanche(self):
        white = (255, 255, 255)
        # we want each block of the avalanche to be between some y range on the screen
        avalanche_min = 50
        avalanche_max = 230
        avalanche_range = avalanche_max - avalanche_min

        # draw the avalanche as an array of long snow columns that are of dimension Slope.block_size * avalanche length
        for x in range(0, self.screen_w, Slope.block_size):
            # want a noisy avalanche, clip noise from 0 to 1
            pos = self.get_screen_UL_pos() + pygame.Vector2(x, 0)
            noise = min(((Noise.avalanche_noise(pos, 2000)) / 0.45) + 0.1, 1.0)
            avalanche_height = (avalanche_range * noise) + avalanche_min

            # avalanche column
            avalanche_length = Slope.block_size * (avalanche_height // Slope.block_size) - Slope.block_size
            avalanche_column = pygame.Rect(x, 0, Slope.block_size, avalanche_length)
            # last block of the avalanche column will be a grey color
            debris_hue = 40 * noise + 215
            debris_color = (debris_hue, debris_hue, 255)
            avalanche_debris = pygame.Rect(x, avalanche_length, Slope.block_size,  Slope.block_size)

            # draw white avalanche with the shadow
            pygame.draw.rect(self.screen, white, avalanche_column)
            pygame.draw.rect(self.screen, debris_color, avalanche_debris)

    # for each block, draw the slope, tree
    def draw(self):
        UL_x = int(self.get_screen_UL_pos_x())
        UL_y = int(self.get_screen_UL_pos_y())

        # render each block
        UL_corner_rem_x = UL_x % Slope.block_size
        UL_corner_rem_y = UL_y % Slope.block_size
        for x in range(UL_x - UL_corner_rem_x, UL_x + self.screen_w, Slope.block_size):
            screen_x = x - UL_x

            # python does a modulus flip for negative numbers. If a % b = r then -a % b = b - r
            for y in range(UL_y + (Slope.block_size - UL_corner_rem_y), UL_y - self.screen_h, - Slope.block_size):
                screen_y = UL_y - y

                # the noise functions really slow down the rendering
                pos = pygame.Vector2(x, y)
                height = Slope.get_slope_height(pos)
                has_tree = Slope.block_has_tree(pos)

                # draw the slope and trees
                self.draw_slope_block(screen_x, screen_y, height)
                if has_tree:
                    self.draw_tree(screen_x, screen_y)