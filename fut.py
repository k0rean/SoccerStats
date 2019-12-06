import csv
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import sys
import urllib.request
from Game import game
from Team import team
from graphs import *
import predicts
import os
from tkinter import *

GUI = 1
teams = []
active_league = ""

class Application:
	def __init__(self, master=None):

		self.widget1 = Frame(master,width=1000, height=1000)
		self.widget1.pack()
		## Title
		self.msg = Label(self.widget1, text="SoccerStats:" + str(active_league))
		self.msg["font"] = ("Calibri", "30", "italic")
		self.msg.place(x=350,y=0)
		## Scored
		self.scored = Button(self.widget1)  
		self.scored["text"] = "Scored"
		self.scored["font"] = ("Calibri", "9")
		self.scored["width"] = 10
		self.scored.bind("<Button-1>", self.scored_func)
		self.scored.place(x=200, y=200)
		## Conceded
		self.conceded = Button(self.widget1)
		self.conceded["text"] = "Conceded"
		self.conceded["font"] = ("Calibri", "9")
		self.conceded["width"] = 10
		self.conceded.bind("<Button-1>", self.conceded_func)
		self.conceded.place(x=200, y=250)
		## Diffs
		self.diffs = Button(self.widget1)
		self.diffs["text"] = "Diffs"
		self.diffs["font"] = ("Calibri", "9")
		self.diffs["width"] = 10
		self.diffs.bind("<Button-1>", self.diffs_func)
		self.diffs.place(x=200, y=300)
		## Corners
		self.corners = Button(self.widget1)
		self.corners["text"] = "Corners"
		self.corners["font"] = ("Calibri", "9")
		self.corners["width"] = 10
		self.corners.bind("<Button-1>", self.corners_func)
		self.corners.place(x=200, y=350)
		## Shots
		self.shots = Button(self.widget1)
		self.shots["text"] = "Shots"
		self.shots["font"] = ("Calibri", "9")
		self.shots["width"] = 10
		self.shots.bind("<Button-1>", self.shots_func)
		self.shots.place(x=200, y=400)
		## Shots_acc
		self.shots_acc = Button(self.widget1)
		self.shots_acc["text"] = "Shots acc"
		self.shots_acc["font"] = ("Calibri", "9")
		self.shots_acc["width"] = 10
		self.shots_acc.bind("<Button-1>", self.shots_acc_func)
		self.shots_acc.place(x=200, y=450)
		## Fouls
		self.fouls = Button(self.widget1)
		self.fouls["text"] = "Fouls"
		self.fouls["font"] = ("Calibri", "9")
		self.fouls["width"] = 10
		self.fouls.bind("<Button-1>", self.fouls_func)
		self.fouls.place(x=200, y=500)
		## Shots_acc
		self.cards = Button(self.widget1)
		self.cards["text"] = "Cards"
		self.cards["font"] = ("Calibri", "9")
		self.cards["width"] = 10
		self.cards.bind("<Button-1>", self.cards_func)
		self.cards.place(x=200, y=550)

		##LIGAS
		## liganos
		self.liganos = Button(self.widget1)  
		self.liganos["text"] = "Liga Nos"
		self.liganos["font"] = ("Calibri", "9")
		self.liganos["width"] = 10
		self.liganos.bind("<Button-1>", self.liganos_func)
		self.liganos.place(x=0, y=200)
		## premier_league
		self.premier_league = Button(self.widget1)
		self.premier_league["text"] = "Premier League"
		self.premier_league["font"] = ("Calibri", "9")
		self.premier_league["width"] = 10
		self.premier_league.bind("<Button-1>", self.premier_league_func)
		self.premier_league.place(x=0, y=250)
		## championship
		self.championship = Button(self.widget1)
		self.championship["text"] = "Championship"
		self.championship["font"] = ("Calibri", "9")
		self.championship["width"] = 10
		self.championship.bind("<Button-1>", self.championship_func)
		self.championship.place(x=0, y=300)
		## La_Liga
		self.La_Liga = Button(self.widget1)
		self.La_Liga["text"] = "La Liga"
		self.La_Liga["font"] = ("Calibri", "9")
		self.La_Liga["width"] = 10
		self.La_Liga.bind("<Button-1>", self.La_Liga_func)
		self.La_Liga.place(x=0, y=350)
		## La_Liga2
		self.La_Liga2 = Button(self.widget1)
		self.La_Liga2["text"] = "La Liga 2"
		self.La_Liga2["font"] = ("Calibri", "9")
		self.La_Liga2["width"] = 10
		self.La_Liga2.bind("<Button-1>", self.La_Liga2_func)
		self.La_Liga2.place(x=0, y=400)
		## SerieA
		self.SerieA = Button(self.widget1)
		self.SerieA["text"] = "Serie A"
		self.SerieA["font"] = ("Calibri", "9")
		self.SerieA["width"] = 10
		self.SerieA.bind("<Button-1>", self.SerieA_func)
		self.SerieA.place(x=0, y=450)
		## Bundesliga
		self.Bundesliga = Button(self.widget1)
		self.Bundesliga["text"] = "Bundesliga"
		self.Bundesliga["font"] = ("Calibri", "9")
		self.Bundesliga["width"] = 10
		self.Bundesliga.bind("<Button-1>", self.Bundesliga_func)
		self.Bundesliga.place(x=0, y=500)
		## Bundesliga2
		self.Bundesliga2 = Button(self.widget1)
		self.Bundesliga2["text"] = "Bundesliga2"
		self.Bundesliga2["font"] = ("Calibri", "9")
		self.Bundesliga2["width"] = 10
		self.Bundesliga2.bind("<Button-1>", self.Bundesliga2_func)
		self.Bundesliga2.place(x=0, y=550)
		## Ligue 1
		self.ligue1 = Button(self.widget1)
		self.ligue1["text"] = "Ligue 1"
		self.ligue1["font"] = ("Calibri", "9")
		self.ligue1["width"] = 10
		self.ligue1.bind("<Button-1>", self.ligue1_func)
		self.ligue1.place(x=0, y=600)

  
	def scored_func(self, event):
		graph_averages(sort_by_points(teams),"goalsScored","home")

	def conceded_func(self, event):
		graph_averages(sort_by_points(teams),"goalsConceded","home")

	def diffs_func(self, event):
		graph_averages(sort_by_points(teams),"diffs","home")        

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
		active_league = "Liga Nos"
		teams = getLeague("P1")
		calculate_rates(teams)
		print_teams(teams)

	def premier_league_func(self, event):
		global teams
		active_league = "Premier League"
		teams = getLeague("E0")
		calculate_rates(teams)
		print_teams(teams)

	def championship_func(self, event):
		global teams
		active_league = "Championship"
		teams = getLeague("E1") 
		calculate_rates(teams)
		print_teams(teams)      

	def La_Liga_func(self, event):
		global teams
		active_league = "La Liga"
		teams = getLeague("SP1")
		calculate_rates(teams)
		print_teams(teams) 

	def La_Liga2_func(self, event):
		global teams
		active_league = "La Liga 2"
		teams = getLeague("SP2")
		calculate_rates(teams)
		print_teams(teams) 

	def SerieA_func(self, event):
		global teams
		active_league = "Serie A"
		teams = getLeague("I1")
		calculate_rates(teams)
		print_teams(teams) 
  
	def Bundesliga_func(self, event):
		global teams
		active_league = "Bundesliga"
		teams = getLeague("D1")
		calculate_rates(teams)
		print_teams(teams) 

	def Bundesliga2_func(self, event):
		global teams
		active_league = "Bundesliga 2"
		teams = getLeague("D2")
		calculate_rates(teams)
		print_teams(teams) 

	def ligue1_func(self, event):
		global teams
		active_league = "Ligue 1"
		teams = getLeague("F1")
		calculate_rates(teams)
		print_teams(teams) 
  
