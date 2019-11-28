import matplotlib.pyplot as plt

def graph_averages(teams,type,side):
	if type is "diffs":
		graph_diffs(teams,side)
	elif type is "goalsScored":
		graph_goals_scored(teams,side)
	elif type is "goalsConceded":
		graph_goals_conceded(teams,side)
	elif type is "corners":
		graph_corners(teams)
	elif type is "shots":
		graph_shots(teams)
	elif type is "shots_acc":
		graph_shots_acc(teams)
	elif type is "fouls":
		graph_fouls(teams)
	elif type is "cards":
		graph_cards(teams)

def graph_goals_scored(teams,side):
	teams_1st = []
	teams_2nd = []
	names = []
		
	if side is "home":
		for team in teams:
			names.append(team.name)
			teams_1st.append(team.hScored_first)
			teams_2nd.append(team.hScored_second)
	elif side is "away":
		for team in teams:
			names.append(team.name)
			teams_1st.append(team.aScored_first)
			teams_2nd.append(team.aScored_second)
	else:
		for team in teams:
			names.append(team.name)
			teams_1st.append((team.hScored_first+team.aScored_first)/2)
			teams_2nd.append((team.hScored_second+team.aScored_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('1st Half Goals Scored ' + side)
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('2nd Half Goals Scored ' + side)
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()

def graph_goals_conceded(teams,side):
	teams_1st = []
	teams_2nd = []
	names = []

	if side is "home":
		for team in teams:
			names.append(team.name)
			teams_1st.append(team.hConceded_first)
			teams_2nd.append(team.hConceded_second)
	elif side is "away":
		for team in teams:
			names.append(team.name)
			teams_1st.append(team.aConceded_first)
			teams_2nd.append(team.aConceded_second)
	else:
		for team in teams:
			names.append(team.name)
			teams_1st.append((team.hConceded_first+team.aConceded_first)/2)
			teams_2nd.append((team.hConceded_second+team.aConceded_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('1st Half Goals Conceded ' + side)
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('2nd Half Goals Conceded ' + side)
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_diffs(teams,side):
	teams_1st = []
	teams_2nd = []
	names = []

	if side is "home":
		for team in teams:
			names.append(team.name)
			teams_1st.append(team.hRate_first)
			teams_2nd.append(team.hRate_second)
	elif side is "away":
		for team in teams:
			names.append(team.name)
			teams_1st.append(team.aRate_first)
			teams_2nd.append(team.aRate_second)
	else:
		for team in teams:
			names.append(team.name)
			teams_1st.append((team.hRate_first+team.aRate_first)/2)
			teams_2nd.append((team.hRate_second+team.aRate_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('1st Half Performance ' + side)
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('2nd Half Performance ' + side)
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()

def graph_corners(teams):
	teams_1st = []
	teams_2nd = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(team.hCorners)
		teams_2nd.append(team.aCorners)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('Corners home')
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('Corners away')
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()

def graph_shots(teams):
	teams_1st = []
	teams_2nd = []
	teams_1stT = []
	teams_2ndT = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(team.hShots)
		teams_2nd.append(team.aShots)
		teams_1stT.append(team.hShotsT)
		teams_2ndT.append(team.aShotsT)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)
	teams_1stT_average = sum(teams_1stT)/len(teams_1st)
	teams_2ndT_average = sum(teams_2ndT)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r')
	plt.scatter(names,teams_1stT,c='b')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('Shots home')
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	plt.scatter(names,teams_2ndT,c='b')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('Shots away')
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_shots_acc(teams):
	teams_1st = []
	teams_2nd = []
	teams_1stT = []
	teams_2ndT = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append((team.hScored_first+team.hScored_second)/team.hShots)
		teams_2nd.append((team.aScored_first+team.aScored_second)/team.aShots)
		teams_1stT.append((team.hScored_first+team.hScored_second)/team.hShotsT)
		teams_2ndT.append((team.aScored_first+team.aScored_second)/team.aShotsT)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)
	teams_1stT_average = sum(teams_1stT)/len(teams_1st)
	teams_2ndT_average = sum(teams_2ndT)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r')
	plt.scatter(names,teams_1stT,c='b')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('Shots accuracy home')
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	plt.scatter(names,teams_2ndT,c='b')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('Shots accuracy away')
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_fouls(teams):
	teams_1st = []
	teams_2nd = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(team.hFouls)
		teams_2nd.append(team.aFouls)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('Fouls home')
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('Fouls away')
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()

def graph_cards(teams):
	teams_1st = []
	teams_2nd = []
	teams_1stT = []
	teams_2ndT = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(team.hYellow)
		teams_2nd.append(team.aYellow)
		teams_1stT.append(team.hRed)
		teams_2ndT.append(team.aRed)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)
	teams_1stT_average = sum(teams_1stT)/len(teams_1st)
	teams_2ndT_average = sum(teams_2ndT)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='y')
	plt.scatter(names,teams_1stT,c='r')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux)
	plt.title('Cards home')
	plt.xticks(fontsize=6, rotation=90)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='y')
	plt.scatter(names,teams_2ndT,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux)
	plt.title('Cards away')
	plt.xticks(fontsize=6, rotation=90)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()