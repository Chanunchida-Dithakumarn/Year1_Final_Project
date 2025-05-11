import tkinter as tk
# import threading

from game import Game
from statistic import Statistic


class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Menu")
        self.root.geometry("500x500")

        self.root.configure(bg="darkseagreen")

        self.label = tk.Label(self.root, text="On the Way!", font=("Verdana", 50))
        self.label.pack(pady=80)

        self.play_btn = tk.Button(self.root, text="Play Game", font=("Verdana", 25), command=self.start_game)
        self.play_btn.pack(pady=20)

        self.stat_btn = tk.Button(self.root, text="Statistic", font=("Verdana", 25), command=self.stat_data)
        self.stat_btn.pack(pady=20)

        self.quit_btn = tk.Button(self.root, text="Quit", font=("Verdana", 20), command=self.root.destroy)
        self.quit_btn.pack(pady=30)

    def start_game(self):
        Game()

    def stat_data(self):
        root = tk.Tk()
        Statistic(root)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
