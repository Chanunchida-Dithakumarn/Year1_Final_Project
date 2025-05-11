import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Statistic:
    def __init__(self, root):
        self.data = "game_data.csv"
        self.df = None

        self.root = root
        self.root.title("Game Statistics")
        self.root.geometry("800x600")

        self.load_data()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.time_btn = ttk.Button(self.button_frame, text="Playing Duration", command=self.time_hist)
        self.time_btn.pack(side=tk.LEFT, padx=5)

        self.pie_btn = ttk.Button(self.button_frame, text="Item Collected", command=self.item_pie)
        self.pie_btn.pack(side=tk.LEFT, padx=5)

        self.coin_btn = ttk.Button(self.button_frame, text="Coin Collected", command=self.coin_table)
        self.coin_btn.pack(side=tk.LEFT, padx=5)

        self.obs_btn = ttk.Button(self.button_frame, text="Obstacles Passed", command=self.obs_bar)
        self.obs_btn.pack(side=tk.LEFT, padx=5)

        self.movement_obs_btn = ttk.Button(self.button_frame, text="Movement & Obstacles",
                                           command=self.movement_obs_scatter)
        self.movement_obs_btn.pack(side=tk.LEFT, padx=5)

        self.quit_btn = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_btn.pack(side=tk.BOTTOM, pady=10)

        self.tree = None
        self.canvas = None

    def load_data(self):
        self.df = pd.read_csv(self.data)

    def show_plot(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)

    def time_hist(self):
        self.delete_previous()
        fig, ax = plt.subplots(figsize=(6, 5))
        self.df['time'].hist(ax=ax, bins=20, color='steelblue')
        ax.set_title('Playing Duration Histogram')
        ax.set_xlabel('Duration (seconds)')
        ax.set_ylabel('Number of games played')
        self.show_plot(fig)

    def item_pie(self):
        self.delete_previous()
        shield = self.df['shield'].sum()
        star = self.df['star'].sum()

        labels = ['Shield', 'Star']
        values = [shield, star]
        color = ['plum', 'gold']

        fig, ax = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax.pie(values,
                                          labels=labels,
                                          colors=color,
                                          startangle=90,
                                          autopct='%1.1f%%',
                                          pctdistance=0.8)
        ax.set_title('Item Pie Chart')
        ax.legend(wedges,
                  labels,
                  title="Items",
                  loc="upper right",)
        self.show_plot(fig)

    def coin_table(self):
        self.delete_previous()
        coin = self.df['coins']
        coin_data = {'Min': coin.min(), 'Max': coin.max(),
                     'Mean': coin.mean(), 'Median': coin.median(),
                     'Mode': coin.mode().iloc[0] if not coin.mode().empty else 'N/A', 'SD': coin.std()}

        self.tree = ttk.Treeview(self.root, columns=('stat', 'value'), show='headings', height=len(coin_data))
        self.tree.heading('stat', text='Statistic')
        self.tree.heading('value', text='Value')

        for key, value in coin_data.items():
            val = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            self.tree.insert('', tk.END, values=(key, val))

        self.tree.pack(pady=20)

    def obs_bar(self):
        self.delete_previous()
        obs = self.df['obstacle']
        bins = range(0, obs.max() + 51, 50)
        labels = [f'{i}-{i + 50}' for i in bins[:-1]]

        obs_grouped = pd.cut(obs, bins=bins, labels=labels, right=False)

        obs_counts = obs_grouped.value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(6, 5))
        obs_counts.plot(kind='bar', ax=ax, color='limegreen')

        ax.set_title('Obstacle Bar Chart')
        ax.set_xlabel('Obstacles Passed')
        ax.set_ylabel('Number of Games Played')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

        self.show_plot(fig)

    def movement_obs_scatter(self):
        self.delete_previous()
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(self.df['obstacle'], self.df['movement'], color='salmon', alpha=0.6)

        ax.set_title('Player Movement & Obstacles')
        ax.set_xlabel('Obstacles Passed')
        ax.set_ylabel('Player Movement')
        self.show_plot(fig)

    def delete_previous(self):
        if hasattr(self, 'tree') and self.tree:
            self.tree.destroy()
            self.tree = None

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def run(self):
        self.root.mainloop()


# if __name__ == "__main__":
#     root = tk.Tk()
#     stat = Statistic(root)
#     stat.run()
