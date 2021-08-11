import sys
from tkinter import Tk, Label, Button, StringVar, Text, END
from tkinter.ttk import OptionMenu

from tabulate import tabulate
from ttkthemes import ThemedStyle

from src.graphs import *
from src.utils import download_league, calculate_league_stats, get_table_sorted, get_match

sort_options = ['Points', 'HPoints', 'APoints', 'Scored', 'Conceded', 'Shots', 'Corners', 'OEff', 'DEff']

leagues = ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1', 'Liga NOS', 'Eredivisie',
           'Jupiler', 'Turkey', 'Greece', 'Premiership', 'Championship', 'La Liga2', 'Bundesliga2',
           'Serie B', 'Ligue 2']

years = ['17/18', '18/19', '19/20', '20/21', '21/22']

x_buttons_league = 150
x_buttons_stats = 1200

general_button_width = 15
N = 30

frame = {'w': 60, 'h': 40}

title = {'x': 0.3, 'y': 0.01}

league_info = {'x': 0.04, 'y': 0.05}
league_sel = {'x': 0.1, 'y': 0.05}
year_info = {'x': 0.04, 'y': 0.1}
year_sel = {'x': 0.1, 'y': 0.1}
league_year_get = {'x': 0.1, 'y': 0.15}

sort_table_info = {'x': 0.04, 'y': 0.25}
sort_table_sel = {'x': 0.1, 'y': 0.25}
sort_table_get = {'x': 0.1, 'y': 0.3}
table_text = {'x': 0.04, 'y': 0.35, 'h': 0.4, 'w': 0.2}

home_team_info = {'x': 0.3, 'y': 0.15}
home_team_sel = {'x': 0.36, 'y': 0.15}
away_team_info = {'x': 0.3, 'y': 0.2}
away_team_sel = {'x': 0.36, 'y': 0.2}
match_get = {'x': 0.36, 'y': 0.25}

big_text = {'x': 0.3, 'y': 0.3, 'h': 0.45, 'w': 0.25}

plots_info = {'x': 0.9, 'y': 0.3}
graphs_button_offset = 0.05

quit_but = {'x': 0.04, 'y': 0.95}