def initGUI():
	root = Tk()
	root.attributes('-fullscreen', True)
	Application(root)
	root.mainloop()

def teams_contains(teams,name):
	value = 0
	aux = 1
	for team in teams:
		if team.name == name :
			value = 1
		if value == 0:
			aux += 1

	if value == 0:
		aux = 0

	return aux

def sort_by_points(teams):
	points = []
	for team in teams:
		points.append(team.points)
	
	points, teams = (list(t) for t in zip(*sorted(zip(points, teams),key=lambda x: x[0],reverse=True)))
	return teams

def print_teams_names(teams):
	for team in teams:
		print(team.name)

def print_teams(teams):
	teams = sort_by_points(teams)	
	print("Teams sorted by points")
	table = PrettyTable(['Index','Team','Points','HomeDiff 1st','HomeDiff 2nd','AwayDiff 1st','AwayDiff 2nd','HomeScored','HomeConceded','AwayScored','AwayConceded'])
	for team in teams:
		table.add_row([team.index, team.name, team.points,"%.2f" % team.hRate_first,"%.2f" % team.hRate_second,"%.2f" % team.aRate_first,"%.2f" % team.aRate_second,
			"%.2f" % (team.hScored_first+team.hScored_second),"%.2f" % (team.hConceded_first+team.hConceded_second),
			"%.2f" % (team.aScored_first+team.aScored_second),"%.2f" % (team.aConceded_first+team.aConceded_second),])
	print(table)

