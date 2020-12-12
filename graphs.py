import matplotlib.pyplot as plt
import matplotlib as mpl

import pandas as pd

import numpy as np


mpl.rcParams['toolbar'] = 'None'
fig = ""


def graph_goals(df, str):
	teams = df.Team.to_list()
	if "Scored" in str:
		hGoals1 = df.HScored1H.to_list()
		hGoals2 = df.HScored2H.to_list()
		aGoals1 = df.AScored1H.to_list()
		aGoals2 = df.AScored2H.to_list()
	else:
		hGoals1 = df.HConceded1H.to_list()
		hGoals2 = df.HConceded2H.to_list()
		aGoals1 = df.AConceded1H.to_list()
		aGoals2 = df.AConceded2H.to_list()

	plt.subplot(211)
	plt.bar(teams,hGoals1, label='1st Half Home')
	plt.bar(teams,hGoals2, bottom=hGoals1, label='2nd Half Home')
	plt.legend(prop={'size': 8})
	plt.title(str)
	plt.xticks(fontsize=10, rotation=20)

	plt.subplot(212)
	plt.bar(teams,aGoals1, label='1st Half Away')
	plt.bar(teams,aGoals2, bottom=aGoals1, label='2nd Half Away')
	plt.legend(prop={'size': 8})
	plt.xticks(fontsize=10, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def graph_situations(df,str):
	teams = df.Team.to_list()
	if "Corners" in str:
		hCorners1 = df.HCornersFavor.to_list()
		hCorners2 = df.HCornersAgainst.to_list()
		aCorners1 = df.ACornersFavor.to_list()
		aCorners2 = df.ACornersAgainst.to_list()
	elif "Fouls" in str:
		hFouls1 = df.HFoulsCommited.to_list()
		hFouls2 = df.HFoulsSuffered.to_list()
		aFouls1 = df.AFoulsCommited.to_list()
		aFouls2 = df.AFoulsSuffered.to_list()
	elif "Performance" in str:
		hPerf1 = df.HScored1H.sub(df.HConceded1H, axis = 0).to_list()
		hPerf2 = df.HScored2H.sub(df.HConceded2H, axis = 0).to_list()
		aPerf1 = df.AScored1H.sub(df.AConceded1H, axis = 0).to_list()
		aPerf2 = df.AScored2H.sub(df.AConceded2H, axis = 0).to_list()

	plt.subplot(211)
	if "Corners" in str:
		subcategorybar(teams, [hCorners1,hCorners2])
		plt.legend(('Home Corners in favor', 'Home Corners Against'), prop={'size': 8})
	elif "Fouls" in str:
		subcategorybar(teams, [hFouls1,hFouls2])
		plt.legend(('Home Fouls Commited', 'Home Fouls Suffered'), prop={'size': 8})
	elif "Performance" in str:
		subcategorybar(teams, [hPerf1,hPerf2], 0.6)
		plt.legend(('Home Performance 1Half', 'Home Performance 2Half'), prop={'size': 8})
		plt.axhline(y=0, color='black', linestyle='-')
	plt.title(str)
	plt.xticks(fontsize=10, rotation=20)

	plt.subplot(212)
	if "Corners" in str:
		subcategorybar(teams, [aCorners1,aCorners2])
		plt.legend(('Away Corners in favor', 'Away Corners Against'), prop={'size': 8})
	elif "Fouls" in str:
		subcategorybar(teams, [aFouls1,aFouls2])
		plt.legend(('Away Fouls Commited', 'Away Fouls Suffered'), prop={'size': 8})
	elif "Performance" in str:
		subcategorybar(teams, [aPerf1,aPerf2], 0.6)
		plt.legend(('Away Performance 1Half', 'Away Performance 2Half'), prop={'size': 8})
		plt.axhline(y=0, color='black', linestyle='-')
	plt.xticks(fontsize=10, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def subcategorybar(X, vals, width=0.8):
    n = len(vals)
    _X = np.arange(len(X))
    for i in range(n):
        plt.bar(_X - width/2. + i/float(n)*width, vals[i], 
                width=width/float(n), align="edge")   
    plt.xticks(_X, X)


def graph_situations_stack(df,str):
	teams = df.Team.to_list()
	if "Shots" in str:
		hShots1 = df.HShotsFavor.to_list()
		hShots2 = df.HShotsAgainst.to_list()
		aShots1 = df.AShotsFavor.to_list()
		aShots2 = df.AShotsAgainst.to_list()
		# target
		hShotsT1 = df.HShotsTFavor.to_list()
		hShotsT2 = df.HShotsTAgainst.to_list()
		aShotsT1 = df.AShotsTFavor.to_list()
		aShotsT2 = df.AShotsTAgainst.to_list()
	elif "Cards" in str:
		hYellow1 = df.HYellowFavor.to_list()
		hYellow2 = df.HYellowAgainst.to_list()
		aYellow1 = df.AYellowFavor.to_list()
		aYellow2 = df.AYellowAgainst.to_list()
		#Red
		hRed1 = df.HRedFavor.to_list()
		hRed2 = df.HRedAgainst.to_list()
		aRed1 = df.ARedFavor.to_list()
		aRed2 = df.ARedAgainst.to_list()

	plt.subplot(211)
	if "Shots" in str:
		subcategorybar_stack(teams, [hShots1,hShots2], [hShotsT1,hShotsT2])
		plt.legend(('Home Shots in favor', 'Home Shots on target in favor', 'Home Shots against', 'Home Shots on target against'), prop={'size': 8})
	elif "Cards" in str:
		subcategorybar_stack(teams, [hYellow1,hYellow2], [hRed1,hRed2])
		plt.legend(('Home Yellows in favor', 'Home Reds in favor', 'Home Yellows against', 'Home Reds against'), prop={'size': 8})
	plt.title(str)
	plt.xticks(fontsize=10, rotation=20)

	plt.subplot(212)
	if "Shots" in str:
		subcategorybar_stack(teams, [aShots1,aShots2], [aShotsT1,aShotsT2])
		plt.legend(('Away Shots in favor', 'Away Shots on target in favor', 'Away Shots against', 'Away Shots on target against'), prop={'size': 8})
	elif "Cards" in str:
		subcategorybar_stack(teams, [hYellow1,hYellow2], [hRed1,hRed2])
		plt.legend(('Away Yellows in favor', 'Away Reds in favor', 'Away Yellows against', 'Away Reds against'), prop={'size': 8})
	plt.xticks(fontsize=10, rotation=20)

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	plt.show()


def subcategorybar_stack(X, vals1, vals2, width=0.8):
    n = len(vals1)
    _X = np.arange(len(X))
    for i in range(n):
        plt.bar(_X - width/2. + i/float(n)*width, vals1[i],
                width=width/float(n), align="edge")
        plt.bar(_X - width/2. + i/float(n)*width, vals2[i],
                width=width/float(n), align="edge", bottom=vals1[i])
    plt.xticks(_X, X)