class Application:
    def __init__(self, master=None):

        # Title
        self.msg = Label(master, text="SoccerStats: " + ''.join([' '] * (max([len(item) for item in leagues]) + 6)),
                         font=("Calibri", "40", "bold"))
        self.msg.place(relx=title['x'], rely=title['y'])

        # Year
        self.active_year = StringVar(master)
        self.active_year.set(years[0])
        self.year_menu = OptionMenu(master, self.active_year, years[0], *years)
        self.year_menu.config(width=general_button_width)
        self.year_menu.place(relx=year_sel['x'], rely=year_sel['y'])

        # League
        self.active_league = StringVar(master)
        self.active_league.set(leagues[0])
        self.league_menu = OptionMenu(master, self.active_league, leagues[0], *leagues)
        self.league_menu.config(width=general_button_width)
        self.league_menu.place(relx=league_sel['x'], rely=league_sel['y'])

        # Initialize
        self.league_games = download_league(self.active_league, self.active_year)
        self.league_stats = calculate_league_stats(self.league_games)

        # Text
        self.big_text = Text(master)
        self.big_text.place(relx=big_text['x'], rely=big_text['y'], relwidth=big_text['w'], relheight=big_text['h'])

        self.table_text = Text(master)
        self.table_text.place(relx=table_text['x'], rely=table_text['y'], relwidth=table_text['w'],
                              relheight=table_text['h'])

        # Teams
        teams = self.league_stats.Team.to_list()
        # HTeam
        self.hTeam_vs = StringVar(master)
        self.hTeam_vs.set(teams[0])
        self.h_team_menu = OptionMenu(master, self.hTeam_vs, teams[0], *teams)
        self.h_team_menu.place(relx=home_team_sel['x'], rely=home_team_sel['y'])
        # ATeam
        self.aTeam_vs = StringVar(master)
        self.aTeam_vs.set(teams[1])
        self.a_team_menu = OptionMenu(master, self.aTeam_vs, teams[1], *teams)
        self.a_team_menu.place(relx=away_team_sel['x'], rely=away_team_sel['y'])

        # Sort by
        self.sortBy = StringVar(master)
        self.sortBy.set(sort_options[0])
        self.sort_menu = OptionMenu(master, self.sortBy, sort_options[0], *sort_options)
        self.sort_menu.config(width=general_button_width)
        self.sort_menu.place(relx=sort_table_sel['x'], rely=sort_table_sel['y'])

        def place_button(widget, text, width, func, x, y, color=''):
            if color == '':
                button = Button(widget)
            else:
                button = Button(widget, bg=color)
            button["text"] = text
            button["width"] = width
            button.bind("<Button-1>", func)
            button.place(relx=x, rely=y)

            return button

        # Stats buttons
        # Scored
        self.scored = place_button(master, "Goals Scored", general_button_width, self.scored_func, plots_info['x'],
                                   plots_info['y'] + 1 * graphs_button_offset)
        # Conceded
        self.conceded = place_button(master, "Goals Conceded", general_button_width, self.conceded_func,
                                     plots_info['x'],
                                     plots_info['y'] + 2 * graphs_button_offset)
        # Diffs
        self.goal_diffs = place_button(master, "Goal Difference", general_button_width, self.goal_diffs_func,
                                       plots_info['x'],
                                       plots_info['y'] + 3 * graphs_button_offset)
        # Corners
        self.corners = place_button(master, "Corners", general_button_width, self.corners_func, plots_info['x'],
                                    plots_info['y'] + 4 * graphs_button_offset)
        # Shots
        self.shots = place_button(master, "Shots", general_button_width, self.shots_func, plots_info['x'],
                                  plots_info['y'] + 5 * graphs_button_offset)
        # Fouls
        self.fouls = place_button(master, "Fouls", general_button_width, self.fouls_func, plots_info['x'],
                                  plots_info['y'] + 6 * graphs_button_offset)
        # Cards
        self.cards = place_button(master, "Cards", general_button_width, self.cards_func, plots_info['x'],
                                  plots_info['y'] + 7 * graphs_button_offset)
        # Get League
        self.get_league = place_button(master, "Get League", general_button_width, self.get_league_func,
                                       league_year_get['x'],
                                       league_year_get['y'], 'green')
        # Get Match
        self.get_match = place_button(master, "Get Match", general_button_width, self.get_match_func, match_get['x'],
                                      match_get['y'], 'green')
        # Get Table
        self.get_table = place_button(master, "Get Table", general_button_width, self.get_table_func,
                                      sort_table_get['x'], sort_table_get['y'], 'green')
        # Infos
        # league
        self.league_info = place_button(master, "League", general_button_width, self.dummy_func, league_info['x'],
                                        league_info['y'])
        # year
        self.year_info = place_button(master, "Year", general_button_width, self.dummy_func, year_info['x'],
                                      year_info['y'])
        # Plots
        self.plots_info = place_button(master, "Plots", general_button_width, self.dummy_func, plots_info['x'],
                                       plots_info['y'], 'orange')
        # Home
        self.home = place_button(master, "Home", general_button_width, self.dummy_func, home_team_info['x'],
                                 home_team_info['y'])
        # Away
        self.away = place_button(master, "Away", general_button_width, self.dummy_func, away_team_info['x'],
                                 away_team_info['y'])
        # Sort Table
        self.sort_table = place_button(master, "Sort Table", general_button_width, self.dummy_func,
                                       sort_table_info['x'], sort_table_info['y'])
        # Quit
        self.quit = place_button(master, "Quit", general_button_width, self.exit_func, quit_but['x'], quit_but['y'],
                                 'red')

    # Buttons methods
    def scored_func(self, event=None):
        graph_goals(self.league_stats, "Goals Scored per game")

    def conceded_func(self, event=None):
        graph_goals(self.league_stats, "Goals Conceded per game")

    def goal_diffs_func(self, event=None):
        graph_situations(self.league_stats, "Goal Difference per game")

    def corners_func(self, event=None):
        graph_situations(self.league_stats, "Corners per game")

    def fouls_func(self, event=None):
        graph_situations(self.league_stats, "Fouls per game")

    def shots_func(self, event=None):
        graph_situations_stack(self.league_stats, "Shots per game")

    def cards_func(self, event=None):
        graph_situations_stack(self.league_stats, "Cards per game")

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
        self.msg['text'] = "SoccerStats: " + str(self.active_league.get()) + " " + str(
            self.active_year.get()) + ''.join(
            [' '] * (max([len(item) for item in leagues]) - len(str(self.active_league.get()))))
        # Update Table - sorted by points
        self.sortBy.set(sort_options[0])
        self.get_table_func()

    def get_table_func(self, event=None):
        table = get_table_sorted(self.league_stats, self.sortBy)
        self.table_text.delete('1.0', END)
        self.table_text.insert(END, tabulate(table, headers='keys', tablefmt='psql'))

    def get_match_func(self, event=None):
        home, away = get_match(self.league_stats, self.hTeam_vs.get(), self.aTeam_vs.get())
        self.big_text.delete('1.0', END)
        # home
        self.big_text.insert(END, self.hTeam_vs.get() + ':\n')
        self.big_text.insert(END, '#' + str(home['Rank']).ljust(2, ' ') + ' place\t\t\t #' + str(home['HRank']).ljust(2,
                                                                                                                      ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['Scored']).ljust(2, ' ') + ' goals scored\t\t\t #' + str(
            home['HScored']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['Scored_1H']).ljust(2, ' ') + ' goals scored 1H\t\t\t #' + str(
            home['HScored_1H']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['Scored_2H']).ljust(2, ' ') + ' goals scored 2H\t\t\t #' + str(
            home['HScored_2H']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['Conceded']).ljust(2, ' ') + ' goals conceded\t\t\t #' + str(
            home['HConceded']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['Conceded_1H']).ljust(2, ' ') + ' goals conceded 1H\t\t\t #' + str(
            home['HConceded_1H']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['Conceded_2H']).ljust(2, ' ') + ' goals conceded 2H\t\t\t #' + str(
            home['HConceded_2H']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END,
                             '#' + str(home['Shots']).ljust(2, ' ') + ' shots\t\t\t #' + str(home['HShots']).ljust(2,
                                                                                                                   ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['Corners']).ljust(2, ' ') + ' corners\t\t\t #' + str(
            home['HCorners']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['OEff']).ljust(2, ' ') + ' ofensive efficiency\t #' + str(
            home['HOEff']).ljust(2, ' ') + ' home\n')
        self.big_text.insert(END, '#' + str(home['DEff']).ljust(2, ' ') + ' defensive efficiency\t#' + str(
            home['HDEff']).ljust(2, ' ') + ' home\n')
        # away
        self.big_text.insert(END, '\n')
        self.big_text.insert(END, self.aTeam_vs.get() + ':\n')
        self.big_text.insert(END, '#' + str(away['Rank']).ljust(2, ' ') + ' place\t\t\t #' + str(away['ARank']).ljust(2,
                                                                                                                      ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['Scored']).ljust(2, ' ') + ' goals scored\t\t\t #' + str(
            away['AScored']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['Scored_1H']).ljust(2, ' ') + ' goals scored 1H\t\t\t #' + str(
            away['AScored_1H']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['Scored_2H']).ljust(2, ' ') + ' goals scored 2H\t\t\t #' + str(
            away['AScored_2H']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['Conceded']).ljust(2, ' ') + ' goals conceded\t\t\t #' + str(
            away['AConceded']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['Conceded_1H']).ljust(2, ' ') + ' goals conceded 1H\t\t\t #' + str(
            away['AConceded_1H']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['Conceded_2H']).ljust(2, ' ') + ' goals conceded 2H\t\t\t #' + str(
            away['AConceded_2H']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END,
                             '#' + str(away['Shots']).ljust(2, ' ') + ' shots\t\t\t #' + str(away['AShots']).ljust(2,
                                                                                                                   ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['Corners']).ljust(2, ' ') + ' corners\t\t\t #' + str(
            away['ACorners']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['OEff']).ljust(2, ' ') + ' ofensive efficiency\t #' + str(
            away['AOEff']).ljust(2, ' ') + ' away\n')
        self.big_text.insert(END, '#' + str(away['DEff']).ljust(2, ' ') + ' defensive efficiency\t#' + str(
            away['ADEff']).ljust(2, ' ') + ' away\n')

    @staticmethod
    def exit_func(event=None):
        sys.exit()


if __name__ == '__main__':
    root = Tk()
    root.attributes('-fullscreen', True)
    Application(root)
    style = ThemedStyle(root)
    style.set_theme("scidgrey")
    root.mainloop()
