#lav en jøøddde gui og noget matplotlib

import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import numpy as np
import time

from geometry import distance


class nodeDrawer:
    def __init__(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.pointX = []
        self.pointY = []
        self.text = [] 
        self.lines = []
        self.latest_event = "None"
        self.routing_text = None

    def add_on_click(self, analyser):
        def on_click(event, drawer, figure, axis):
            if drawer.routing_text != None:
                drawer.routing_text.remove()
                drawer.routing_text = None

            id, pos = analyser.closest_node_to_pos((event.xdata, event.ydata))

            if distance(pos, (event.xdata,event.ydata)) < 0.8:
                drawer.routing_text = axis.text(0.05,
                            .95,
                            analyser.get_routing_table_text(f'{id}'),
                            fontsize = 8,     
                            ha='left',
                            va='top',
                            transform = axis.transAxes,
                            bbox=dict(facecolor='white', edgecolor='black'))
                
            figure.canvas.draw()

        cid = self.fig.canvas.mpl_connect('button_release_event', lambda event: on_click(event, self, self.fig, self.ax))


    def add_point(self,x,y,text):
        self.pointX.append(x)
        self.pointY.append(y)
        self.text.append(text)

    def add_line(self,x1,y1,x2,y2, color = "black"):
        #self.lines.append(lns.Line2D([x1,x2], [y1,y2]))
        circle_radius = 0.1
        self.lines.append(ptch.FancyArrow(x1,y1,(x2-x1),(y2-y1),
                                          head_width=0.2,
                                          length_includes_head=True,
                                          fill=False,
                                          color = color
                                          ))
        
    def add_single_point(self,x,y,color):
        self.ax.scatter(x,y,Color=color)

    def show(self, axis):
        self.ax.scatter(self.pointX,self.pointY, Color = 'dodgerblue')
        for i, label in enumerate(self.text):
            self.ax.annotate(label, (self.pointX[i]+0.3,self.pointY[i]-0.15))
        
        for line in self.lines:
            self.ax.add_line(line)
        

        ticks = np.arange(0, axis+1, axis/10)

        #self.ax.grid()
        self.ax.set_yticks(ticks)
        self.ax.set_xticks(ticks)
        self.ax.set_xlim([0, axis])
        self.ax.set_ylim([0, axis])
        #plt.show(block=False)

        #self.fig.clf()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()



    @staticmethod
    def show_static():
        plt.ioff()
        plt.show()


    def clear(self):
        self.pointX = []
        self.pointY = []
        self.text = [] 
        self.lines = []
        self.ax.clear()



if __name__ == '__main__':
    pass