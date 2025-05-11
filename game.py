from config import Config
from road import Road
from car import Car
from obstacle import Obstacle
from item import Item
from coin import Coin

import pygame as pg
import random
import time
import pandas as pd
import os


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Config.width, Config.height))
        pg.display.set_caption('On the Way!')
        self.clock = pg.time.Clock()

        self.road = Road(self.screen)

        self.obs_list = []
        self.obs_collected = 0

        self.car = Car(self.screen)

        self.shield_list = []
        self.shield_collected = 0
        self.circle_time = 0
        self.life = False
        self.blank = 0

        self.star_list = []
        self.star_collected = 0
        self.star_time = 0
        self.star_coin = False

        self.coin_list = []
        self.coin_collected = 0

        self.game_over = False
        self.passed_time = 0
        self.start_time = 0
        self.playing_time = 0

        # self.root = None

        self.open_screen()
        # self.count_down()

        self.run()

    def run(self):
        self.start_time = time.time()
        self.playing_time = 0
        running = True
        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        self.car.move('left')
                    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                        self.car.move('right')

            if not self.game_over:
                self.playing_time = int(time.time() - self.start_time)
                self.road.update()
                self.road.draw()
                # obstacle
                self.obs_process()
                # item
                self.item_process()
                # coin
                self.coin_process()

                self.car.update()
                self.car.gen_car()
                self.time_display()
                self.coin_display()

            pg.display.update()
            self.clock.tick(Config.fps)

        self.save_collected()

        pg.quit()

    def obs_process(self):
        if self.passed_time % 55 == 0:
            num_obs = random.randint(1, 2)  # number of obs
            lane_list = []
            for i in range(num_obs):
                obs = Obstacle(self.screen)
                self.obs_list.append(obs)
                # check duplicated lane
                lane_list.append(obs)
            if num_obs == 2:
                lane_list[0].check_duplicated_lane(lane_list[1])

        self.passed_time += 1

        for obs in self.obs_list[:]:
            obs.update()
            if self.car.rect().colliderect(obs.rect()) and not self.life:
                print("Game Over")
                self.game_over = True
                # break
                self.game_over_screen()
                # running = False
            elif obs.y >= self.car.y + self.car.car_size[1] and not obs.passed:
                self.obs_collected += 1
                obs.passed = True
        self.obs_list = [obs for obs in self.obs_list if obs.y <= Config.height]

    def item_process(self):
        if self.passed_time % 470 == 0 and self.passed_time % 55 != 0:
            item = Item(self.screen)
            if item.item == 1:
                self.shield_list.append(item)
            elif item.item == 2:
                self.star_list.append(item)

        for shield in self.shield_list:
            shield.update()
            if self.car.rect().colliderect(shield.rect()):
                self.circle_time = 350
                self.shield_collected += 1
                self.shield_list.remove(shield)
                print("Shield Collected")

        if self.circle_time > 0:
            self.life = True
            if self.circle_time < 80:
                if 0 <= self.blank % 10 <= 3:
                    self.car.gen_circle()
                self.blank += 1
            else:
                self.car.gen_circle()
            self.circle_time -= 1
        else:
            self.life = False

        for star in self.star_list:
            star.update()
            if self.car.rect().colliderect(star.rect()):
                self.star_time = 350
                self.star_collected += 1
                self.star_list.remove(star)
                print("Star Collected")

        if self.star_time > 0:
            self.star_coin = True
            if self.star_time < 80:
                if 0 <= self.blank % 10 <= 3:
                    self.car.gen_star_cir()
                self.blank += 1
            else:
                self.car.gen_star_cir()
            self.star_time -= 1
        else:
            self.star_coin = False

    def coin_process(self):
        if self.passed_time % 70 == 0 and self.passed_time % 55 != 0:
            self.coin_list.append(Coin(self.screen))

        for coin in self.coin_list:
            coin.update()
            if self.car.rect().colliderect(coin.rect()):
                if self.star_coin:
                    self.coin_collected += 5
                else:
                    self.coin_collected += 1
                self.coin_list.remove(coin)
                print("Coin Collected")

    def open_screen(self):
        # self.screen.fill((0, 0, 0))
        dark_screen = pg.Surface((Config.width, Config.height))
        dark_screen.set_alpha(200)
        dark_screen.fill((0, 0, 0))
        self.screen.blit(dark_screen, (0, 0))

        # On the Way!
        name_font = pg.font.Font(None, 100)
        name_text = name_font.render("On the Way!", True, Config.color['W'])
        name_rect = name_text.get_rect(center=(Config.width // 2, Config.height // 2 - 80))
        self.screen.blit(name_text, name_rect)

        # play
        font = pg.font.Font(None, 60)
        play_text = font.render("PLAY", True, Config.color['BK'])
        play_rect = play_text.get_rect(center=(Config.width // 2, Config.height // 2 + 50))

        # main menu
        main_text = font.render("Main Menu", True, Config.color['BK'])
        main_rect = main_text.get_rect(center=(Config.width // 2, Config.height // 2 + 150))

        waiting = True
        while waiting:
            mouse_pos = pg.mouse.get_pos()
            mouse_click = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_click = True

            # play button
            if play_rect.collidepoint(mouse_pos):
                pg.draw.rect(self.screen, Config.color['dark_orange'], play_rect.inflate(10, 10))
                if mouse_click:
                    self.count_down()
                    waiting = False
            # main menu
            elif main_rect.collidepoint(mouse_pos):
                pg.draw.rect(self.screen, Config.color['dark_orange'], main_rect.inflate(10, 10))
                if mouse_click:
                    pg.quit()
                    waiting = False
            else:
                pg.draw.rect(self.screen, Config.color['orange'], play_rect.inflate(10, 10))
                pg.draw.rect(self.screen, Config.color['orange'], main_rect.inflate(10, 10))

            self.screen.blit(play_text, play_rect)
            self.screen.blit(main_text, main_rect)
            pg.display.update()
            self.clock.tick(Config.fps)

    def count_down(self):
        font = pg.font.Font(None, 300)
        self.screen.fill((0, 0, 0))

        for i in range(3, 0, -1):
            self.screen.fill((0, 0, 0))
            text = font.render(f"{i}", True, Config.color['R'])
            rect = text.get_rect(center=(Config.width // 2, Config.height // 2))
            self.screen.blit(text, rect)

            pg.display.update()
            pg.time.wait(1000)

    def game_over_screen(self):
        dark_screen = pg.Surface((Config.width, Config.height))
        dark_screen.set_alpha(170)
        dark_screen.fill((0, 0, 0))
        self.screen.blit(dark_screen, (0, 0))

        # game over
        over_font = pg.font.Font(None, 120)
        over_text = over_font.render("GAME OVER", True, (255, 0, 0))
        over_rect = over_text.get_rect(center=(Config.width // 2, Config.height // 2 - 100))
        self.screen.blit(over_text, over_rect)

        # restart
        font = pg.font.Font(None, 60)
        restart_text = font.render("RESTART", True, Config.color['BK'])
        restart_rect = restart_text.get_rect(center=(Config.width // 2, Config.height // 2))
        self.screen.blit(restart_text, restart_rect)

        # home
        home_text = font.render("Home", True, Config.color['BK'])
        home_rect = home_text.get_rect(center=(Config.width // 2, Config.height // 2 + 100))

        self.time_display()
        self.coin_display()

        waiting = True
        while waiting:

            mouse_pos = pg.mouse.get_pos()
            mouse_click = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.game_over = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_click = True

            # restart button
            if restart_rect.collidepoint(mouse_pos):
                pg.draw.rect(self.screen, Config.color['dark_orange'], restart_rect.inflate(10, 10))
                if mouse_click:
                    self.save_collected()
                    self.reset()
                    self.count_down()
                    self.run()
                    waiting = False

            # home
            elif home_rect.collidepoint(mouse_pos):
                pg.draw.rect(self.screen, Config.color['dark_orange'], home_rect.inflate(10, 10))
                if mouse_click:
                    self.reset()
                    self.open_screen()
                    waiting = False

            else:
                pg.draw.rect(self.screen, Config.color['orange'], restart_rect.inflate(10, 10))
                pg.draw.rect(self.screen, Config.color['orange'], home_rect.inflate(10, 10))

            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(home_text, home_rect)
            pg.display.update()
            self.clock.tick(Config.fps)

    def reset(self):
        self.road = Road(self.screen)

        self.obs_list = []
        self.obs_collected = 0

        self.car = Car(self.screen)

        self.shield_list = []
        self.shield_collected = 0
        self.circle_time = 0
        self.life = False
        self.blank = 0

        self.star_list = []
        self.star_collected = 0
        self.star_time = 0
        self.star_coin = False

        self.coin_list = []
        self.coin_collected = 0

        self.game_over = False
        self.passed_time = 0
        self.start_time = 0
        self.playing_time = 0

    def time_display(self):
        time_text = f"{self.playing_time}"
        font = pg.font.Font(None, 50)
        text_surface = font.render(time_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (20, 20))

    def coin_display(self):
        text = f"Coins: {self.coin_collected}"
        font = pg.font.Font(None, 38)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (550, 20))

    def save_collected(self):
        data = {
            "obstacle": self.obs_collected,
            "shield": self.shield_collected,
            "star": self.star_collected,
            "coins": self.coin_collected,
            "time": self.playing_time,
            "movement": self.car.movement,
        }
        df = pd.DataFrame([data])
        file_path = "game_data.csv"

        if os.path.exists(file_path):
            df_old = pd.read_csv(file_path, index_col=0)
            df_combined = pd.concat([df_old, df], ignore_index=True)
        else:
            df_combined = df

        df_combined.index += 1
        df_combined.to_csv(file_path, index=True)


if __name__ == "__main__":
    game = Game()
