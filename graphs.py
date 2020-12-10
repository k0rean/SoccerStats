import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px


mpl.rcParams['toolbar'] = 'None'
fig = ""

def graph_averages(teams,type,side):
	if type is "diffs":
		if side is "all":
			graph_diffs_complete(teams)
		else:
			graph_diffs(teams,side)
	elif type is "goalsScored":
		if side is "all":
			graph_goals_scored_complete_bar(teams)
		else:
			graph_goals_scored(teams,side)
	elif type is "goalsConceded":
		if side is "all":
			graph_goals_conceded_complete_bar(teams)
		else:
			graph_goals_conceded(teams,side)
	elif type is "corners":
		graph_corners_bar(teams)
	elif type is "shots":
		graph_shots_bar(teams)
	elif type is "shots_acc":
		graph_shots_acc(teams)
	elif type is "cards":
		graph_cards_bar(teams)
	elif type is "fouls":
		graph_fouls_bar(teams)


def graph_goals_scored_complete(teams):
	teams_1st, teams_1stH, teams_1stA = [], [], []
	teams_2nd, teams_2ndH, teams_2ndA = [], [], []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1stH.append(team.hScored_first)
		teams_2ndH.append(team.hScored_second)
		teams_1stA.append(team.aScored_first)
		teams_2ndA.append(team.aScored_second)
		teams_1st.append((team.hScored_first+team.hScored_second)/2)
		teams_2nd.append((team.aScored_first+team.aScored_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r', label='total')
	plt.scatter(names,teams_1stH,c='g', label='1st')
	plt.scatter(names,teams_2ndH,c='b', label='2nd')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux, label='avg')
	plt.legend()
	plt.title('Home Goals Scored ')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r', label='total')
	plt.scatter(names,teams_1stA,c='g', label='1st')
	plt.scatter(names,teams_2ndA,c='b', label='2nd')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux, label='average')
	plt.title('Away Goals Scored ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_goals_scored_complete_bar(teams):
	teams_1st, teams_1stH, teams_1stA = [], [], []
	teams_2nd, teams_2ndH, teams_2ndA = [], [], []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1stH.append(team.hScored_first)
		teams_2ndH.append(team.hScored_second)
		teams_1stA.append(team.aScored_first)
		teams_2ndA.append(team.aScored_second)
		teams_1st.append((team.hScored_first+team.hScored_second)/2)
		teams_2nd.append((team.aScored_first+team.aScored_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.bar(names,teams_1stH, label='1st Half Home')
	plt.bar(names,teams_2ndH, bottom=teams_1stH, label='2nd Half Home')
	plt.legend()
	plt.title('Goals Scored ')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.bar(names,teams_1stA, label='1st Half Away')
	plt.bar(names,teams_2ndA, bottom=teams_1stA, label='2nd Half Away')
	#plt.title('Away Goals Scored ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()



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
	#plt.plot(names,aux)
	plt.title('1st Half Goals Scored ' + side)
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('2nd Half Goals Scored ' + side)
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_goals_conceded_complete(teams):
	teams_1st, teams_1stH, teams_1stA = [], [], []
	teams_2nd, teams_2ndH, teams_2ndA = [], [], []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1stH.append(team.hConceded_first)
		teams_2ndH.append(team.hConceded_second)
		teams_1stA.append(team.aConceded_first)
		teams_2ndA.append(team.aConceded_second)
		teams_1st.append((team.hConceded_first+team.hConceded_second)/2)
		teams_2nd.append((team.aConceded_first+team.aConceded_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r', label='total')
	plt.scatter(names,teams_1stH,c='g', label='1st')
	plt.scatter(names,teams_2ndH,c='b', label='2nd')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux, label='avg')
	plt.legend()
	plt.title('Home Goals Conceded ')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r', label='total')
	plt.scatter(names,teams_1stA,c='g', label='1st')
	plt.scatter(names,teams_2ndA,c='b', label='2nd')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux, label='average')
	plt.title('Away Goals Conceded ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_goals_conceded_complete_bar(teams):
	teams_1st, teams_1stH, teams_1stA = [], [], []
	teams_2nd, teams_2ndH, teams_2ndA = [], [], []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1stH.append(team.hConceded_first)
		teams_2ndH.append(team.hConceded_second)
		teams_1stA.append(team.aConceded_first)
		teams_2ndA.append(team.aConceded_second)
		teams_1st.append((team.hConceded_first+team.hConceded_second)/2)
		teams_2nd.append((team.aConceded_first+team.aConceded_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.bar(names,teams_1stH, label='1st Half Home')
	plt.bar(names,teams_2ndH, bottom=teams_1stH, label='2nd Half Home')
	plt.legend()
	plt.title('Goals Conceded ')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.bar(names,teams_1stA, label='1st Half Away')
	plt.bar(names,teams_2ndA, bottom=teams_1stA, label='2nd Half Away')
	#plt.title('Away Goals Conceded ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

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
	#plt.plot(names,aux)
	plt.title('1st Half Goals Conceded ' + side)
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('2nd Half Goals Conceded ' + side)
	plt.xticks(fontsize=8, rotation=20)

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
	#plt.plot(names,aux)
	plt.title('1st Half Performance ' + side)
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('2nd Half Performance ' + side)
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_diffs_complete(teams):
	teams_1st, teams_1stH, teams_1stA = [], [], []
	teams_2nd, teams_2ndH, teams_2ndA = [], [], []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1stH.append(team.hRate_first)
		teams_2ndH.append(team.hRate_second)
		teams_1stA.append(team.aRate_first)
		teams_2ndA.append(team.aRate_second)
		teams_1st.append((team.hRate_first+team.hRate_second)/2)
		teams_2nd.append((team.aRate_first+team.aRate_second)/2)

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r', label='total')
	plt.scatter(names,teams_1stH,c='g', label='1st')
	plt.scatter(names,teams_2ndH,c='b', label='2nd')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	plt.plot(names,aux, label='avg')
	plt.legend()
	plt.title('Home Performance ')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r', label='total')
	plt.scatter(names,teams_1stA,c='g', label='1st')
	plt.scatter(names,teams_2ndA,c='b', label='2nd')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	plt.plot(names,aux, label='average')
	plt.title('Away Performance ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

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
	#plt.plot(names,aux)
	plt.title('Corners home')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('Corners away')
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_corners_bar(teams):
	teams_1st = []
	teams_2nd = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(team.hCorners)
		teams_2nd.append(team.aCorners)

	plt.subplot(2,1,1)
	plt.bar(names,teams_1st, label='Home')
	plt.title('Corners')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.bar(names,teams_2nd, label='Away', color='orange')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

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
	plt.scatter(names,teams_1st,c='r', label='shots')
	plt.scatter(names,teams_1stT,c='b', label='shots on goal')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	#plt.plot(names,aux)
	plt.title('Shots home')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r', label='shots')
	plt.scatter(names,teams_2ndT,c='b', label='shots on goal')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('Shots away')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_shots_bar(teams):
	teams_1st = []
	teams_2nd = []
	teams_1stT = []
	teams_2ndT = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(team.hShots-team.hShotsT)
		teams_2nd.append(team.aShots-team.aShotsT)
		teams_1stT.append(team.hShotsT)
		teams_2ndT.append(team.aShots)


	plt.subplot(2,1,1)
	plt.bar(names,teams_1st, label='Shots off goal Home')
	plt.bar(names,teams_1stT, bottom=teams_1st, label='Shots on goal Home')
	plt.legend()
	plt.title('Shots ')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.bar(names,teams_2nd, label='Shots off goal Away')
	plt.bar(names,teams_2ndT, bottom=teams_2nd, label='Shots on goal Away')
	#plt.title('Away Goals Scored ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

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
		teams_1st.append(100*((team.hScored_first+team.hScored_second)/team.hShots))
		teams_2nd.append(100*((team.aScored_first+team.aScored_second)/team.aShots))
		teams_1stT.append(100*((team.hScored_first+team.hScored_second)/team.hShotsT))
		teams_2ndT.append(100*((team.aScored_first+team.aScored_second)/team.aShotsT))

	teams_1st_average = sum(teams_1st)/len(teams_1st)
	teams_2nd_average = sum(teams_2nd)/len(teams_2nd)
	teams_1stT_average = sum(teams_1stT)/len(teams_1st)
	teams_2ndT_average = sum(teams_2ndT)/len(teams_2nd)

	plt.subplot(2,1,1)
	plt.bar(names,teams_1st, label='Shots Home')
	plt.bar(names,[teams_1stT[i]-teams_1st[i] for i in range(len(teams_1st))], bottom=teams_1st, label='Shots on goal Home')
	plt.legend()
	plt.title('Shots success percentage')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.bar(names,teams_2nd, label='Shots Away')
	plt.bar(names,[teams_2ndT[i]-teams_2nd[i] for i in range(len(teams_2nd))], bottom=teams_2nd, label='Shots on goal Away')
	#plt.title('Away Goals Scored ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_shots_acc_bar(teams):
	teams_1st = []
	teams_2nd = []
	teams_1stT = []
	teams_2ndT = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(100*((team.hScored_first+team.hScored_second)/team.hShots))
		teams_2nd.append(100*((team.aScored_first+team.aScored_second)/team.aShots))
		teams_1stT.append(100*((team.hScored_first+team.hScored_second)/team.hShotsT))
		teams_2ndT.append(100*((team.aScored_first+team.aScored_second)/team.aShotsT))

	plt.subplot(2,1,1)
	plt.scatter(names,teams_1st,c='r', label='shots')
	plt.scatter(names,teams_1stT,c='b', label='shots on goal')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	#plt.plot(names,aux)
	plt.title('Shots accuracy home')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r', label='shots')
	plt.scatter(names,teams_2ndT,c='b', label='shots on goal')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('Shots accuracy away')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

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
	#plt.plot(names,aux)
	plt.title('Fouls')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('Fouls away')
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_fouls_bar(teams):
	teams_1st = []
	teams_2nd = []
	names = []
		
	for team in teams:
		names.append(team.name)
		teams_1st.append(team.hFouls)
		teams_2nd.append(team.aFouls)

	plt.subplot(2,1,1)
	plt.bar(names,teams_1st, label='Home')
	plt.title('Fouls')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.bar(names,teams_2nd, label='Away', color='orange')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

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
	#plt.plot(names,aux)
	plt.title('Cards home')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.scatter(names,teams_2nd,c='y')
	plt.scatter(names,teams_2ndT,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	#plt.plot(names,aux)
	plt.title('Cards away')
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_cards_bar(teams):
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
	plt.bar(names,teams_1st, color='y', label='Yellow Cards Home')
	plt.bar(names,teams_1stT, bottom=teams_1st, color='r', label='Red Cards Home')
	plt.legend()
	plt.title('Cards ')
	plt.xticks(fontsize=8, rotation=20)

	plt.subplot(2,1,2)
	plt.bar(names,teams_2nd, color='y', label='Yellow Cards Away')
	plt.bar(names,teams_2ndT, bottom=teams_2nd, color='r', label='Red Cards Away')
	#plt.title('Away Goals Scored ')
	plt.legend()
	plt.xticks(fontsize=8, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()