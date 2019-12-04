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

GUI = 0
teams = []

class Application:
	def __init__(self, master=None):

		self.widget1 = Frame(master)
		self.widget1.pack()
		self.msg = Label(self.widget1, text="SoccerStats")
		self.msg["font"] = ("Calibri", "20", "italic")
		self.msg.pack()
		## Scored
		self.scored = Button(self.widget1)  
		self.scored["text"] = "Scored"
		self.scored["font"] = ("Calibri", "9")
		self.scored["width"] = 10
		self.scored.bind("<Button-1>", self.scored_func)
		self.scored.pack()
		## Conceded
		self.conceded = Button(self.widget1)
		self.conceded["text"] = "Conceded"
		self.conceded["font"] = ("Calibri", "9")
		self.conceded["width"] = 10
		self.conceded.bind("<Button-1>", self.conceded_func)
		self.conceded.pack()
		## Diffs
		self.diffs = Button(self.widget1)
		self.diffs["text"] = "Diffs"
		self.diffs["font"] = ("Calibri", "9")
		self.diffs["width"] = 10
		self.diffs.bind("<Button-1>", self.diffs_func)
		self.diffs.pack()
		## Corners
		self.corners = Button(self.widget1)
		self.corners["text"] = "Corners"
		self.corners["font"] = ("Calibri", "9")
		self.corners["width"] = 10
		self.corners.bind("<Button-1>", self.corners_func)
		self.corners.pack()
		## Shots
		self.shots = Button(self.widget1)
		self.shots["text"] = "Shots"
		self.shots["font"] = ("Calibri", "9")
		self.shots["width"] = 10
		self.shots.bind("<Button-1>", self.shots_func)
		self.shots.pack()
		## Shots_acc
		self.shots_acc = Button(self.widget1)
		self.shots_acc["text"] = "Shots acc"
		self.shots_acc["font"] = ("Calibri", "9")
		self.shots_acc["width"] = 10
		self.shots_acc.bind("<Button-1>", self.shots_acc_func)
		self.shots_acc.pack()
		## Fouls
		self.fouls = Button(self.widget1)
		self.fouls["text"] = "Fouls"
		self.fouls["font"] = ("Calibri", "9")
		self.fouls["width"] = 10
		self.fouls.bind("<Button-1>", self.fouls_func)
		self.fouls.pack()
		## Shots_acc
		self.cards = Button(self.widget1)
		self.cards["text"] = "Cards"
		self.cards["font"] = ("Calibri", "9")
		self.cards["width"] = 10
		self.cards.bind("<Button-1>", self.cards_func)
		self.cards.pack()
  
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

def getLeague():
	teams = []
	teams_index = 0
	filename = sys.argv[1] + ".csv"
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


				g = game(hIndex,aIndex,row)
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
if len(sys.argv) < 2:
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
			txt = input("1-Goals Scored\n2-Goals Conceded\n3-Diffs\n4-Corners\n5-Shots\n6-Fouls\n7-Cards\n8-Shots accuracy\n9-Predict_scored\n10-Predict_conceded\na-Game analysis\n")
			if txt is "1":
				graph_averages(sort_by_points(teams),"goalsScored","home")
				graph_averages(sort_by_points(teams),"goalsScored","away")
				graph_averages(sort_by_points(teams),"goalsScored","all")
			elif txt is "2":
				graph_averages(sort_by_points(teams),"goalsConceded","home")
				graph_averages(sort_by_points(teams),"goalsConceded","away")
				graph_averages(sort_by_points(teams),"goalsConceded","all")
			elif txt is "3":
				graph_averages(sort_by_points(teams),"diffs","home")
				graph_averages(sort_by_points(teams),"diffs","away")
				graph_averages(sort_by_points(teams),"diffs","all")
			elif txt is "4":
				graph_averages(sort_by_points(teams),"corners","all")
			elif txt is "5":
				graph_averages(sort_by_points(teams),"shots","all")
			elif txt is "6":
				graph_averages(sort_by_points(teams),"fouls","all")
			elif txt is "7":
				graph_averages(sort_by_points(teams),"cards","all")
			elif txt is "8":
				graph_averages(sort_by_points(teams),"shots_acc","all")
			elif txt is "9":
				h = input("HomeIndex ")
				a = input("AwayIndex ")
				predicts.predict_outcome(teams[int(h)],teams[int(a)],"scored")
			elif txt is "10":
				h = input("HomeIndex ")
				a = input("AwayIndex ")
				predicts.predict_outcome(teams[int(h)],teams[int(a)],"conceded")
			elif txt is "a":
				h = input("HomeIndex ")
				a = input("AwayIndex ")
				print_game_info(teams[int(h)],teams[int(a)])
			else:
				print_teams(teams)
