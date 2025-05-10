from config import Config
import pygame as pg
import random


class Item:
    def __init__(self, screen):
        self.__screen = screen
        self.shield = pg.image.load('picture/shield.png')
        self.shield_size = (70, 70)
        self.shield = pg.transform.scale(self.shield, self.shield_size)

        self.star = pg.image.load('picture/star.png')
        self.star_size = (70, 70)
        self.star = pg.transform.scale(self.star, self.star_size)

        self.item = random.randint(1, 2)
        # self.item = 2

        mid_lane = (Config.width / 2) - (self.shield_size[0] / 2)
        self.pos_lane = [mid_lane - 110, mid_lane, mid_lane + 110]
        self.lane_num = random.randint(0, 2)  # random lane
        self.x = self.pos_lane[self.lane_num]
        self.y = -70

        self.speed = Config.speed * 1.8

    def gen_shield(self, x=None, y=None):
        if x is not None or y is not None:
            self.__screen.blit(self.shield, (x, y))
        else:
            self.__screen.blit(self.shield, (self.x, self.y))

    def gen_star(self, x=None, y=None):
        if x is not None or y is not None:
            self.__screen.blit(self.star, (x, y))
        else:
            self.__screen.blit(self.star, (self.x, self.y))

    def update(self):
        if self.item == 1:
            self.gen_shield()
        elif self.item == 2:
            self.gen_star()
        self.y += self.speed

    def rect(self):
        return pg.Rect(self.x + 5, self.y + 5, self.shield_size[0] - 10, self.shield_size[1] - 10)
