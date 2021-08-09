import os
import urllib.request

from tkinter import *
from ttkthemes import ThemedStyle
import tkinter.ttk as ttk

from src.graphs import *
from tabulate import tabulate

root = ""
t1, t2 = "", ""
w3, w4, w5 = "", "", ""
active_league = "Premier League"
active_year = "20/21"
league_games = ""
league_stats = ""
sortBy = ""
sort_options = ['Points', 'HPoints', 'APoints', 'Scored', 'Conceded', 'Shots', 'Corners', 'OEff', 'DEff']

h_team_vs, aTeam_vs = "", ""

league_codes = {'Premier League': 'E0',
                'La Liga': 'SP1',
                'Bundesliga': 'D1',
                'Serie A': 'I1',
                'Ligue 1': 'F1',
                'Liga NOS': 'P1',
                'Eredivisie': 'N1',
                'Jupiler': 'B1',
                'Turkey': 'T1',
                'Greece': 'G1',
                'Premiership': 'SC0',
                'Championship': 'E1',
                'La Liga2': 'SP2',
                'Bundesliga2': 'D2',
                'Serie B': 'I2',
                'Ligue 2': 'F2'}

x_buttons_league = 150
x_buttons_stats = 330

button_width = 15
N = 30


class Application:
    def __init__(self, master=None):
        global t1, t2, w3, w4, w5

        self.widget1 = Frame(master, width=1400, height=1200)
        self.widget1.grid_rowconfigure(0, weight=1)
        self.widget1.grid_columnconfigure(0, weight=1)
        self.widget1.pack()
        ## Title
        self.msg = Label(self.widget1, text="SoccerStats: \t\t\t\t")
        self.msg["font"] = ("Calibri", "40", "bold")
        self.msg.place(x=200, y=0)

        ## Text
        t1 = Text(root, height=28, width=63)
        t1.place(x=450, y=3*N)

        t2 = Text(root, height=20, width=37)
        t2.place(x=20, y=6*N)

        ## Year
        global active_year
        years = ['17/18', '18/19', '19/20', '20/21', '21/22']
        active_year = StringVar(master)
        active_year.set(years[-1])
        w1 = ttk.OptionMenu(master, active_year, years[-1], *years)
        w1.place(x=20, y=3*N)

        ## League
        global active_league
        leagues = ['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1', 'Liga NOS', 'Eredivisie',
                   'Jupiler', 'Turkey', 'Greece', 'Premiership', 'Championship', 'La Liga2', 'Bundesliga2',
                   'Serie B', 'Ligue 2']
        active_league = StringVar(master)
        active_league.set(leagues[0])
        w2 = ttk.OptionMenu(master, active_league, leagues[0], *leagues)
        w2.place(x=20, y=4*N)

        ## Teams
        global hTeam_vs
        teams = league_stats.Team.to_list()
        hTeam_vs = StringVar(master)
        hTeam_vs.set(teams[0])
        w3 = ttk.OptionMenu(master, hTeam_vs, teams[0], *teams)
        w3.place(x=1100, y=3*N)

        global aTeam_vs
        teams = league_stats.Team.to_list()
        aTeam_vs = StringVar(master)
        aTeam_vs.set(teams[1])
        w4 = ttk.OptionMenu(master, aTeam_vs, teams[1], *teams)
        w4.place(x=1100, y=4*N)

        global sortBy
        sortBy = StringVar(master)
        sortBy.set(sort_options[0])
        w5 = ttk.OptionMenu(master, sortBy, sort_options[0], *sort_options)
        w5.place(x=1100, y=7*N)

        # STATS
        ## Scored
        self.scored = ttk.Button(self.widget1)
        self.scored["text"] = "Goals Scored"
        self.scored["width"] = button_width
        self.scored.bind("<Button-1>", self.scored_func)
        self.scored.place(x=x_buttons_stats, y=3*N)
        ## Conceded
        self.conceded = ttk.Button(self.widget1)
        self.conceded["text"] = "Goals Conceded"
        self.conceded["width"] = button_width
        self.conceded.bind("<Button-1>", self.conceded_func)
        self.conceded.place(x=x_buttons_stats, y=4*N)
        ## Diffs
        self.diffs = ttk.Button(self.widget1)
        self.diffs["text"] = "Performance"
        self.diffs["width"] = button_width
        self.diffs.bind("<Button-1>", self.diffs_func)
        self.diffs.place(x=x_buttons_stats, y=5*N)
        ## Corners
        self.corners = ttk.Button(self.widget1)
        self.corners["text"] = "Corners"
        self.corners["width"] = button_width
        self.corners.bind("<Button-1>", self.corners_func)
        self.corners.place(x=x_buttons_stats, y=6*N)
        ## Shots
        self.shots = ttk.Button(self.widget1)
        self.shots["text"] = "Shots"
        self.shots["width"] = button_width
        self.shots.bind("<Button-1>", self.shots_func)
        self.shots.place(x=x_buttons_stats, y=7*N)
        """
		## Shots_acc
		self.shots_acc = ttk.Button(self.widget1)
		self.shots_acc["text"] = "Shots accuracy"
		self.shots_acc["width"] = 15
		self.shots_acc.bind("<Button-1>", self.shots_acc_func)
		self.shots_acc.place(x=x_buttons_stats, y=8*N)
		"""
        ## Fouls
        self.fouls = ttk.Button(self.widget1)
        self.fouls["text"] = "Fouls"
        self.fouls["width"] = button_width
        self.fouls.bind("<Button-1>", self.fouls_func)
        self.fouls.place(x=x_buttons_stats, y=8*N)

        ## Cards
        self.cards = ttk.Button(self.widget1)
        self.cards["text"] = "Cards"
        self.cards["width"] = button_width
        self.cards.bind("<Button-1>", self.cards_func)
        self.cards.place(x=x_buttons_stats, y=9*N)

        ## get league
        self.liganos = Button(self.widget1, bg='green')
        self.liganos["text"] = "Get League"
        self.liganos["width"] = button_width
        self.liganos.bind("<Button-1>", self.getLeague_func)
        self.liganos.place(x=20, y=5*N)

        ## get match
        self.liganos = Button(self.widget1, bg='green')
        self.liganos["text"] = "Get Match"
        self.liganos["width"] = button_width
        self.liganos.bind("<Button-1>", self.getMatch_func)
        self.liganos.place(x=1100, y=5*N)

        ## get match
        self.liganos = Button(self.widget1, bg='green')
        self.liganos["text"] = "Get Table"
        self.liganos["width"] = button_width
        self.liganos.bind("<Button-1>", self.getTable_func)
        self.liganos.place(x=1100, y=8*N)

        ## Home
        self.ligue1 = Button(self.widget1)
        self.ligue1["text"] = "Sort Table"
        self.ligue1["width"] = 10
        self.ligue1.bind("<Button-1>", self.dummy_func)
        self.ligue1.place(x=1000, y=7*N)

        ## Home
        self.ligue1 = Button(self.widget1)
        self.ligue1["text"] = "Home"
        self.ligue1["width"] = 10
        self.ligue1.bind("<Button-1>", self.dummy_func)
        self.ligue1.place(x=1000, y=3*N)

        ## Away
        self.ligue1 = Button(self.widget1)
        self.ligue1["text"] = "Away"
        self.ligue1["width"] = 10
        self.ligue1.bind("<Button-1>", self.dummy_func)
        self.ligue1.place(x=1000, y=4*N)

        ## EXIT
        self.ligue1 = Button(self.widget1, bg='red')
        self.ligue1["text"] = "QUIT"
        self.ligue1["width"] = button_width
        self.ligue1.bind("<Button-1>", self.exit_func)
        self.ligue1.place(x=20, y=24*N)

    ### Metodos dos butoes
    def scored_func(self, event):
        global league_stats
        graph_goals(league_stats, "Goals Scored")

    def conceded_func(self, event):
        graph_goals(league_stats, "Goals Conceded")

    def corners_func(self, event):
        graph_situations(league_stats, "Corners")

    def fouls_func(self, event):
        graph_situations(league_stats, "Fouls")

    def shots_func(self, event):
        graph_situations_stack(league_stats, "Shots")

    def cards_func(self, event):
        graph_situations_stack(league_stats, "Cards")

    def diffs_func(self, event):
        graph_situations(league_stats, "Performance")

    def dummy_func(self, event):
        pass

    def getLeague_func(self, event):
        global league_games
        global league_stats
        global active_league
        global w3, w4
        getLeague()
        calculateStats(league_games)
        teams = league_stats.Team.to_list()
        w3.set_menu(teams[0], *teams)
        w4.set_menu(teams[1], *teams)
        ## Title
        self.msg = Label(self.widget1,
                         text="SoccerStats: " + str(active_league.get()) + " " + str(active_year.get()) + "\t\t\t\t")
        self.msg["font"] = ("Calibri", "40", "bold")
        self.msg.place(x=200, y=0)

    def getMatch_func(self, event):
        print_match_metrics()

    def getTable_func(self, event):
        print_table_sorted()

    def exit_func(self, event):
        import sys
        sys.exit()


