import pygame
import math


class Noise:

    @staticmethod
    # outputs a decimal in range [0, 1]
    def slope_noise(pos, fbm_scale):
        # get fbm noise
        fbm = Noise.fbm(pos / fbm_scale)
        # fbm seems to output in range 0.3 to 0.7, so scale it over maximum spread in [0, 1]
        scaled = min(((fbm / 0.4) + 0.3), 1.0)
        # divide the noise into 0.2 intervals to give a more pixelated look
        slope_noise = min(0.2 * (scaled // 0.2) + 0.2, 1.0)

        return slope_noise

    @staticmethod
    # outputs a decimal in range [0, 1]
    def trees_noise(pos, perlin_scale, fbm_scale):
        # get perlin noise (creates patches
        perlin = Noise.perlin(pos / perlin_scale)
        # get fbm noise (creates irregularity
        fbm = Noise.fbm(pos / fbm_scale)
        # LERP between perlin and fbm
        trees_noise = Noise.mix(fbm, perlin, 0.65)

        return trees_noise

    @staticmethod
    # fbm scale should be relatively smaller to make the avalanches noisier
    # and to make it look like the debris cloud is rumbling
    def avalanche_noise(pos, fbm_scale):
        fbm = Noise.fbm(pos / fbm_scale)

        return fbm

    @staticmethod
    # divide uv by the amount you want to scale the perlin noise!
    def perlin(uv):
        uvXLYL = Noise.floor(uv)
        uvXHYL = uvXLYL + pygame.Vector2(1, 0)
        uvXHYH = uvXLYL + pygame.Vector2(1, 1)
        uvXLYH = uvXLYL + pygame.Vector2(0, 1)

        surflet_sum = (Noise.surflet(uv, uvXLYL) + Noise.surflet(uv, uvXHYL)
                       + Noise.surflet(uv, uvXHYH) + Noise.surflet(uv, uvXLYH))

        # set output from 0 to 1
        sum_normalized = (surflet_sum + 1.0) / 2.0

        return sum_normalized

    @staticmethod
    # Compute the dot product between each random vector and each corner-to-point vector
    def surflet(pos, grid_point):
        dist_x = abs(pos.x - grid_point.x)
        dist_y = abs(pos.y - grid_point.y)

        t_x = 1 - 6 * pow(dist_x, 5.0) + 15 * pow(dist_x, 4.0) - 10 * pow(dist_x, 3.0)
        t_y = 1 - 6 * pow(dist_y, 5.0) + 15 * pow(dist_y, 4.0) - 10 * pow(dist_y, 3.0)
        # Get the random vector for the grid point
        gradient = 2.0 * Noise.random2(grid_point)
        # Get the vector from the grid point to P
        diff = pos - grid_point
        # Get the value of our height field by dotting grid->P with our gradient
        height = diff.dot(gradient)

        # Scale our height field (i.e.reduce it) by our polynomial falloff function
        return height * t_x * t_y

    @staticmethod
    def random2(pos):
        vec_2 = pygame.Vector2(pos.dot(pygame.Vector2(127.1, 311.7)),
                               pos.dot(pygame.Vector2(269.5, 183.3)))

        return Noise.fract_vec2(Noise.sin(vec_2) * 43758.5453)

    @staticmethod
    # fractal brownian motion
    def fbm(uv):
        total = 0
        persistence = 0.15
        octaves = 10  # changes frequency of ripples
        freq = 18  # changes spacing of noise
        amp = 3.5  # changes height of spikes
        for i in range(octaves):
            freq *= 1.8  # was 2.0
            amp *= persistence
            total += Noise.interp_noise(uv.x * freq, uv.y * freq) * amp

        return pow(total, 1.4)

    @staticmethod
    def interp_noise(x, y):
        int_x = int(math.floor(x))
        fract_x = Noise.fract_float(x)
        int_y = int(math.floor(y))
        fract_y = Noise.fract_float(y)

        v1 = Noise.noise(pygame.Vector2(int_x, int_y))
        v2 = Noise.noise(pygame.Vector2(int_x + 1, int_y))
        v3 = Noise.noise(pygame.Vector2(int_x, int_y + 1))
        v4 = Noise.noise(pygame.Vector2(int_x + 1, int_y + 1))

        i1 = Noise.mix(v1, v2, fract_x)
        i2 = Noise.mix(v3, v4, fract_x)

        return Noise.mix(i1, i2, fract_y)

    @staticmethod
    def noise(pos):
        return Noise.fract_float(math.sin(pos.dot(pygame.Vector2(127.1, 311.7))) * 43758.5453)

    @staticmethod
    def sin(vec_2: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(math.sin(vec_2.x), math.sin(vec_2.y))

    @staticmethod
    def fract_vec2(vec_2: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(vec_2.x - math.floor(vec_2.x), vec_2.y - math.floor(vec_2.y))

    @staticmethod
    def fract_float(x: float) -> float:
        return x - math.floor(x)

    @staticmethod
    def floor(vec_2: pygame.Vector2):
        return pygame.Vector2(math.floor(vec_2.x), math.floor(vec_2.y))

    @staticmethod
    def mix(x, y, a):
        return x * (1 - a) + y * a
