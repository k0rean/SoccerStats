import csv
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import sys
import urllib.request
from Game import game
from Team import team
import graphs
import predicts
import os

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
		txt = input("1-Goals Scored\n2-Goals Conceded\n3-Diffs\n4-Corners\n5-Shots\n6-Fouls\n7-Cards\n8-Shots accuracy\n9-Predict_scored\n10-Predict_conceded\n")
		if txt is "1":
			graphs.graph_averages(sort_by_points(teams),"goalsScored","home")
			graphs.graph_averages(sort_by_points(teams),"goalsScored","away")
			graphs.graph_averages(sort_by_points(teams),"goalsScored","all")
		elif txt is "2":
			graphs.graph_averages(sort_by_points(teams),"goalsConceded","home")
			graphs.graph_averages(sort_by_points(teams),"goalsConceded","away")
			graphs.graph_averages(sort_by_points(teams),"goalsConceded","all")
		elif txt is "3":
			graphs.graph_averages(sort_by_points(teams),"diffs","home")
			graphs.graph_averages(sort_by_points(teams),"diffs","away")
			graphs.graph_averages(sort_by_points(teams),"diffs","all")
		elif txt is "4":
			graphs.graph_averages(sort_by_points(teams),"corners","all")
		elif txt is "5":
			graphs.graph_averages(sort_by_points(teams),"shots","all")
		elif txt is "6":
			graphs.graph_averages(sort_by_points(teams),"fouls","all")
		elif txt is "7":
			graphs.graph_averages(sort_by_points(teams),"cards","all")
		elif txt is "8":
			graphs.graph_averages(sort_by_points(teams),"shots_acc","all")
		elif txt is "9":
			h = input("HomeIndex ")
			a = input("AwayIndex ")
			predicts.predict_outcome(teams[int(h)],teams[int(a)],"scored")
		elif txt is "10":
			h = input("HomeIndex ")
			a = input("AwayIndex ")
			predicts.predict_outcome(teams[int(h)],teams[int(a)],"conceded")
		else:
			print_teams(teams)
