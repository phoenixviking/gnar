import pygame
from player import Player
from slope import Slope
import math


class SkiPatrol:
    def __init__(self):
        # initialize pygame attributes
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.ticks = 0

        # initialize game states
        self.start = False
        self.pause = False
        self.game_over = True

        # initialize game attributes
        self.player = Player(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2), self.screen)
        self.slope = Slope(self.screen, self.player)

        # extract assets
        self.start_img = pygame.image.load("assets/gnar.png").convert_alpha()
        self.pause_img = pygame.image.load("assets/pause.png").convert_alpha()
        self.game_over_img = pygame.image.load("assets/game_over.png").convert_alpha()
        self.gnar_pts_img = pygame.image.load("assets/gnar_pts.png").convert_alpha()
        self.score_0 = pygame.image.load("assets/0.png").convert_alpha()
        self.score_1 = pygame.image.load("assets/1.png").convert_alpha()
        self.score_2 = pygame.image.load("assets/2.png").convert_alpha()
        self.score_3 = pygame.image.load("assets/3.png").convert_alpha()
        self.score_4 = pygame.image.load("assets/4.png").convert_alpha()
        self.score_5 = pygame.image.load("assets/5.png").convert_alpha()
        self.score_6 = pygame.image.load("assets/6.png").convert_alpha()
        self.score_7 = pygame.image.load("assets/7.png").convert_alpha()
        self.score_8 = pygame.image.load("assets/8.png").convert_alpha()
        self.score_9 = pygame.image.load("assets/9.png").convert_alpha()

    # game loop
    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # draw the slope, then player, then avalanche on top
            self.slope.draw()
            self.player.draw()
            self.slope.draw_avalanche()

            # handle key inputs for start / quit / pause
            self.handle_events()

            # wait to begin the game
            if not self.start:
                # draw the start banner
                self.draw_start()
                pygame.display.flip()
                continue

            # set FPS to 40
            self.dt = self.clock.tick(40) / 1000

            # check if game over
            if self.slope.player_collided():
                # draw game over banner
                self.draw_game_over()
                self.game_over = True
            else:
                if self.pause:
                    # draw pause banner
                    self.draw_pause()
                else:
                    # move the player
                    # 1. handle user events, get player's new x positions
                    delta_x = self.get_mouse_x() * self.dt
                    # 2. move player downhill (default = -10 pixels / frame), get player's new y positions
                    delta_y = self.get_translation_y(-10)
                    # 3. translate player
                    self.player.translate(delta_x, delta_y)
                    # 4. scroll on the grid accordingly
                    self.slope.update_screen_UL_pos()

                    # increment timer and draw score
                    self.ticks += self.dt
                    self.draw_score()

            # flip
            pygame.display.flip()

        # quit the game and close the window
        pygame.quit()
        quit()

    # draw opening menu
    def draw_start(self):
        self.screen.blit(self.start_img, self.start_img.get_rect(center=self.screen.get_rect().center))

    # draw pause menu
    def draw_pause(self):
        self.screen.blit(self.pause_img, self.pause_img.get_rect(center=self.screen.get_rect().center))

    # draw game over menu
    def draw_game_over(self):
        self.screen.blit(self.game_over_img, self.game_over_img.get_rect(center=self.screen.get_rect().center))

    # draw some score from 000-999
    def draw_score(self):
        self.screen.blit(self.gnar_pts_img, self.gnar_pts_img.get_rect(center=(150, 70)))

        # print each digit
        hundreds_digit = math.floor(self.ticks / 100)
        tens_digit = math.floor((self.ticks - (100 * hundreds_digit)) / 10)
        ones_digit = math.floor(self.ticks - (100 * hundreds_digit) - (10 * tens_digit))
        hundreds_img = self.score_0
        tens_img = self.score_0
        ones_img = self.score_0

        # get corresponding digit assets
        match hundreds_digit:
            case 0:
                hundreds_img = self.score_0
            case 1:
                hundreds_img = self.score_1
            case 2:
                hundreds_img = self.score_2
            case 3:
                hundreds_img = self.score_3
            case 4:
                hundreds_img = self.score_4
            case 5:
                hundreds_img = self.score_5
            case 6:
                hundreds_img = self.score_6
            case 7:
                hundreds_img = self.score_7
            case 8:
                hundreds_img = self.score_8
            case 9:
                hundreds_img = self.score_9

        match tens_digit:
            case 0:
                tens_img = self.score_0
            case 1:
                tens_img = self.score_1
            case 2:
                tens_img = self.score_2
            case 3:
                tens_img = self.score_3
            case 4:
                tens_img = self.score_4
            case 5:
                tens_img = self.score_5
            case 6:
                tens_img = self.score_6
            case 7:
                tens_img = self.score_7
            case 8:
                tens_img = self.score_8
            case 9:
                tens_img = self.score_9

        match ones_digit:
            case 0:
                ones_img = self.score_0
            case 1:
                ones_img = self.score_1
            case 2:
                ones_img = self.score_2
            case 3:
                ones_img = self.score_3
            case 4:
                ones_img = self.score_4
            case 5:
                ones_img = self.score_5
            case 6:
                ones_img = self.score_6
            case 7:
                ones_img = self.score_7
            case 8:
                ones_img = self.score_8
            case 9:
                ones_img = self.score_9

        # print hundreds, tens, ones
        self.screen.blit(hundreds_img, hundreds_img.get_rect(center=(75, 120)))
        self.screen.blit(tens_img, tens_img.get_rect(center=(150, 120)))
        self.screen.blit(ones_img, ones_img.get_rect(center=(220, 120)))

    # returns the difference between the mouse and the player in screen space
    def get_mouse_x(self):
        # respond to mouse movement in the x direction
        mouse_pos_x = pygame.mouse.get_pos()[0]
        # find the dist. b/w mouse & player screen location to calculate x-translation
        responsiveness = 0.15
        pos_x_delta = responsiveness * (mouse_pos_x - self.player.screen_pos.x)

        return pos_x_delta

    # handle key press events
    def handle_events(self):
        # respond to arrow key events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.pause:
                self.pause = False
            else:
                if self.game_over:
                    self.game_over = False
                    self.player.reset()

                self.ticks = 0
            self.start = True
        if keys[pygame.K_ESCAPE]:
            if self.pause:
                self.running = False
            else:
                self.pause = True

    # adjust speed that the player descends slope
    def get_translation_y(self, delta_y):
        # - camera is viewing the player from above, down the z axis
        # - player is constantly moving down in the y-axis, in the -y direction
        # - want to find delta y after factoring the change in slope height
        #   in the z direction

        # delta_y = downhill speed
        # delta_z = change in height of slope
        # find x, y locations of current and current + delta_y (default velocity)
        curr_pos = self.player.get_pos()
        next_pos = pygame.Vector2(curr_pos.x, curr_pos.y + delta_y)

        # find the change in height from current to next position
        curr_height = Slope.get_slope_height(curr_pos)
        next_height = Slope.get_slope_height(next_pos)
        delta_z = next_height - curr_height

        # decrease downhill speed if delta_z > 0, increase downhill speed if delta_z < 0
        translation_y = delta_y + (10 * delta_z * delta_y)

        # return translation_y
        return delta_y


# run the game
game = SkiPatrol()
game.play()
