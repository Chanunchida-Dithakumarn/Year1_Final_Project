from config import Config
import pygame as pg
import random


class Obstacle:
    obs1 = pg.image.load('picture/barrier.png')
    obs2 = pg.image.load('picture/oil.png')
    obs3 = pg.image.load('picture/cone.png')

    def __init__(self, screen):
        self.__screen = screen

        # barrier
        self.__obs1 = Obstacle.obs1
        self.__obs1_size = (80, 28)
        self.__obs1 = pg.transform.scale(self.__obs1, self.__obs1_size)

        # oil
        self.__obs2 = Obstacle.obs2
        self.__obs2_size = (80, 50)
        self.__obs2 = pg.transform.scale(self.__obs2, self.__obs2_size)

        # cone
        self.__obs3 = Obstacle.obs3
        self.__obs3_size = (23, 26)
        self.__obs3 = pg.transform.scale(self.__obs3, self.__obs3_size)

        mid_lane = (Config.width / 2) - (self.__obs1_size[0] / 2)
        self.pos_lane = [mid_lane - 110, mid_lane, mid_lane + 110]
        self.lane_num = random.randint(0, 2)  # random lane
        self.x = self.pos_lane[self.lane_num]
        self.y = -20
        self.speed = Config.speed * 1.8
        self.passed = False

        self.obs = random.randint(1, 2)  # random obs

    def gen_obs1(self):
        self.__screen.blit(self.__obs1, (self.x, self.y))

    def gen_obs2(self):
        self.__screen.blit(self.__obs2, (self.x, self.y))  # oil
        self.__screen.blit(self.__obs3, (self.x + 30, self.y + 3))  # single cone

    def check_duplicated_lane(self, other):
        number = (0, 1, 2)
        if self.lane_num == other.lane_num:
            new = tuple(filter(lambda x: x != self.lane_num, number))
            other.lane_num = random.randint(new[0], new[1])
            other.x = self.pos_lane[other.lane_num]

    def update(self):
        if self.obs == 1:
            self.gen_obs1()
        elif self.obs == 2:
            self.gen_obs2()
        self.y += self.speed

    def rect(self):
        if self.obs == 1:
            return pg.Rect(self.x, self.y, self.__obs1_size[0], self.__obs1_size[1])
        elif self.obs == 2:
            return pg.Rect(self.x, self.y, self.__obs2_size[0], self.__obs2_size[1])
