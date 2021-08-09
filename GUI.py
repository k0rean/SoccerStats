import sys

from tkinter import Tk, Frame, Label, Button, StringVar
from tkinter.ttk import OptionMenu
from ttkthemes import ThemedStyle

from src.graphs import *
from src.utils import download_league, calculate_league_stats

sort_options = ['Points', 'HPoints', 'APoints', 'Scored', 'Conceded', 'Shots', 'Corners', 'OEff', 'DEff']

leagues = ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1', 'Liga NOS', 'Eredivisie',
           'Jupiler', 'Turkey', 'Greece', 'Premiership', 'Championship', 'La Liga2', 'Bundesliga2',
           'Serie B', 'Ligue 2']

years = ['17/18', '18/19', '19/20', '20/21', '21/22']

x_buttons_league = 150
x_buttons_stats = 330

button_width = 15
N = 30


class Application:
    def __init__(self, master=None):
        # Frame
        self.frame = Frame(master, width=1400, height=1200)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack()

        # Title
        self.msg = Label(self.frame, text="SoccerStats: \t\t\t\t")
        self.msg["font"] = ("Calibri", "40", "bold")
        self.msg.place(x=200, y=0)

        # Year
        self.active_year = StringVar(master)
        self.active_year.set(years[0])
        self.year_menu = OptionMenu(master, self.active_year, years[0], *years)
        self.year_menu.place(x=20, y=3 * N)

        # League
        self.active_league = StringVar(master)
        self.active_league.set(leagues[0])
        self.league_menu = OptionMenu(master, self.active_league, leagues[0], *leagues)
        self.league_menu.place(x=20, y=4 * N)

        # Initialize
        self.league_games = download_league(self.active_league, self.active_year)
        self.league_stats = calculate_league_stats(self.league_games)

        # Teams
        teams = self.league_stats.Team.to_list()
        # HTeam
        self.hTeam_vs = StringVar(master)
        self.hTeam_vs.set(teams[0])
        self.h_team_menu = OptionMenu(master, self.hTeam_vs, teams[0], *teams)
        self.h_team_menu.place(x=1100, y=3 * N)
        # ATeam
        self.aTeam_vs = StringVar(master)
        self.aTeam_vs.set(teams[1])
        self.a_team_menu = OptionMenu(master, self.aTeam_vs, teams[1], *teams)
        self.a_team_menu.place(x=1100, y=4 * N)

        # Sort by
        self.sortBy = StringVar(master)
        self.sortBy.set(sort_options[0])
        self.sort_menu = OptionMenu(master, self.sortBy, sort_options[0], *sort_options)
        self.sort_menu.place(x=1100, y=7 * N)

        # STATS
        def place_button(widget, text, width, func, x, y, color=''):
            if color == '':
                button = Button(widget)
            else:
                button = Button(widget, bg=color)
            button["text"] = text
            button["width"] = width
            button.bind("<Button-1>", func)
            button.place(x=x, y=y)

            return button

        # Stats buttons
        # Scored
        self.scored = place_button(self.frame, "Goals Scored", button_width, self.scored_func, x_buttons_stats, 3 * N)
        # Conceded
        self.conceded = place_button(self.frame, "Goals Conceded", button_width, self.conceded_func, x_buttons_stats,
                                     4 * N)
        # Diffs
        self.goal_diffs = place_button(self.frame, "Goal Difference", button_width, self.goal_diffs_func,
                                       x_buttons_stats,
                                       5 * N)
        # Corners
        self.corners = place_button(self.frame, "Corners", button_width, self.corners_func, x_buttons_stats,
                                    6 * N)
        # Shots
        self.shots = place_button(self.frame, "Shots", button_width, self.shots_func, x_buttons_stats,
                                  7 * N)
        # Shots_acc
        #self.shots_acc = place_button(self.frame, "Shots acc", button_width, self.shots_acc_func, x_buttons_stats,
        #                              8 * N)
        # Fouls
        self.fouls = place_button(self.frame, "Fouls", button_width, self.fouls_func, x_buttons_stats,
                                  9 * N)
        # Cards
        self.cards = place_button(self.frame, "Cards", button_width, self.cards_func, x_buttons_stats,
                                  10 * N)


        # Get League
        self.get_league = place_button(self.frame, "Get League", button_width, self.get_league_func, 20,
                                       5 * N, 'green')
        # Get Match
        self.get_match = place_button(self.frame, "Get Match", button_width, self.get_match_func, 1100,
                                      5 * N, 'green')
        # Get Table
        self.get_table = place_button(self.frame, "Get Table", button_width, self.get_table_func, 1100,
                                      8 * N, 'green')

        # Sort Table
        self.sort_table = place_button(self.frame, "Sort Table", 10, self.dummy_func, 1000,
                                       7 * N)
        # Home
        self.home = place_button(self.frame, "Home", 10, self.dummy_func, 1000,
                                 3 * N)
        # Away
        self.away = place_button(self.frame, "Away", 10, self.dummy_func, 1000,
                                 4 * N)
        # Quit
        self.quit = place_button(self.frame, "QUIT", 10, self.exit_func, 20,
                                 24 * N, 'red')

    # Buttons methods
    def scored_func(self, event):
        graph_goals(self.league_stats, "Goals Scored")

    def conceded_func(self, event):
        graph_goals(self.league_stats, "Goals Conceded")

    def corners_func(self, event):
        graph_situations(self.league_stats, "Corners")

    def fouls_func(self, event):
        graph_situations(self.league_stats, "Fouls")

    def shots_func(self, event):
        graph_situations_stack(self.league_stats, "Shots")

    def cards_func(self, event):
        graph_situations_stack(self.league_stats, "Cards")

    def goal_diffs_func(self, event):
        graph_situations(self.league_stats, "Goal Difference")

    def dummy_func(self, event):
        pass

    def get_league_func(self, event):
        self.league_games = download_league(self.active_league, self.active_year)
        self.league_stats = calculate_league_stats(self.league_games)
        teams = self.league_stats.Team.to_list()
        self.h_team_menu.set_menu(teams[0], *teams)
        self.a_team_menu.set_menu(teams[1], *teams)
        # Title
        self.msg = Label(self.frame,
                         text="SoccerStats: " + str(self.active_league.get()) + " " + str(self.active_year.get()))
        self.msg["font"] = ("Calibri", "40", "bold")
        self.msg.place(x=200, y=0)

    def get_match_func(self, event):
        # print_match_metrics()
        pass

    def get_table_func(self, event):
        # print_table_sorted()
        pass

    @staticmethod
    def exit_func(event):
        sys.exit()


if __name__ == '__main__':
    root = Tk()
    root.attributes('-fullscreen', True)
    Application(root)
    style = ThemedStyle(root)
    style.set_theme("scidgrey")
    root.mainloop()
