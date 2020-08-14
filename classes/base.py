import os

import pygame as pg

BASE_IMG = pg.transform.scale2x(
    pg.image.load(os.path.join('imgs', 'base.png')))


class Base:
    VEL = 8
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    # moves ground with pipes
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # uses two ground textures to rotate through to make it seem like the ground
        # continues on forever
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
