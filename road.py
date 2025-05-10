from config import Config
import pygame as pg


class Road:
    def __init__(self, screen):
        self.__screen = screen
        self.road_width = 380
        self.x = Config.width/2 - self.road_width/2
        self.y = 0
        self.moved = 0
        self.speed = Config.speed-0.5

        self.draw()

    def side(self):
        pg.draw.rect(self.__screen, Config.color['G'], (0, 0, Config.width, Config.height))

    def road(self):
        pg.draw.rect(self.__screen, Config.color['BK'], (self.x, self.y, 380, Config.height))

    def road_line(self, y=0):
        # two side line
        pg.draw.rect(self.__screen, Config.color['W'], (180, 0, 10, Config.height))
        pg.draw.rect(self.__screen, Config.color['W'], (510, 0, 10, Config.height))
        # two middle line
        l_x = 0
        for j in range(2):
            l_y = 0
            for i in range(9):
                pg.draw.rect(self.__screen, Config.color['W'], (290 + l_x, 20 + l_y + y, 10, 40))
                l_y += 80
            l_x += 110

    def update(self):
        self.road_line(self.moved)
        self.road_line(self.moved - Config.height - 15)
        self.moved += self.speed
        if self.moved >= Config.height:
            self.moved = 0
            self.road_line(self.moved - Config.height - 15)

    def draw(self):
        self.side()
        self.road()
        self.update()
