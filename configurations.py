from visualizer import nodeDrawer
from rpl import Network
from rpl import Node, RootNode
from geometry import generate_random_nodes, generate_binary_tree_no_root
from simpy.util import start_delayed
import matplotlib.pyplot as plt


class base_simulation():
    def __init__(self,
                 env):
        self.env = env
        self.time = 0
        self.network = Network(self.env)

        self.figure = nodeDrawer()
        self.env.process(self.draw(14)) 
    
    def run(self, timesteps):
        pass

    def draw(self, size):
        while True:
            for node in self.network.nodes:
                if node.is_alive:
                    if node.battery_life > 0:
                        self.figure.add_point(node.pos[0],node.pos[1],node.rank)
                    else:
                        self.figure.add_single_point(node.pos[0],node.pos[1],'lightgray')
                    if node.rank != 0 and node.parent != None:
                        if not node.connectionsOut[f'{node.parent}'].empty or not node.connectionsIn[f'{node.parent}'].empty:
                            color = "green"
                        else:
                            color = "black"
                        self.figure.add_line(
                            node.pos[0],
                            node.pos[1],
                            self.network.idToNode[f'{node.parent}'].pos[0],
                            self.network.idToNode[f'{node.parent}'].pos[1],
                            color)
                else:
                    self.figure.add_single_point(node.pos[0],node.pos[1],'lightgray')

            self.figure.ax.set_title(f'Discrete time: {self.env.now}  |  Last event: {self.figure.latest_event}')
            self.figure.show(size)

            yield self.env.timeout(1)
            self.figure.clear()

    def analyse(self):
        running_sum_dis = []
        running_sum_dao = []
        running_sum_dio = []
        #running_sum = []
        while True:
            dao,dis,dio = self.network_analyser.sum_of_each_message_type()
            #running_sum.append(networkAnalyser.sum_of_messages())
            running_sum_dis.append(dis)
            running_sum_dao.append(dao)
            running_sum_dio.append(dio)
            if self.env.now == self.time - 1:
                break
            yield self.env.timeout(1)

        fig, ax = plt.subplots()
        ax.plot(running_sum_dis)
        ax.plot(running_sum_dao)
        ax.plot(running_sum_dio)
        #ax.plot(running_sum)

        ax.legend(['dis','dao','dio'])
        nodeDrawer.show_static()

    def setup_anaylser(self, analyser):
        self.network_analyser = analyser
        self.env.process(self.analyse())

    def random_network(self, lower, upper, number_of_nodes):
        for index, position in enumerate(generate_random_nodes(number_of_nodes, lower, upper)):
            if index == 0:
                self.network.addNode(RootNode(self.env, position, None, 2, index, 200))
            else:
                self.network.addNode(Node(self.env, position, None, 2, index, 200))
    
    def tree_network(self, root_pos, number_of_layers, radio_range):
        number_of_layers -= 1
        self.network.addNode(RootNode(self.env, root_pos, None, radio_range, 0, 500))
        
        for index, position in enumerate(generate_binary_tree_no_root(number_of_layers, root_pos, radio_range),1):
            self.network.addNode(Node(self.env, position, None, radio_range, index, 500))
    
    def update_title(self, title):
        self.figure.latest_event = title + f" Time: {self.env.now}"
        yield self.env.timeout(1)

class binary_tree_simulation_1(base_simulation):
    def __init__(self, env):
        super().__init__(env)

    def run(self, timesteps = 201):
        self.tree_network((5, 1), 5, 2)

        self.network.setup()
        self.time = timesteps

        start_delayed(self.env,self.network.idToNode['12'].kill(), 60)
        start_delayed(self.env,self.update_title("kill node 12"), 60)

        start_delayed(self.env,self.network.idToNode['0'].global_repair(), 130)
        start_delayed(self.env,self.update_title("Global repair"), 130)

        self.env.run(until=timesteps)

class random_simulation_1(base_simulation):
    def __init__(self, env):
        super().__init__(env)   

    def run(self, timesteps = 201):
        self.random_network(1,10,60)

        self.network.setup()
        self.time = timesteps

        self.env.run(until=timesteps)
    
if __name__ == '__main__':
    pass