import datetime
import sys
from tkinter import Tk, Label, Button, StringVar, Text, END, LEFT
from tkinter.ttk import OptionMenu

import pandas as pd
from tabulate import tabulate
from ttkthemes import ThemedStyle
from win32api import GetSystemMetrics

from src.graphs import *
from src.utils import download_league, calculate_league_stats, get_table_sorted, get_match

sort_options = ['Points', 'HPoints', 'APoints', 'Scored', 'Conceded', 'Shots', 'Corners', 'OEff', 'DEff']

leagues = ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1', 'Liga NOS', 'Eredivisie',
           'Jupiler', 'Turkey', 'Greece', 'Premiership', 'Championship', 'La Liga2', 'Bundesliga2',
           'Serie B', 'Ligue 2']

actual_time = datetime.datetime.now()
if actual_time.month >= 8:
    actual_year = actual_time.year + 1

years = ['{}/{}'.format(year - 2000, year - 2000 + 1) for year in range(2010, actual_year)]

screen_width = GetSystemMetrics(0)
if screen_width > 1500:
    general_button_width = 15
    general_font_size = 12
else:
    general_button_width = 13
    general_font_size = 10

general_font = ('Consolas', general_font_size)

frame = {'w': 60, 'h': 40}

title = {'x': 0.25, 'y': 0.0}
title_font = ('Calibri', '40', 'bold')

league_info = {'x': 0.02, 'y': 0.03}
league_sel = {'x': 0.1, 'y': 0.03}
year_info = {'x': 0.02, 'y': 0.08}
year_sel = {'x': 0.1, 'y': 0.08}
league_year_get = {'x': 0.1, 'y': 0.13}

sort_table_info = {'x': 0.02, 'y': 0.2}
sort_table_sel = {'x': 0.1, 'y': 0.2}
sort_table_get = {'x': 0.1, 'y': 0.25}
table_text = {'x': 0.02, 'y': 0.3, 'h': 0.6, 'w': 0.22}

home_team_info = {'x': 0.6, 'y': 0.12}
home_team_sel = {'x': 0.68, 'y': 0.12}
away_team_info = {'x': 0.6, 'y': 0.17}
away_team_sel = {'x': 0.68, 'y': 0.17}
match_get = {'x': 0.68, 'y': 0.22}

big_text = {'x': 0.45, 'y': 0.3, 'h': 0.65, 'w': 0.25}

pred_text = {'x': 0.67, 'y': 0.3, 'h': 0.65, 'w': 0.25}

plots_info = {'x': 0.92, 'y': 0.1}
graphs_button_offset = 0.05

theme_but = {'x': 0.92, 'y': 0.03}

quit_but = {'x': 0.02, 'y': 0.95}