def initGUI():
    global root
    root = Tk()
    root.attributes('-fullscreen', True)
    Application(root)
    style = ThemedStyle(root)
    style.set_theme("scidgrey")
    root.mainloop()


def getLeague():
    global active_league
    global active_year
    global league_games
    if type(active_league) is str:
        filename = league_codes[active_league] + ".csv"
    else:
        filename = league_codes[active_league.get()] + ".csv"
    if type(active_year) is str:
        url = 'http://www.football-data.co.uk/mmz4281/' + active_year.replace('/', '') + '/' + filename
    else:
        url = 'http://www.football-data.co.uk/mmz4281/' + active_year.get().replace('/', '') + '/' + filename
    urllib.request.urlretrieve(url, filename)

    league_games = pd.read_csv(filename)
    os.remove(filename)


def calculateStats(games):
    global league_stats
    teams = list(set([*games.HomeTeam, *games.AwayTeam]))
    _df_homeGames = games.groupby('HomeTeam')
    _df_awayGames = games.groupby('AwayTeam')
    res = []
    for team in teams:
        res.append(calculateStatsTeam(_df_homeGames.get_group(team), _df_awayGames.get_group(team)))

    df = pd.concat(res).reset_index(drop=True)
    df.columns = ['Team', 'HGames', 'HPoints', 'HPoints1H', 'HPoints2H', 'HScored1H', 'HScored2H', 'HConceded1H',
                  'HConceded2H', 'HShotsFavor', 'HShotsAgainst', 'HShotsTFavor', 'HShotsTAgainst', 'HFoulsCommited',
                  'HFoulsSuffered',
                  'HCornersFavor', 'HCornersAgainst', 'HYellowFavor', 'HYellowAgainst', 'HRedFavor', 'HRedAgainst',
                  'AGames', 'APoints', 'APoints1H', 'APoints2H', 'AScored1H', 'AScored2H',
                  'AConceded1H', 'AConceded2H', 'AShotsFavor', 'AShotsAgainst', 'AShotsTFavor', 'AShotsTAgainst',
                  'AFoulsCommited', 'AFoulsSuffered', 'ACornersFavor', 'ACornersAgainst', 'AYellowFavor',
                  'AYellowAgainst',
                  'ARedFavor', 'ARedAgainst', 'W', 'D', 'L']
    league_stats = df.iloc[(df.HPoints + df.APoints).sort_values(ascending=False).index].reset_index(drop=True)
    print_table()
    print_league_metrics()


