from config import Config
import pygame as pg


class Car:
    def __init__(self, screen):
        self.__screen = screen
        self.__car = pg.image.load('picture/red_car.png')
        self.car_size = (54, 100)
        self.__car = pg.transform.scale(self.__car, self.car_size)

        self.__circle = pg.image.load('picture/circle.png')
        self.__circle_size = (180, 200)
        self.__circle = pg.transform.scale(self.__circle, self.__circle_size)

        self.__star_cir = pg.image.load('picture/star_cir.png')
        self.__star_cir_size = (180, 200)
        self.__star_cir = pg.transform.scale(self.__star_cir, self.__star_cir_size)

        mid_lane = (Config.width / 2) - (self.car_size[0] / 2)
        self.pos_lane = [mid_lane-110, mid_lane, mid_lane+110]
        self.lane_num = 1
        self.x = self.pos_lane[self.lane_num]
        self.y = 500
        self.pos_move = self.x
        self.movement = 0  # number of lane changing
        self.speed = Config.speed*1.3
        self.gen_car()

    def gen_car(self):
        self.__screen.blit(self.__car, (self.x, self.y))

    def gen_circle(self):
        self.__screen.blit(self.__circle, (self.x + self.car_size[0]/2 - self.__circle_size[0]/2,
                                           self.y + self.car_size[1]/2 - self.__circle_size[1]/2))

    def gen_star_cir(self):
        self.__screen.blit(self.__star_cir, (self.x + self.car_size[0] / 2 - self.__circle_size[0] / 2,
                                             self.y + self.car_size[1] / 2 - self.__circle_size[1] / 2))

    def move(self, direction):
        old_lane = self.lane_num
        if direction == 'left' and self.lane_num > 0:
            self.lane_num -= 1
        elif direction == 'right' and self.lane_num < 2:
            self.lane_num += 1
        self.pos_move = self.pos_lane[self.lane_num]

        if old_lane != self.lane_num:
            self.movement += 1

    def update(self):
        if abs(self.x - self.pos_move) < self.speed:
            self.x = self.pos_move
        elif self.x > self.pos_move:  # left
            self.x -= self.speed
        elif self.x < self.pos_move:  # right
            self.x += self.speed

    def rect(self):
        return pg.Rect(self.x + 10, self.y + 10, self.car_size[0] - 20, self.car_size[1] - 20)
