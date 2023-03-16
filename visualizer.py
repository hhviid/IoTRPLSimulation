#lav en jøøddde gui og noget matplotlib

import matplotlib.pyplot as plt
import matplotlib.lines as lns
import matplotlib.patches as ptch
import numpy as np


class myFigure:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.pointX = []
        self.pointY = []
        self.ranks = [] 
        self.lines = []

    def add_point(self,x,y,rank):
        self.pointX.append(x)
        self.pointY.append(y)
        self.ranks.append(rank)

    def add_line(self,x1,y1,x2,y2):
        #self.lines.append(lns.Line2D([x1,x2], [y1,y2]))
        circle_radius = 0.1
        self.lines.append(ptch.FancyArrow(x1,y1,(x2-x1),(y2-y1),
                                          head_width=0.2,
                                          length_includes_head=True,
                                          fill=False
                                          ))


    def show(self):
        self.ax.scatter(self.pointX,self.pointY)
        for i, label in enumerate(self.ranks):
            self.ax.annotate(label, (self.pointX[i]+0.3,self.pointY[i]-0.15))
        
        for line in self.lines:
            self.ax.add_line(line)

        plt.show()