def print_table():
    global t1
    _df = league_stats.copy(deep=True)
    _df['Pts'] = _df['HPoints'] + _df['APoints']
    _df['GD'] = (((_df['HScored1H'] + _df['HScored2H'] - _df['HConceded1H'] - _df['HConceded2H']) * _df['HGames']) +
                 ((_df['AScored1H'] + _df['AScored2H'] - _df['AConceded1H'] - _df['AConceded2H']) * _df[
                     'AGames'])).astype('float').round(0).astype('int')
    _df = _df[['Team', 'W', 'D', 'L', 'GD', 'Pts']]
    _df.index = _df.index + 1
    _df.index.name = '#'
    if not type(t1) is str:
        t1.delete('1.0', END)
        t1.insert(END, tabulate(_df, headers='keys', tablefmt='psql'))


def print_league_metrics():
    global t2

    _df = league_games.mean()
    index_list = ['Goals 1H', 'Goals 2H', 'Goals Home', 'Goals Away', 'Shots Home', 'Shots Away', 'Corners Home',
                  'Corners Away',
                  'Fouls Home', 'Fouls Away']  # , 'Ofensive Efficiency', 'Defensive Efficiency']
    values_list = [(_df.loc['HTHG'] + _df.loc['HTAG']).round(2),
                   (_df.loc['FTHG'] + _df.loc['FTAG'] - _df.loc['HTHG'] - _df.loc['HTAG']).round(2),
                   (_df.loc['FTHG'].round(2)), (_df.loc['FTAG'].round(2)),
                   (_df.loc['HS'].round(2)), (_df.loc['AS'].round(2)),
                   (_df.loc['HC'].round(2)), (_df.loc['AC'].round(2)),
                   (_df.loc['HF'].round(2)), (_df.loc['AF'].round(2))]  # ,
    _df_metrics = pd.DataFrame([values_list], columns=index_list).transpose()
    _df_metrics.index.name = 'League metrics'
    _df_metrics = _df_metrics.rename({0: 'per game'}, axis=1)
    if not type(t2) is str:
        t2.delete('1.0', END)
        t2.insert(END, tabulate(_df_metrics, headers='keys', tablefmt='psql'))