class Application:
    def __init__(self, master=None):

        self.master = master

        self.master.tk.call('source', 'sun-valley.tcl')
        self.master.tk.call('set_theme', 'light')
        self.theme = 'light'

        # Title
        self.title = Label(self.master,
                         text="SoccerStats: " + ''.join([' '] * (max([len(item) for item in leagues]) + 6)),
                         font=title_font)
        self.title.place(relx=title['x'], rely=title['y'])

        # Year
        self.active_year = StringVar(self.master)
        self.active_year.set(years[0])
        self.year_menu = OptionMenu(self.master, self.active_year, years[0], *years)
        self.year_menu.config(width=general_button_width)
        self.year_menu.place(relx=year_sel['x'], rely=year_sel['y'])

        # League
        self.active_league = StringVar(self.master)
        self.active_league.set(leagues[0])
        self.league_menu = OptionMenu(self.master, self.active_league, leagues[0], *leagues)
        self.league_menu.config(width=general_button_width)
        self.league_menu.place(relx=league_sel['x'], rely=league_sel['y'])

        # Initialize
        self.league_games = download_league(self.active_league, self.active_year)
        self.league_stats = calculate_league_stats(self.league_games)

        # Text
        self.big_text = Label(self.master, font=general_font, justify=LEFT, anchor='nw')
        self.big_text.place(relx=big_text['x'], rely=big_text['y'], relwidth=big_text['w'], relheight=big_text['h'])

        self.table_text = Label(self.master, font=general_font, justify=LEFT, anchor='nw')
        self.table_text.place(relx=table_text['x'], rely=table_text['y'], relwidth=table_text['w'],
                              relheight=table_text['h'])

        self.pred_text = Label(self.master, font=general_font, justify=LEFT, anchor='nw')
        self.pred_text.place(relx=pred_text['x'], rely=pred_text['y'], relwidth=pred_text['w'],
                             relheight=pred_text['h'])

        # Teams
        teams = self.league_stats.Team.to_list()
        # HTeam
        self.hTeam_vs = StringVar(self.master)
        self.hTeam_vs.set(teams[0])
        self.h_team_menu = OptionMenu(self.master, self.hTeam_vs, teams[0], *teams)
        self.h_team_menu.place(relx=home_team_sel['x'], rely=home_team_sel['y'])
        # ATeam
        self.aTeam_vs = StringVar(self.master)
        self.aTeam_vs.set(teams[1])
        self.a_team_menu = OptionMenu(self.master, self.aTeam_vs, teams[1], *teams)
        self.a_team_menu.place(relx=away_team_sel['x'], rely=away_team_sel['y'])

        # Sort by
        self.sortBy = StringVar(self.master)
        self.sortBy.set(sort_options[0])
        self.sort_menu = OptionMenu(self.master, self.sortBy, sort_options[0], *sort_options)
        self.sort_menu.config(width=general_button_width)
        self.sort_menu.place(relx=sort_table_sel['x'], rely=sort_table_sel['y'])

        def place_button(widget, text, width, func, x, y, color=''):
            button = Button(widget, command=func, text=text, width=width)
            if color != '':
                button['bg'] = color
            button.place(relx=x, rely=y)

            return button

        # Stats buttons
        # Scored
        self.scored = place_button(self.master, "Goals Scored", general_button_width, self.scored_func, plots_info['x'],
                                   plots_info['y'] + 1 * graphs_button_offset)
        # Conceded
        self.conceded = place_button(self.master, "Goals Conceded", general_button_width, self.conceded_func,
                                     plots_info['x'],
                                     plots_info['y'] + 2 * graphs_button_offset)
        # Diffs
        self.goal_diffs = place_button(self.master, "Goal Difference", general_button_width, self.goal_diffs_func,
                                       plots_info['x'],
                                       plots_info['y'] + 3 * graphs_button_offset)
        # Corners
        self.corners = place_button(self.master, "Corners", general_button_width, self.corners_func, plots_info['x'],
                                    plots_info['y'] + 4 * graphs_button_offset)
        # Shots
        self.shots = place_button(self.master, "Shots", general_button_width, self.shots_func, plots_info['x'],
                                  plots_info['y'] + 5 * graphs_button_offset)
        # Fouls
        self.fouls = place_button(self.master, "Fouls", general_button_width, self.fouls_func, plots_info['x'],
                                  plots_info['y'] + 6 * graphs_button_offset)
        # Cards
        self.cards = place_button(self.master, "Cards", general_button_width, self.cards_func, plots_info['x'],
                                  plots_info['y'] + 7 * graphs_button_offset)
        # Get League
        self.get_league = place_button(self.master, "Get League", general_button_width, self.get_league_func,
                                       league_year_get['x'],
                                       league_year_get['y'], 'green')
        # Get Match
        self.get_match = place_button(self.master, "Get Match", general_button_width, self.get_match_func,
                                      match_get['x'],
                                      match_get['y'], 'green')
        # Get Table
        self.get_table = place_button(self.master, "Get Table", general_button_width, self.get_table_func,
                                      sort_table_get['x'], sort_table_get['y'], 'green')
        # Infos
        # league
        self.league_info = place_button(self.master, "League", general_button_width, self.dummy_func, league_info['x'],
                                        league_info['y'])
        # year
        self.year_info = place_button(self.master, "Year", general_button_width, self.dummy_func, year_info['x'],
                                      year_info['y'])
        # Plots
        self.plots_info = place_button(self.master, "Plots", general_button_width, self.dummy_func, plots_info['x'],
                                       plots_info['y'], 'orange')
        # Home
        self.home = place_button(self.master, "Home", general_button_width, self.dummy_func, home_team_info['x'],
                                 home_team_info['y'])
        # Away
        self.away = place_button(self.master, "Away", general_button_width, self.dummy_func, away_team_info['x'],
                                 away_team_info['y'])
        # Sort Table
        self.sort_table = place_button(self.master, "Sort Table", general_button_width, self.dummy_func,
                                       sort_table_info['x'], sort_table_info['y'])
        # Quit
        self.quit = place_button(self.master, "Quit", general_button_width, self.exit_func, quit_but['x'],
                                 quit_but['y'],
                                 'red')
        # Change theme
        self.theme = place_button(self.master, "Theme", general_button_width, self.theme_func, theme_but['x'],
                                  theme_but['y'])

    # Buttons methods
    def scored_func(self, event=None):
        graph_goals(self.league_stats, "Goals Scored per game", self.theme)

    def conceded_func(self, event=None):
        graph_goals(self.league_stats, "Goals Conceded per game", self.theme)

    def goal_diffs_func(self, event=None):
        graph_situations(self.league_stats, "Goal Difference per game", self.theme)

    def corners_func(self, event=None):
        graph_situations(self.league_stats, "Corners per game", self.theme)

    def fouls_func(self, event=None):
        graph_situations(self.league_stats, "Fouls per game", self.theme)

    def shots_func(self, event=None):
        graph_situations_stack(self.league_stats, "Shots per game", self.theme)

    def cards_func(self, event=None):
        graph_situations_stack(self.league_stats, "Cards per game", self.theme)

    def theme_func(self, event=None):
        if self.theme == 'dark':
            self.master.tk.call("set_theme", "light")
            self.theme = 'light'
        else:
            self.master.tk.call("set_theme", "dark")
            self.theme = 'dark'

    def dummy_func(self, event=None):
        pass

    def get_league_func(self, event=None):
        self.league_games = download_league(self.active_league, self.active_year)
        self.league_stats = calculate_league_stats(self.league_games)
        # Update teams
        teams = self.league_stats.Team.to_list()
        self.h_team_menu.set_menu(teams[0], *teams)
        self.a_team_menu.set_menu(teams[1], *teams)
        # Update Title
        self.title['text'] = "SoccerStats: " + str(self.active_league.get()) + " " + str(
            self.active_year.get()) + ''.join(
            [' '] * (max([len(item) for item in leagues]) - len(str(self.active_league.get()))))
        # Update Table - sorted by points
        self.sortBy.set(sort_options[0])
        self.get_table_func()
        # clear big_text
        self.big_text['text'] = ''

    def get_table_func(self, event=None):
        table = get_table_sorted(self.league_stats, self.sortBy)
        self.table_text['text'] = tabulate(table, headers='keys', tablefmt='psql', numalign='center')

    def get_match_func(self, event=None):
        # Big text
        home, away = get_match(self.league_stats, self.hTeam_vs.get(), self.aTeam_vs.get())
        data = ['Rank', 'Scored', 'Scored_1H', 'Scored_2H', 'Conceded', 'Conceded_1H', 'Conceded_2H',
                'Shots', 'ShotsT', 'Corners', 'OEff', 'DEff']
        # home
        _df = pd.DataFrame(home, columns=['#Geral', '#Home'])
        _df[self.hTeam_vs.get().ljust(10)] = data
        self.big_text['text'] = tabulate(_df.set_index(self.hTeam_vs.get().ljust(10), drop=True), headers='keys',
                                           tablefmt='psql', numalign='center')
        # away
        _df = pd.DataFrame(away, columns=['#Geral', '#Away'])
        _df[self.aTeam_vs.get().ljust(10)] = data
        self.big_text['text'] += "\n" + tabulate(_df.set_index(self.aTeam_vs.get().ljust(10), drop=True), headers='keys',
                                           tablefmt='psql', numalign='center')

        # Pred text
        _df_aux = self.league_games[
            (self.league_games.HomeTeam == self.hTeam_vs.get()) & (self.league_games.AwayTeam == self.aTeam_vs.get())]
        if len(_df_aux) == 0:
            self.pred_text['text'] = "This match hasn't occurred yet\n"
            return
        _df_aux = _df_aux.iloc[0]
        self.pred_text['text'] = "Played at {}\n\n".format(_df_aux.Date)
        ht = {'home': _df_aux.HTHG, 'away': _df_aux.HTAG}
        ft = {'home': _df_aux.FTHG, 'away': _df_aux.FTAG}
        odds = {'1': _df_aux.B365H, 'X': _df_aux.B365D, '2': _df_aux.B365A}
        shots = {'home': _df_aux.HS, 'away': _df_aux.AS}
        shots_target = {'home': _df_aux.HST, 'away': _df_aux.AST}
        corners = {'home': _df_aux.HC, 'away': _df_aux.AC}
        fouls = {'home': _df_aux.HF, 'away': _df_aux.AF}
        yellows = {'home': _df_aux.HY, 'away': _df_aux.AY}
        reds = {'home': _df_aux.HR, 'away': _df_aux.AR}
        self.pred_text['text'] += tabulate(pd.DataFrame([ft.values(), ht.values(), shots.values(), shots_target.values(), corners.values(),
                                                          fouls.values(), yellows.values(), reds.values()],
                                                         columns=[self.hTeam_vs.get(), self.aTeam_vs.get()],
                                                         index=['FT', 'HT', 'Shots', 'Shots target', 'Corners', 'Fouls',
                                                                'Yellow Cards', 'Red Cards']),
                                            headers='keys', tablefmt='psql', numalign='center')
        self.pred_text['text'] += "\n\n"
        self.pred_text['text'] += tabulate(
            pd.DataFrame([odds.values()], columns=[self.hTeam_vs.get(), 'X', self.aTeam_vs.get()],
                         index=['Odds']), headers='keys', tablefmt='psql', numalign='center')

    @staticmethod
    def exit_func(event=None):
        sys.exit()


if __name__ == '__main__':
    root = Tk()
    root.attributes('-fullscreen', True)
    Application(root)
    root.mainloop()
