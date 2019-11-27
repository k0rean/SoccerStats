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