def print_table_sorted():
    global sortBy
    global league_stats
    global t1
    _df = league_stats.copy(deep=True)
    _df['Scored'] = (_df.HScored1H + _df.HScored2H) * _df.HGames + (_df.AScored1H + _df.AScored2H) * _df.AGames
    _df['Conceded'] = (_df.HConceded1H + _df.HConceded2H) * _df.HGames + (
                _df.AConceded1H + _df.AConceded2H) * _df.AGames
    _df['Points'] = _df.HPoints + _df.APoints
    _df['Shots'] = (_df.HShotsFavor * _df.HGames + _df.AShotsFavor * _df.AGames) / (_df.HGames + _df.AGames)
    _df['Corners'] = (_df.HCornersFavor * _df.HGames + _df.ACornersFavor * _df.AGames) / (_df.HGames + _df.AGames)
    _df['OEff'] = (((_df.HScored1H + _df.HScored2H) / (_df.HShotsFavor + _df.HCornersFavor)) * _df.HGames +
                   ((_df.AScored1H + _df.AScored2H) / (_df.AShotsFavor + _df.ACornersFavor)) * _df.AGames) / (
                              _df.HGames + _df.AGames)
    _df['DEff'] = (((_df.HConceded1H + _df.HConceded2H) / (_df.HShotsAgainst + _df.HCornersAgainst)) * _df.HGames +
                   ((_df.AConceded1H + _df.AConceded2H) / (_df.AShotsAgainst + _df.ACornersAgainst)) * _df.AGames) / (
                              _df.HGames + _df.AGames)

    bool_var = False
    if sortBy.get() == 'Conceded' or sortBy.get() == 'DEff':
        bool_var = True

    _df = _df[['Team', sortBy.get()]]
    _df = _df.sort_values(sortBy.get(), ascending=bool_var).reset_index(drop=True)
    _df.index = _df.index + 1
    if not type(t1) is str:
        t1.delete('1.0', END)
        t1.insert(END, tabulate(_df, headers='keys', tablefmt='psql'))


