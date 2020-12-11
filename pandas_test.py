import pandas as pd
import urllib.request
import os


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



league_games = getLeague('E0')
league_stats = calculateStats(league_games)
print(league_stats)

while(True):
	txt = input("0-Goals Scored\n1-Goals Conceded\n2-Diffs\n3-Corners\n4-Shots\n5-Fouls\n6-Cards\n7-Shots accuracy\n8-Predict_scored\n9-Predict_conceded\na-Game analysis\n")
	if txt is "0":
		graph_averages(league,"goalsScored","home")
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
