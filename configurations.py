from visualizer import nodeDrawer
from rpl import Network
from rpl import Node, RootNode
from geometry import generate_random_nodes, generate_binary_tree_no_root
from simpy.util import start_delayed
import matplotlib.pyplot as plt


class base_simulation():
    def __init__(self,
                 env,
                 view = 14):
        self.env = env
        self.time = 0
        self.network = Network(self.env)

        self.figure = nodeDrawer()
        self.env.process(self.draw(view)) 
    
    def run(self, *args, **kwargs):
        self.run_simulation(*args, **kwargs)
        nodeDrawer.show_static()

    def run_simulation(self, *args, **kwargs):
        pass

    def draw(self, size):
        while True:
            for node in self.network.nodes:
                if node.is_alive:
                    if node.battery_life > 0:
                        self.figure.add_point(node.pos[0],node.pos[1],node.id)
                    else:
                        self.figure.add_single_point(node.pos[0],node.pos[1],'lightgray')
                    if node.rank != 0 and node.parent != None:
                        if self.network.idToNode[f'{node.parent}'].is_alive:
                            if not node.connectionsOut[f'{node.parent}'].empty or not node.connectionsIn[f'{node.parent}'].empty:
                                color = "green"
                            else:
                                color = "black"
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

    def setup_analyser(self, analyser):
        self.figure.add_on_click(analyser)
        self.network_analyser = analyser
    
    def add_analysis(self, analysis):
        self.env.process(analysis(self.env,self.network_analyser,self.time-1))

    def random_network(self, lower, upper, number_of_nodes):
        for index, position in enumerate(generate_random_nodes(number_of_nodes, lower, upper)):
            if index == 0:
                self.network.addNode(RootNode(self.env, position, None, 2, index, 500))
            else:
                self.network.addNode(Node(self.env, position, None, 2, index, 500))
    
    def tree_network(self, root_pos, number_of_layers, radio_range):
        number_of_layers -= 1
        self.network.addNode(RootNode(self.env, root_pos, None, radio_range, 0, 500))
        
        for index, position in enumerate(generate_binary_tree_no_root(number_of_layers, root_pos, radio_range),1):
            self.network.addNode(Node(self.env, position, None, radio_range, index, 500))
    
    def update_title(self, title):
        self.figure.latest_event = title + f" Time: {self.env.now}"
        yield self.env.timeout(1)

class binary_tree_simulation_1(base_simulation):
    def __init__(self, env, layers, view = 14):
        super().__init__(env, view)
        self.time = 200
        self.layers = layers

    def run_simulation(self, timesteps = 200):
        self.tree_network((5, 1), self.layers, 2)

        self.network.setup()
        self.time = timesteps

        start_delayed(self.env, self.network.kill_node(12), 60)
        start_delayed(self.env, self.update_title("kill node 12"), 60)

        start_delayed(self.env,self.network.idToNode['0'].global_repair(), 130)
        start_delayed(self.env,self.update_title("Global repair"), 130)

        self.env.run(until=timesteps)

class random_simulation_1(base_simulation):
    def __init__(self, env, view = 14):
        super().__init__(env, view)   
        self.time = 100

    def run_simulation(self, timesteps = 80):
        self.random_network(1,10,30)

        self.network.setup()
        self.time = timesteps

        self.env.run(until=timesteps)

class spawn_node_late_kill_later(base_simulation):
    def __init__(self, env):
        super().__init__(env, 10)   
        self.time = 250

    def run_simulation(self, timesteps = 250):
        self.tree_network((5, 1), 4, 2)
        self.network.setup()
        self.time = timesteps

        self.network.addNode(Node(self.env,(2.4, 5),None, 2, 100, 200))
        start_delayed(self.env, self.network.idToNode[f'{100}'].alive(), 40)
        start_delayed(self.env,self.update_title("Spawned node"), 40)

        start_delayed(self.env, self.network.kill_node(10), 80)
        start_delayed(self.env,self.update_title("Killed node 10 "), 80)

        start_delayed(self.env,self.network.idToNode['0'].global_repair(), 130)
        start_delayed(self.env,self.update_title("Global repair"), 130)

        self.env.run(until=timesteps)
    
    
if __name__ == '__main__':
    pass