import os
import random

import pygame as pg

PIPE_IMG = pg.transform.scale2x(
    pg.image.load(os.path.join('imgs', 'pipe.png')))


class Pipe:
    GAP = 200
    VEL = 8

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pg.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    # sets height of both pipes using the gap as a point of reference
    def set_height(self):
        self.height = random.randrange(40, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # checks for collision based on overlapping of masks
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)

        # offsets of the masks so collisions work well
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # point of collision for the bird
        # overlap will return none until there is overlap in the bird's mask
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # determins whether the bird hit the pipe or not
        if t_point or b_point:
            return True

        return False
