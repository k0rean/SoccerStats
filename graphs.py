import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

fig = ""

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
        self.conceded.bind("<Button-2>", self.conceded_func)
        self.conceded.pack()
        ## Diffs
        self.diffs = Button(self.widget1)
        self.diffs["text"] = "Diffs"
        self.diffs["font"] = ("Calibri", "9")
        self.diffs["width"] = 10
        self.diffs.bind("<Button-3>", self.diffs_func)
        self.diffs.pack()
        ## Corners
        self.corners = Button(self.widget1)
        self.corners["text"] = "Corners"
        self.corners["font"] = ("Calibri", "9")
        self.corners["width"] = 10
        self.corners.bind("<Button-4>", self.corners_func)
        self.corners.pack()
  
    def scored_func(self, event):
        graph_averages(fig,f.getTeams(),"goalsScored","home")

    def conceded_func(self, event):
    	graph_averages(fig,f.getTeams(),"goalsConceded","home")

    def diffs_func(self, event):
    	graph_averages(fig,f.getTeams(),"diffs","home")        

    def corners_func(self, event):
    	graph_averages(fig,f.getTeams(),"corners","all")
  
  
def initGUI():
	global fig
	root = Tk()
	root.attributes('-fullscreen', True)
	Application(root)
	fig = Figure(figsize=(8, 7), dpi=50)
	canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
	canvas.draw()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	root.mainloop()


def graph_averages(fig,teams,type,side):
	if type is "diffs":
		graph_diffs(fig,teams,side)
	elif type is "goalsScored":
		graph_goals_scored(fig,teams,side)
	elif type is "goalsConceded":
		graph_goals_conceded(fig,teams,side)
	elif type is "corners":
		graph_corners(fig,teams)

def graph_goals_scored(fig,teams,side):
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

	fig.subplot(2,1,1).scatter(names,teams_1st,c='r')
	aux = []
	for item in teams_1st:
		aux.append(teams_1st_average)
	fig.subplot(2,1,1).plot(names,aux)
	plt.title('1st Half Goals Scored ' + side)
	plt.xticks(fontsize=6, rotation=90)

	fig.subplot(2,1,2).scatter(names,teams_2nd,c='r')
	aux = []
	for item in teams_2nd:
		aux.append(teams_2nd_average)
	fig.subplot(2,1,2).plot(names,aux)
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