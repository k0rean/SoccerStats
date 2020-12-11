import sys
import urllib.request
import pandas as pd
import os
from tkinter import *

GUI = 1
root = ""
teams = []
active_league = ""

class Application:
	def __init__(self, master=None):

		self.widget1 = Frame(master,width=1000, height=1000)
		self.widget1.pack()
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)
		## Scored
		self.scored = Button(self.widget1)  
		self.scored["text"] = "Scored"
		self.scored["font"] = ("Calibri", "11")
		self.scored["width"] = 12
		self.scored.bind("<Button-1>", self.scored_func)
		self.scored.place(x=500, y=200)
		## Conceded
		self.conceded = Button(self.widget1)
		self.conceded["text"] = "Conceded"
		self.conceded["font"] = ("Calibri", "11")
		self.conceded["width"] = 12
		self.conceded.bind("<Button-1>", self.conceded_func)
		self.conceded.place(x=500, y=250)
		## Diffs
		self.diffs = Button(self.widget1)
		self.diffs["text"] = "Performance"
		self.diffs["font"] = ("Calibri", "11")
		self.diffs["width"] = 12
		self.diffs.bind("<Button-1>", self.diffs_func)
		self.diffs.place(x=500, y=300)
		## Corners
		self.corners = Button(self.widget1)
		self.corners["text"] = "Corners"
		self.corners["font"] = ("Calibri", "11")
		self.corners["width"] = 12
		self.corners.bind("<Button-1>", self.corners_func)
		self.corners.place(x=500, y=350)
		## Shots
		self.shots = Button(self.widget1)
		self.shots["text"] = "Shots"
		self.shots["font"] = ("Calibri", "11")
		self.shots["width"] = 12
		self.shots.bind("<Button-1>", self.shots_func)
		self.shots.place(x=500, y=400)
		## Shots_acc
		self.shots_acc = Button(self.widget1)
		self.shots_acc["text"] = "Shots accuracy"
		self.shots_acc["font"] = ("Calibri", "11")
		self.shots_acc["width"] = 12
		self.shots_acc.bind("<Button-1>", self.shots_acc_func)
		self.shots_acc.place(x=500, y=450)
		## Fouls
		self.fouls = Button(self.widget1)
		self.fouls["text"] = "Fouls"
		self.fouls["font"] = ("Calibri", "11")
		self.fouls["width"] = 12
		self.fouls.bind("<Button-1>", self.fouls_func)
		self.fouls.place(x=500, y=500)
		## Shots_acc
		self.cards = Button(self.widget1)
		self.cards["text"] = "Cards"
		self.cards["font"] = ("Calibri", "11")
		self.cards["width"] = 12
		self.cards.bind("<Button-1>", self.cards_func)
		self.cards.place(x=500, y=550)

		##LIGAS
		N = 45
		## liganos
		self.liganos = Button(self.widget1)  
		self.liganos["text"] = "Liga NOS"
		self.liganos["font"] = ("Calibri", "11")
		self.liganos["width"] = 14
		self.liganos.bind("<Button-1>", self.liganos_func)
		self.liganos.place(x=0, y=8*N)
		## premier_league
		self.premier_league = Button(self.widget1)
		self.premier_league["text"] = "Premier League" 
		self.premier_league["font"] = ("Calibri", "11")
		self.premier_league["width"] = 14
		self.premier_league.bind("<Button-1>", self.premier_league_func)
		self.premier_league.place(x=0, y=3*N)
		## championship
		self.championship = Button(self.widget1)
		self.championship["text"] = "Championship"
		self.championship["font"] = ("Calibri", "11")
		self.championship["width"] = 14
		self.championship.bind("<Button-1>", self.championship_func)
		self.championship.place(x=150, y=3*N)
		## La_Liga
		self.La_Liga = Button(self.widget1)
		self.La_Liga["text"] = "La Liga"
		self.La_Liga["font"] = ("Calibri", "11")
		self.La_Liga["width"] = 14
		self.La_Liga.bind("<Button-1>", self.La_Liga_func)
		self.La_Liga.place(x=0, y=4*N)
		## La_Liga2
		self.La_Liga2 = Button(self.widget1)
		self.La_Liga2["text"] = "La Liga 2"
		self.La_Liga2["font"] = ("Calibri", "11")
		self.La_Liga2["width"] = 14
		self.La_Liga2.bind("<Button-1>", self.La_Liga2_func)
		self.La_Liga2.place(x=150, y=4*N)
		## SerieA
		self.SerieA = Button(self.widget1)
		self.SerieA["text"] = "Serie A"
		self.SerieA["font"] = ("Calibri", "11")
		self.SerieA["width"] = 14
		self.SerieA.bind("<Button-1>", self.SerieA_func)
		self.SerieA.place(x=0, y=5*N)
		## SerieB
		self.SerieB = Button(self.widget1)
		self.SerieB["text"] = "Serie B"
		self.SerieB["font"] = ("Calibri", "11")
		self.SerieB["width"] = 14
		self.SerieB.bind("<Button-1>", self.SerieB_func)
		self.SerieB.place(x=150, y=5*N)
		## Bundesliga
		self.Bundesliga = Button(self.widget1)
		self.Bundesliga["text"] = "Bundesliga"
		self.Bundesliga["font"] = ("Calibri", "11")
		self.Bundesliga["width"] = 14
		self.Bundesliga.bind("<Button-1>", self.Bundesliga_func)
		self.Bundesliga.place(x=0, y=6*N)
		## Bundesliga2
		self.Bundesliga2 = Button(self.widget1)
		self.Bundesliga2["text"] = "Bundesliga 2"
		self.Bundesliga2["font"] = ("Calibri", "11")
		self.Bundesliga2["width"] = 14
		self.Bundesliga2.bind("<Button-1>", self.Bundesliga2_func)
		self.Bundesliga2.place(x=150, y=6*N)
		## Ligue 1
		self.ligue1 = Button(self.widget1)
		self.ligue1["text"] = "Ligue 1"
		self.ligue1["font"] = ("Calibri", "11")
		self.ligue1["width"] = 14
		self.ligue1.bind("<Button-1>", self.ligue1_func)
		self.ligue1.place(x=0, y=7*N)
		## Ligue 2
		self.ligue2 = Button(self.widget1)
		self.ligue2["text"] = "Ligue 2"
		self.ligue2["font"] = ("Calibri", "11")
		self.ligue2["width"] = 14
		self.ligue2.bind("<Button-1>", self.ligue2_func)
		self.ligue2.place(x=150, y=7*N)
		## Jupiler
		self.ligue1 = Button(self.widget1)
		self.ligue1["text"] = "Jupiler"
		self.ligue1["font"] = ("Calibri", "11")
		self.ligue1["width"] = 14
		self.ligue1.bind("<Button-1>", self.jupiler_func)
		self.ligue1.place(x=0, y=9*N)
		## Eredivisie
		self.ligue1 = Button(self.widget1)
		self.ligue1["text"] = "Eredivisie"
		self.ligue1["font"] = ("Calibri", "11")
		self.ligue1["width"] = 14
		self.ligue1.bind("<Button-1>", self.eredivisie_func)
		self.ligue1.place(x=0, y=10*N)
		## Greece
		self.ligue1 = Button(self.widget1)
		self.ligue1["text"] = "Greece"
		self.ligue1["font"] = ("Calibri", "11")
		self.ligue1["width"] = 14
		self.ligue1.bind("<Button-1>", self.greece_func)
		self.ligue1.place(x=0, y=11*N)
		## Turkey
		self.ligue1 = Button(self.widget1)
		self.ligue1["text"] = "Turkey"
		self.ligue1["font"] = ("Calibri", "11")
		self.ligue1["width"] = 14
		self.ligue1.bind("<Button-1>", self.turkey_func)
		self.ligue1.place(x=0, y=12*N)
		## EXIT
		self.ligue1 = Button(self.widget1)
		self.ligue1["text"] = "QUIT"
		self.ligue1["font"] = ("Calibri", "14")
		self.ligue1["width"] = 14
		self.ligue1.bind("<Button-1>", self.exit_func)
		self.ligue1.place(x=0, y=14*N)


  
	def scored_func(self, event):
		graph_averages(sort_by_points(teams),"goalsScored","all")

	def conceded_func(self, event):
		graph_averages(sort_by_points(teams),"goalsConceded","all")

	def diffs_func(self, event):
		graph_averages(sort_by_points(teams),"diffs","all")        

	def corners_func(self, event):
		graph_averages(sort_by_points(teams),"corners","all")

	def shots_func(self, event):
		graph_averages(sort_by_points(teams),"shots","all")

	def shots_acc_func(self, event):
		graph_averages(sort_by_points(teams),"shots_acc","all")
  
	def fouls_func(self, event):
		graph_averages(sort_by_points(teams),"fouls","all")

	def cards_func(self, event):
		graph_averages(sort_by_points(teams),"cards","all")

	##Ligas
	def liganos_func(self, event):
		global teams
		active_league = "Liga NOS"
		teams = getLeague("P1")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def premier_league_func(self, event):
		global teams
		active_league = "Premier League" + "\t\t\t"
		teams = getLeague("E0")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def championship_func(self, event):
		global teams
		active_league = "Championship"
		teams = getLeague("E1") 
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def premiership_func(self, event):
		global teams
		active_league = "Premiership"
		teams = getLeague("SC0") 
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)   

	def La_Liga_func(self, event):
		global teams
		active_league = "La Liga"
		teams = getLeague("SP1")
		calculate_rates(teams)
		print_teams(teams) 
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def La_Liga2_func(self, event):
		global teams
		active_league = "La Liga 2"
		teams = getLeague("SP2")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0) 

	def SerieA_func(self, event):
		global teams
		active_league = "Serie A"
		teams = getLeague("I1")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def SerieB_func(self, event):
		global teams
		active_league = "Serie B"
		teams = getLeague("I2")
		calculate_rates(teams)
		print_teams(teams) 
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)
  
	def Bundesliga_func(self, event):
		global teams
		active_league = "Bundesliga"
		teams = getLeague("D1")
		calculate_rates(teams)
		print_teams(teams) 
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def Bundesliga2_func(self, event):
		global teams
		active_league = "Bundesliga 2"
		teams = getLeague("D2")
		calculate_rates(teams)
		print_teams(teams) 
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def ligue1_func(self, event):
		global teams
		active_league = "Ligue 1"
		teams = getLeague("F1")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def ligue2_func(self, event):
		global teams
		active_league = "Ligue 2"
		teams = getLeague("F2")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def eredivisie_func(self, event):
		global teams
		active_league = "Eredivisie"
		teams = getLeague("N1")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def jupiler_func(self, event):
		global teams
		active_league = "Jupiler"
		teams = getLeague("B1")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def greece_func(self, event):
		global teams
		active_league = "Greece"
		teams = getLeague("G1")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def turkey_func(self, event):
		global teams
		active_league = "Turkey"
		teams = getLeague("T1")
		calculate_rates(teams)
		print_teams(teams)
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league) + "\t\t\t\t")
		self.msg["font"] = ("Calibri", "50","bold")
		self.msg.place(x=200,y=0)

	def exit_func(self, event):
		import sys
		sys.exit()

  
