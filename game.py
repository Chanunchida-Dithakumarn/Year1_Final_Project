import pygame as pg
import random


class Config:
    width = 700
    height = 700
    color = {'R': (200, 0, 0), 'G': (30, 100, 70), 'B': (0, 0, 200), 'W': (200, 200, 200), 'BK': (50, 50, 50)}
    fps = 60


class Road:
    def __init__(self, screen):
        self.__screen = screen
        self.road_width = 380
        self.x = Config.width/2 - self.road_width/2
        self.y = 0

        self.road()
        self.road_line()

    def road(self):
        pg.draw.rect(self.__screen, Config.color['BK'], (self.x, self.y, 380, Config.height))

    def road_line(self):
        # two side line
        pg.draw.rect(self.__screen, Config.color['W'], (180, 0, 10, Config.height))
        pg.draw.rect(self.__screen, Config.color['W'], (510, 0, 10, Config.height))
        # two middle line
        l_x = 0
        for j in range(2):
            l_y = 0
            for i in range(9):
                pg.draw.rect(self.__screen, Config.color['W'], (290+l_x, 20 + l_y, 10, 40))
                l_y += 80
            l_x += 110


class Car:
    def __init__(self, screen):
        self.__screen = screen
        self.__car_size = (54, 100)
        self.__car = pg.image.load('red_car.png')
        self.__car = pg.transform.scale(self.__car, self.__car_size)

        # self.__x = Config.width/2 - self.__car_size[0]/2
        mid_lane_car = Config.width/2 - self.__car_size[0]/2
        self.__y = 550

        self.__lane_pos = [mid_lane_car - 110, mid_lane_car, mid_lane_car + 110]
        self.__lane = 1

        self.__speed = 5
        # self.x_move = 110
        self.__x = self.__lane_pos[self.__lane]
        self.pos_move = self.__x

        self.player_car()

    def player_car(self):
        self.__screen.blit(self.__car, (self.__x, self.__y))

    def car_move(self, direction):
        if direction == 'left' and self.__lane > 0:
            self.__lane -= 1
            self.pos_move = self.__lane_pos[self.__lane]
        elif direction == 'right' and self.__lane < 2:
            self.__lane += 1
            self.pos_move = self.__lane_pos[self.__lane]

    def car_update(self):
        if self.__x < self.pos_move:
            self.__x += self.__speed
            if self.__x > self.pos_move:
                self.__x = self.pos_move
        elif self.__x > self.pos_move:
            self.__x -= self.__speed
            if self.__x < self.pos_move:
                self.__x = self.pos_move


class Obstacle:
    def __init__(self, screen):
        self.__screen = screen
        self.__b_size = (80, 28)
        self.__pos_x = [200, 310, 420]
        self.__x = self.__pos_x[random.randint(0, 2)]
        self.__y = -30
        self.__speed = 5

        self.b = pg.image.load('barrier.png')
        self.b = pg.transform.scale(self.b, self.__b_size)

    def draw(self):
        self.__screen.blit(self.b, (self.__x, self.__y))

    def move(self):
        self.__y += self.__speed


class Game:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((Config.width, Config.height))
        pg.display.set_caption("On the Way!")
        self.__screen.fill(Config.color['G'])
        self.__clock = pg.time.Clock()

        self.__car = Car(self.__screen)

        self.__obstacle = []
        self.spawn = 0

        running = True
        while running:

            self.__road = Road(self.__screen)
            self.__car.car_update()
            self.__car.player_car()

            self.spawn += 1
            if self.spawn >= 60:
                self.__obstacle.append(Obstacle(self.__screen))
                self.spawn = 0

            for obs in self.__obstacle:
                obs.draw()
                obs.move()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a or event.key == pg.K_LEFT:
                        self.__car.car_move('left')
                    elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                        self.__car.car_move('right')

            pg.display.update()
            self.__clock.tick(Config.fps)

        pg.quit()


game = Game()
