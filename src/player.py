import pygame
import math

class Player():
    # player is bound within a 20 x 20 block
    # if UL corner of block is (0,0):
    # - left ski (skier's right ski)
    #   - UL pos: (5, 0)
    #   - w, h: (3, 20)
    # - right ski (skier's left ski)
    #   - UL pos: (12, 0)
    #   - w, h: (3, 20)

    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen
        self.dist_from_top = 250
        self.screen_pos = pygame.Vector2(self.screen.get_width() / 2, self.dist_from_top)
        self.tracks = []

    def get_pos(self):
        return self.pos

    def get_pos_x(self):
        return self.pos.x

    def get_pos_y(self):
        return self.pos.y

    def get_screen_pos(self):
        return self.screen_pos

    # reset player location
    def reset(self):
        self.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.tracks = []

    def add_track(self, track_pos):
        if len(self.tracks) > 1500:
            self.tracks.pop(0)

        self.tracks.append(track_pos)

    # translate player
    def translate(self, delta_x, delta_y):
        # delta y is always negative
        y_inc = -1
        x_inc = 2
        new_pos = self.pos + pygame.Vector2(delta_x, delta_y)
        if delta_x < 0:
            x_inc = -2

        # add a track for every (+x, -1) or (-x, -1) movement from curr pos to new pos
        for y in range(int(self.pos.y), int(new_pos.y), y_inc):
            # use floor + ceil to make sure that tracks are being added when the mouse pos is directly under the player
            for x in range(int(math.floor(self.pos.x)), int(math.ceil(new_pos.x)), x_inc):
                fresh_track = pygame.Vector2(x, y)
                self.add_track(fresh_track)

        self.pos.x += delta_x
        self.pos.y += delta_y

    # draw the skis
    def draw_skis(self):
        dark_grey = (120, 120, 120)

        left_ski = pygame.Rect(self.screen_pos.x + 5, self.screen_pos.y, 3, 20)
        right_ski = pygame.Rect(self.screen_pos.x + 12, self.screen_pos.y, 3, 20)

        pygame.draw.rect(self.screen, dark_grey, left_ski)
        pygame.draw.rect(self.screen, dark_grey, right_ski)

    # draw the ski marks in the snow behind the player
    def draw_tracks(self):
        shadow = (210, 210, 230)

        for track in self.tracks:
            delta_from_player = self.pos - track  # (0, 3) - (-1, 5)
            track_screen_pos_x = self.screen_pos.x - delta_from_player.x
            track_screen_pos_y = self.screen_pos.y + delta_from_player.y
            left_track = pygame.Rect(track_screen_pos_x + 6, track_screen_pos_y, 2, 2)
            right_track = pygame.Rect(track_screen_pos_x + 14, track_screen_pos_y, 2, 2)

            pygame.draw.rect(self.screen, shadow, left_track)
            pygame.draw.rect(self.screen, shadow, right_track)

    # draw player and their ski tracks
    def draw(self):
        self.draw_skis()
        self.draw_tracks()