def print_match_metrics():
    global t1
    global hTeam_vs, aTeam_vs
    _df = league_stats.copy(deep=True)
    # League rank
    Hser = _df.Team
    hRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    aRank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    # Rank H/A
    _df['HPoints_game'] = _df.HPoints / _df.HGames
    Hser = _df.sort_values('HPoints_game', ascending=False).Team.reset_index(drop=True)
    hHRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    _df['APoints_game'] = _df.APoints / _df.AGames
    Aser = _df.sort_values('APoints_game', ascending=False).Team.reset_index(drop=True)
    aARank = Aser[Aser == aTeam_vs.get()].index[0] + 1
    # Rank Goals S/C
    _df['Scored'] = (_df.HScored1H + _df.HScored2H) * _df.HGames + (_df.AScored1H + _df.AScored2H) * _df.AGames
    Hser = _df.sort_values('Scored', ascending=False).Team.reset_index(drop=True)
    hGSRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    aGSRank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    _df['Conceded'] = (_df.HConceded1H + _df.HConceded2H) * _df.HGames + (
                _df.AConceded1H + _df.AConceded2H) * _df.AGames
    Hser = _df.sort_values('Conceded', ascending=True).Team.reset_index(drop=True)
    hGCRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    aGCRank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    _df['HScored'] = _df.HScored1H + _df.HScored2H
    Hser = _df.sort_values('HScored', ascending=False).Team.reset_index(drop=True)
    hHGSRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    _df['HConceded'] = _df.HConceded1H + _df.HConceded2H
    Hser = _df.sort_values('HConceded', ascending=True).Team.reset_index(drop=True)
    hHGCRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    _df['AScored'] = _df.AScored1H + _df.AScored2H
    Aser = _df.sort_values('AScored', ascending=False).Team.reset_index(drop=True)
    aAGSRank = Aser[Aser == aTeam_vs.get()].index[0] + 1
    _df['AConceded'] = _df.AConceded1H + _df.AConceded2H
    Aser = _df.sort_values('AConceded', ascending=True).Team.reset_index(drop=True)
    aAGCRank = Aser[Aser == aTeam_vs.get()].index[0] + 1
    # Rank 1H/2H
    _df['1Half'] = (_df.HScored1H - _df.HConceded1H) * _df.HGames + (_df.AScored1H - _df.AConceded1H) * _df.AGames
    Hser = _df.sort_values('1Half', ascending=False).Team.reset_index(drop=True)
    h1HRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    a1HRank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    _df['2Half'] = (_df.HScored2H - _df.HConceded2H) * _df.HGames + (_df.AScored2H - _df.AConceded2H) * _df.AGames
    Hser = _df.sort_values('2Half', ascending=False).Team.reset_index(drop=True)
    h2HRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    a2HRank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    _df['H1Half'] = _df.HScored1H - _df.HConceded1H
    Hser = _df.sort_values('H1Half', ascending=False).Team.reset_index(drop=True)
    h1HRankH = Hser[Hser == hTeam_vs.get()].index[0] + 1
    _df['H2Half'] = _df.HScored2H - _df.HConceded2H
    Hser = _df.sort_values('H2Half', ascending=False).Team.reset_index(drop=True)
    h2HRankH = Hser[Hser == hTeam_vs.get()].index[0] + 1
    _df['A1Half'] = _df.AScored1H - _df.AConceded1H
    Aser = _df.sort_values('A1Half', ascending=False).Team.reset_index(drop=True)
    a1HRankA = Aser[Aser == aTeam_vs.get()].index[0] + 1
    _df['A2Half'] = _df.AScored2H - _df.AConceded2H
    Aser = _df.sort_values('A2Half', ascending=False).Team.reset_index(drop=True)
    a2HRankA = Aser[Aser == aTeam_vs.get()].index[0] + 1
    # Rank Shots H/A
    _df['Shots'] = _df.HShotsFavor * _df.HGames + _df.AShotsFavor * _df.AGames
    Hser = _df.sort_values('Shots', ascending=False).Team.reset_index(drop=True)
    hSRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    aSRank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    Hser = _df.sort_values('HShotsFavor', ascending=False).Team.reset_index(drop=True)
    hHSRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    Aser = _df.sort_values('AShotsFavor', ascending=False).Team.reset_index(drop=True)
    aASRank = Aser[Aser == aTeam_vs.get()].index[0] + 1
    # Efficiency Ofensive Defensive
    _df['OEff'] = (((_df.HScored1H + _df.HScored2H) / (_df.HShotsFavor + _df.HCornersFavor)) * _df.HGames + \
                   ((_df.AScored1H + _df.AScored2H) / (_df.AShotsFavor + _df.ACornersFavor)) * _df.AGames) / (
                              _df.HGames + _df.AGames)
    Hser = _df.sort_values('OEff', ascending=False).Team.reset_index(drop=True)
    hORank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    aORank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    #
    _df['DEff'] = (((_df.HConceded1H + _df.HConceded2H) / (_df.HShotsAgainst + _df.HCornersAgainst)) * _df.HGames + \
                   ((_df.AConceded1H + _df.AConceded2H) / (_df.AShotsAgainst + _df.ACornersAgainst)) * _df.AGames) / (
                              _df.HGames + _df.AGames)
    Hser = _df.sort_values('DEff', ascending=True).Team.reset_index(drop=True)
    hDRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    aDRank = Hser[Hser == aTeam_vs.get()].index[0] + 1
    #
    _df['HOEff'] = (_df.HScored1H + _df.HScored2H) / _df.HShotsFavor
    _df['HDEff'] = (_df.HConceded1H + _df.HConceded2H) / _df.HShotsAgainst
    Hser = _df.sort_values('HOEff', ascending=False).Team.reset_index(drop=True)
    hHORank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    Hser = _df.sort_values('HDEff', ascending=True).Team.reset_index(drop=True)
    hHDRank = Hser[Hser == hTeam_vs.get()].index[0] + 1
    _df['AOEff'] = (_df.AScored1H + _df.AScored2H) / _df.AShotsFavor
    _df['ADEff'] = (_df.AConceded1H + _df.AConceded2H) / _df.AShotsAgainst
    Aser = _df.sort_values('AOEff', ascending=False).Team.reset_index(drop=True)
    aAORank = Aser[Aser == aTeam_vs.get()].index[0] + 1
    Aser = _df.sort_values('ADEff', ascending=True).Team.reset_index(drop=True)
    aADRank = Aser[Aser == aTeam_vs.get()].index[0] + 1

    if not type(t1) is str:
        t1.delete('1.0', END)
        t1.insert(END, hTeam_vs.get() + ':\n')
        t1.insert(END, '#' + str(hRank).ljust(2, ' ') + ' place\t\t\t #' + str(hHRank).ljust(2, ' ') + ' home\n')
        t1.insert(END, '#' + str(h1HRank).ljust(2, ' ') + ' 1H\t\t\t #' + str(h1HRankH).ljust(2, ' ') + ' home\n')
        t1.insert(END, '#' + str(h2HRank).ljust(2, ' ') + ' 2H\t\t\t #' + str(h2HRankH).ljust(2, ' ') + ' home\n')
        t1.insert(END,
                  '#' + str(hGSRank).ljust(2, ' ') + ' goals scored\t\t\t #' + str(hHGSRank).ljust(2, ' ') + ' home\n')
        t1.insert(END, '#' + str(hSRank).ljust(2, ' ') + ' shots\t\t\t #' + str(hHSRank).ljust(2, ' ') + ' home\n')
        t1.insert(END,
                  '#' + str(hORank).ljust(2, ' ') + ' ofensive efficiency\t #' + str(hHORank).ljust(2, ' ') + ' home\n')
        t1.insert(END, '#' + str(hGCRank).ljust(2, ' ') + ' goals conceded\t\t\t #' + str(hHGCRank).ljust(2,
                                                                                                          ' ') + ' home\n')
        t1.insert(END,
                  '#' + str(hDRank).ljust(2, ' ') + ' defensive efficiency\t#' + str(hHDRank).ljust(2, ' ') + ' home\n')
        #
        t1.insert(END, '\n')
        t1.insert(END, aTeam_vs.get() + ':\n')
        t1.insert(END, '#' + str(aRank).ljust(2, ' ') + ' place\t\t\t #' + str(aARank).ljust(2, ' ') + ' away\n')
        t1.insert(END, '#' + str(a1HRank).ljust(2, ' ') + ' 1H\t\t\t #' + str(a1HRankA).ljust(2, ' ') + ' away\n')
        t1.insert(END, '#' + str(a2HRank).ljust(2, ' ') + ' 2H\t\t\t #' + str(a2HRankA).ljust(2, ' ') + ' away\n')
        t1.insert(END,
                  '#' + str(aGSRank).ljust(2, ' ') + ' goals scored\t\t\t #' + str(aAGSRank).ljust(2, ' ') + ' away\n')
        t1.insert(END, '#' + str(aSRank).ljust(2, ' ') + ' shots\t\t\t #' + str(aASRank).ljust(2, ' ') + ' away\n')
        t1.insert(END,
                  '#' + str(aORank).ljust(2, ' ') + ' ofensive efficiency\t #' + str(aAORank).ljust(2, ' ') + ' away\n')
        t1.insert(END, '#' + str(aGCRank).ljust(2, ' ') + ' goals conceded\t\t\t #' + str(aAGCRank).ljust(2,
                                                                                                          ' ') + ' away\n')
        t1.insert(END,
                  '#' + str(aDRank).ljust(2, ' ') + ' defensive efficiency\t#' + str(aADRank).ljust(2, ' ') + ' away\n')