def initGUI():
	global root	
	root = Tk()
	root.attributes('-fullscreen', True)
	Application(root)
	root.mainloop()

def getLeague(filename = 'P1'):
	teams = []
	teams_index = 0
	filename = filename + ".csv"
	url = 'http://www.football-data.co.uk/mmz4281/2021/' + filename
	urllib.request.urlretrieve(url,filename)

	df = pd.read_csv(filename)

	os.remove(filename)
	return df


def calculateStats(games):
	teams = list(set([*games['HomeTeam'], *games['AwayTeam']]))
	_df_homeGames = games.groupby('HomeTeam')
	_df_awayGames = games.groupby('AwayTeam')
	res = []
	for team in teams:
		res.append(calculateStatsTeam(_df_homeGames.get_group(team), _df_awayGames.get_group(team)))

	# convert to df
	df = pd.concat(res).reset_index(drop=True)
	df.columns = ['Team', 'HGames', 'HPoints', 'HPoints1H', 'HPoints2H', 'HScored1H', 'HScored2H', 'HConceded1H', 'HConceded2H', 'HShots', 'HShotsT', 'HFoulsCommited', 'HFoulsSuffered', \
		'HCornersFavor', 'HCornersAgainst', 'HYellowFavor', 'HYellowAgainst', 'HRedFavor', 'HRedAgainst', 'AGames', 'APoints', 'APoints1H', 'APoints2H', 'AScored1H', 'AScored2H', \
		'AConceded1H', 'AConceded2H', 'AShots', 'AShotsT', 'AFoulsCommited', 'AFoulsSuffered', 'ACornersFavor', 'ACornersAgainst', 'AYellowFavor', 'AYellowAgainst', \
		'ARedFavor', 'ARedAgainst']
	df = df.iloc[(df.HPoints + df.APoints).sort_values(ascending=False).index].reset_index(drop=True)

	return df


