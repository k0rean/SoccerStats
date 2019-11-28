from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
  
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
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"

    def conceded_func(self, event):
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"

    def diffs_func(self, event):
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"

    def corners_func(self, event):
        if self.msg["text"] == "Primeiro widget":
            self.msg["text"] = "O botão recebeu um clique"
  

root = Tk()
root.attributes('-fullscreen', True)
Application(root)
fig = Figure(figsize=(8, 7), dpi=50)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
root.mainloop()