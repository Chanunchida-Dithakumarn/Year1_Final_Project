from config import Config
import pygame as pg
import random


class Coin:
    def __init__(self, screen):
        self.__screen = screen
        self.__coin = pg.image.load('picture/coin.png')
        self.__coin_size = (70, 70)
        self.__coin = pg.transform.scale(self.__coin, self.__coin_size)

        mid_lane = (Config.width / 2) - (self.__coin_size[0] / 2)
        self.pos_lane = [mid_lane - 110, mid_lane, mid_lane + 110]
        self.lane_num = random.randint(0, 2)  # random lane
        self.x = self.pos_lane[self.lane_num]
        self.y = -70

        self.speed = Config.speed * 1.8

    def gen_coin(self):
        self.__screen.blit(self.__coin, (self.x, self.y))

    def update(self):
        self.gen_coin()
        self.y += self.speed

    def rect(self):
        return pg.Rect(self.x + 5, self.y + 5, self.__coin_size[0] - 10, self.__coin_size[1] - 10)