def calculateStatsTeam(teamHGames, teamAGames):
    teamName = teamHGames.iloc[0].HomeTeam

    # HOME
    hGames = len(teamHGames)
    # Points FT
    _df_points = teamHGames.groupby('FTR').size()
    hPoints = 0
    for item in _df_points.index:
        if item is 'H':
            hPoints += 3 * _df_points['H']
        elif item is 'D':
            hPoints += _df_points['D']
    # Points HT
    _df_points = teamHGames.groupby('HTR').size()
    hPoints1 = 0
    for item in _df_points.index:
        if item is 'H':
            hPoints1 += 3 * _df_points['H']
        elif item is 'D':
            hPoints1 += _df_points['D']
    # Points 2nd half
    wins = len(teamHGames[(teamHGames['FTHG'] - teamHGames['HTHG']) > (teamHGames['FTAG'] - teamHGames['HTAG'])])
    draws = len(teamHGames[(teamHGames['FTHG'] - teamHGames['HTHG']) == (teamHGames['FTAG'] - teamHGames['HTAG'])])
    hPoints2 = 3 * wins + draws
    # Goals
    hScored1 = teamHGames.HTHG.mean()
    hScored2 = teamHGames['FTHG'].sub(teamHGames['HTHG'], axis=0).mean()
    hConceded1 = teamHGames.HTAG.mean()
    hConceded2 = teamHGames['FTAG'].sub(teamHGames['HTAG'], axis=0).mean()
    # Shots
    hShotsFavor = teamHGames.HS.mean()
    hShotsAgainst = teamHGames.AS.mean()
    hShotsTFavor = teamHGames.HST.mean()
    hShotsTAgainst = teamHGames.AST.mean()
    # Fouls
    hFoulsCommited = teamHGames.HF.mean()
    hFoulsSuffered = teamHGames.AF.mean()
    hCornersFavor = teamHGames.HC.mean()
    hCornersAgainst = teamHGames.AC.mean()
    hYellowFavor = teamHGames.HY.mean()
    hYellowAgainst = teamHGames.AY.mean()
    hRedFavor = teamHGames.HR.mean()
    hRedAgainst = teamHGames.AR.mean()

    # AWAY
    aGames = len(teamAGames)

    # Points FT
    _df_points = teamAGames.groupby('FTR').size()
    aPoints = 0
    for item in _df_points.index:
        if item is 'A':
            aPoints += 3 * _df_points['A']
        elif item is 'D':
            aPoints += _df_points['D']
    # Points HT
    _df_points = teamAGames.groupby('HTR').size()
    aPoints1 = 0
    for item in _df_points.index:
        if item is 'A':
            aPoints1 += 3 * _df_points['A']
        elif item is 'D':
            aPoints1 += _df_points['D']
    # Points 2nd half
    wins = len(teamAGames[(teamAGames['FTHG'] - teamAGames['HTHG']) < (teamAGames['FTAG'] - teamAGames['HTAG'])])
    draws = wins = len(
        teamAGames[(teamAGames['FTHG'] - teamAGames['HTHG']) == (teamAGames['FTAG'] - teamAGames['HTAG'])])
    aPoints2 = 3 * wins + draws
    # Goals
    aScored1 = teamAGames.HTAG.mean()
    aScored2 = teamAGames['FTAG'].sub(teamAGames['HTAG'], axis=0).mean()
    aConceded1 = teamAGames.HTHG.mean()
    aConceded2 = teamAGames['FTHG'].sub(teamAGames['HTHG'], axis=0).mean()
    # Shots
    aShotsFavor = teamAGames.AS.mean()
    aShotsAgainst = teamAGames.HS.mean()
    aShotsTFavor = teamAGames.AST.mean()
    aShotsTAgainst = teamAGames.HST.mean()
    # Fouls
    aFoulsCommited = teamAGames.AF.mean()
    aFoulsSuffered = teamAGames.HF.mean()
    aCornersFavor = teamAGames.AC.mean()
    aCornersAgainst = teamAGames.HC.mean()
    aYellowFavor = teamAGames.AY.mean()
    aYellowAgainst = teamAGames.HY.mean()
    aRedFavor = teamAGames.AR.mean()
    aRedAgainst = teamAGames.HR.mean()

    wins = len(teamHGames[(teamHGames['FTHG'] > teamHGames['FTAG'])]) + len(
        teamAGames[(teamAGames['FTAG'] > teamAGames['FTHG'])])
    draws = len(teamHGames[(teamHGames['FTHG'] == teamHGames['FTAG'])]) + len(
        teamAGames[(teamAGames['FTHG'] == teamAGames['FTAG'])])
    losses = len(teamHGames) + len(teamAGames) - wins - draws

    _df = pd.DataFrame(
        [teamName, hGames, hPoints, hPoints1, hPoints2, hScored1, hScored2, hConceded1, hConceded2, hShotsFavor,
         hShotsAgainst, hShotsTFavor, hShotsTAgainst,
         hFoulsCommited, hFoulsSuffered, hCornersFavor, hCornersAgainst, hYellowFavor, hYellowAgainst, hRedFavor,
         hRedAgainst,
         aGames, aPoints, aPoints1, aPoints2, aScored1, aScored2, aConceded1, aConceded2, aShotsFavor, aShotsAgainst,
         aShotsTFavor, aShotsTAgainst, aFoulsCommited, aFoulsSuffered,
         aCornersFavor, aCornersAgainst, aYellowFavor, aYellowAgainst, aRedFavor, aRedAgainst, wins, draws, losses])

    return _df.transpose()


## -------------------------- MAIN ------------------------------------------ 

getLeague()
calculateStats(league_games)

while True:
    initGUI()