def calculate_rates(teams):
	for team in teams:
		team.getRatesDiffs()
		team.getGoalsData()
		team.getCornersData()
		team.getShotsData()
		team.getFoulsData()
		team.getCardsData()

def getLeague(filename = sys.argv[1]):
	teams = []
	teams_index = 0
	filename = filename + ".csv"
	url = 'http://www.football-data.co.uk/mmz4281/1920/' + filename
	urllib.request.urlretrieve(url,filename)

	with open(filename,'r') as file:
		csv_reader = csv.reader(file,delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count != 0:
				hteamName = row[3]
				ateamName = row[4]
				
				hIndex = teams_contains(teams,hteamName) - 1
				if hIndex == -1:
					teams.append(team(hteamName,teams_index))
					hIndex = teams_index
					teams_index += 1

				aIndex = teams_contains(teams,ateamName) - 1
				if aIndex == -1:
					teams.append(team(ateamName,teams_index))
					aIndex = teams_index
					teams_index += 1


				g = game(hIndex,aIndex,row,filename)
				teams[hIndex].addGame(g)
				teams[hIndex].pointsCalc_home(g)
				teams[aIndex].addGame(g)
				teams[aIndex].pointsCalc_away(g)

			line_count += 1
	os.remove(filename)
	return teams

def print_team_info(home,side):
	Hgames = 0
	Agames = 0
	
	for game in reversed(home.gamesList): # for every game in record	
			if(home.index == game.hIndex): # discover if team played home or away
				Hgames+=1
			else:
				Agames+=1

	table = PrettyTable([home.name,'goalsScored', 'goalsConceded','Corners','Shots','Goal/Shots'])
	table.add_row(['Total','{0:.2f}'.format((home.hScored_first*Hgames+home.aScored_first*Agames+home.hScored_second*Hgames+home.aScored_second*Agames)/len(home.gamesList)),
		'{0:.2f}'.format((home.hConceded_first*Hgames+home.aConceded_first*Agames+home.hConceded_second*Hgames+home.aConceded_second*Agames)/len(home.gamesList)),
		'{0:.2f}'.format((home.hCorners*Hgames+home.aCorners*Agames)/len(home.gamesList)),
		'{0:.2f}'.format((home.hShots*Hgames+home.aShots*Agames)/len(home.gamesList)),
		'{0:.2f}'.format((home.hScored_first+home.aScored_first+home.hScored_second+home.aScored_second)/(home.hShots+home.aShots)),
		])
	table.add_row(['1st Half','{0:.2f}'.format((home.hScored_first*Hgames+home.aScored_first*Agames)/len(home.gamesList)),
		'{0:.2f}'.format((home.hConceded_first*Hgames+home.aConceded_first*Agames)/len(home.gamesList)),
		'',
		'',
		'',])
	table.add_row(['2nd Half','{0:.2f}'.format((home.hScored_second*Hgames+home.aScored_second*Agames)/len(home.gamesList)),
		'{0:.2f}'.format((home.hConceded_second*Hgames+home.aConceded_second*Agames)/len(home.gamesList)),
		'',
		'',
		'',])
	print(table)
	if side == "home":
		table = PrettyTable([home.name+' home','goalsScored', 'goalsConceded','Goal/Shots'])
		table.add_row(['Total','{0:.2f}'.format((home.hScored_first+home.hScored_second)),
			'{0:.2f}'.format((home.hConceded_first+home.hConceded_second)),
			'{0:.2f}'.format((home.hScored_first+home.hScored_second)/(home.hShots))
			])
		table.add_row(['1st Half','{0:.2f}'.format((home.hScored_first)),
			'{0:.2f}'.format((home.hConceded_first)),'',])
		table.add_row(['2nd Half','{0:.2f}'.format((home.hScored_second)),
			'{0:.2f}'.format((home.hConceded_second)),'',])
		print(table)
	else:
		table = PrettyTable([home.name+' away','goalsScored', 'goalsConceded','Goal/Shots'])
		table.add_row(['Total','{0:.2f}'.format((home.aScored_first+home.aScored_second)),
			'{0:.2f}'.format((home.aConceded_first+home.aConceded_second)),
			'{0:.2f}'.format((home.aScored_first+home.aScored_second)/(home.aShots))])
		table.add_row(['1st Half','{0:.2f}'.format((home.aScored_first)),
			'{0:.2f}'.format((home.aConceded_first)),'',])
		table.add_row(['2nd Half','{0:.2f}'.format((home.aScored_second)),
			'{0:.2f}'.format((home.aConceded_second)),'',])
		print(table)

def print_game_info(home,away):
	print_team_info(home,"home")
	print_team_info(away,"away")


## -------------------------- MAIN ------------------------------------------ 
if sys.argv[1] == "-h":
	print("Argument league expected\n")
	print("E0 - Premier League")
	print("E1 - Championship")
	print("I1 - Serie A")
	print("SP1 - La Liga")
	print("SP2 - La Liga 2")
	print("P1 - Liga Nos")
	print("D1 - Bundesliga")
else:
	
	teams = getLeague()
	calculate_rates(teams)
	print_teams(teams)

	while(True):
		if GUI == 1:
			initGUI()
		else:
			txt = input("0-Goals Scored\n1-Goals Conceded\n2-Diffs\n3-Corners\n4-Shots\n5-Fouls\n6-Cards\n7-Shots accuracy\n8-Predict_scored\n9-Predict_conceded\na-Game analysis\n")
			if txt is "0":
				graph_averages(sort_by_points(teams),"goalsScored","home")
				graph_averages(sort_by_points(teams),"goalsScored","away")
				graph_averages(sort_by_points(teams),"goalsScored","all")
			elif txt is "1":
				graph_averages(sort_by_points(teams),"goalsConceded","home")
				graph_averages(sort_by_points(teams),"goalsConceded","away")
				graph_averages(sort_by_points(teams),"goalsConceded","all")
			elif txt is "2":
				graph_averages(sort_by_points(teams),"diffs","home")
				graph_averages(sort_by_points(teams),"diffs","away")
				graph_averages(sort_by_points(teams),"diffs","all")
			elif txt is "3":
				graph_averages(sort_by_points(teams),"corners","all")
			elif txt is "4":
				graph_averages(sort_by_points(teams),"shots","all")
			elif txt is "5":
				graph_averages(sort_by_points(teams),"fouls","all")
			elif txt is "6":
				graph_averages(sort_by_points(teams),"cards","all")
			elif txt is "7":
				graph_averages(sort_by_points(teams),"shots_acc","all")
			elif txt is "8":
				h = input("HomeIndex ")
				a = input("AwayIndex ")
				predicts.predict_outcome(teams[int(h)],teams[int(a)],"scored")
			elif txt is "9":
				h = input("HomeIndex ")
				a = input("AwayIndex ")
				predicts.predict_outcome(teams[int(h)],teams[int(a)],"conceded")
			elif txt is "a":
				h = input("HomeIndex ")
				a = input("AwayIndex ")
				print_game_info(teams[int(h)],teams[int(a)])
			else:
				print_teams(teams)