def calculateStatsTeam(teamHGames, teamAGames):
	
	teamName = teamHGames.iloc[0].HomeTeam

	# HOME
	hGames = len(teamHGames)
	# Points FT
	_df_points = teamHGames.groupby('FTR').size()
	hPoints = 0
	for item in _df_points.index:
		if item is 'H':
			hPoints += 3*_df_points['H']
		elif item is 'D':
			hPoints += _df_points['D']
	# Points HT
	_df_points = teamHGames.groupby('HTR').size()
	hPoints1 = 0
	for item in _df_points.index:
		if item is 'H':
			hPoints1 += 3*_df_points['H']
		elif item is 'D':
			hPoints1 += _df_points['D']
	# Points 2nd half
	wins = len(teamHGames[(teamHGames['FTHG'] - teamHGames['HTHG']) > (teamHGames['FTAG'] - teamHGames['HTAG'])])
	draws = wins = len(teamHGames[(teamHGames['FTHG'] - teamHGames['HTHG']) == (teamHGames['FTAG'] - teamHGames['HTAG'])])
	hPoints2 = 3*wins + draws
	# Goals
	hScored1 = teamHGames.HTHG.mean()
	hScored2 = teamHGames.FTHG.mean() - teamHGames.HTHG.mean()
	hConceded1 = teamHGames.HTAG.mean()
	hConceded2 = teamHGames.FTAG.mean() - teamHGames.HTAG.mean()
	# Shots
	hShots = teamHGames.HS.mean()
	hShotsT = teamHGames.HST.mean()
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
			aPoints += 3*_df_points['A']
		elif item is 'D':
			aPoints += _df_points['D']
	# Points HT
	_df_points = teamAGames.groupby('HTR').size()
	aPoints1 = 0
	for item in _df_points.index:
		if item is 'A':
			aPoints1 += 3*_df_points['A']
		elif item is 'D':
			aPoints1 += _df_points['D']
	# Points 2nd half
	wins = len(teamAGames[(teamAGames['FTHG'] - teamAGames['HTHG']) < (teamAGames['FTAG'] - teamAGames['HTAG'])])
	draws = wins = len(teamAGames[(teamAGames['FTHG'] - teamAGames['HTHG']) == (teamAGames['FTAG'] - teamAGames['HTAG'])])
	aPoints2 = 3*wins + draws
	# Goals
	aScored1 = teamAGames.HTAG.mean()
	aScored2 = teamAGames.FTAG.mean() - teamHGames.HTAG.mean()
	aConceded1 = teamAGames.HTHG.mean()
	aConceded2 = teamAGames.FTHG.mean() - teamHGames.HTHG.mean()
	# Shots
	aShots = teamAGames.AS.mean()
	aShotsT = teamAGames.AST.mean()
	# Fouls
	aFoulsCommited = teamAGames.AF.mean()
	aFoulsSuffered = teamAGames.HF.mean()
	aCornersFavor = teamAGames.AC.mean()
	aCornersAgainst = teamAGames.HC.mean()
	aYellowFavor = teamAGames.AY.mean()
	aYellowAgainst = teamAGames.HY.mean()
	aRedFavor = teamAGames.AR.mean()
	aRedAgainst = teamAGames.HR.mean()

	_df = pd.DataFrame([teamName, hGames, hPoints, hPoints1, hPoints2, hScored1, hScored2, hConceded1, hConceded2, hShots, hShotsT, hFoulsCommited, hFoulsSuffered, \
		hCornersFavor, hCornersAgainst, hYellowFavor, hYellowAgainst, hRedFavor, hRedAgainst, \
		aGames, aPoints, aPoints1, aPoints2, aScored1, aScored2, hConceded1, aConceded2, aShots, aShotsT, aFoulsCommited, aFoulsSuffered, \
		aCornersFavor, aCornersAgainst, aYellowFavor, aYellowAgainst, aRedFavor, aRedAgainst])

	return _df.transpose()


## -------------------------- MAIN ------------------------------------------ 

league_games = getLeague('E0')
league_stats = calculateStats(league_games)
print(league_stats)

while(True):
	initGUI()
