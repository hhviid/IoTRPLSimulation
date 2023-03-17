import simpy
from visualizer import myFigure
from rpl import Network
from rpl import Node
from analyser import NetworkAnalyser

from simpy.util import start_delayed

"""
TODO:

* Implement functions in Geometry.py to
* Implement local repair 
* Implement global repair
* Implemement different DODAG priorities

"""



def counter_proc(env):
    counter = 0
    while True:
        print(counter)
        yield env.timeout(1)
        counter += 1

def draw(env,network):
    figure = myFigure()

    while True:
        for node in network.nodes:
            if node.is_alive:
                figure.add_point(node.pos[0],node.pos[1],node.rank)
                if node.rank != 0 and node.parent != None:
                    figure.add_line(
                        node.pos[0],
                        node.pos[1],
                        network.idToNode[f'{node.parent}'].pos[0],
                        network.idToNode[f'{node.parent}'].pos[1])
            else:
                figure.add_single_point(node.pos[0],node.pos[1],'lightgray')

        figure.ax.set_title(f'Discrete time: {env.now}')
        figure.show(10)

        yield env.timeout(1)
        figure.clear()
        

def analyse(env,networkAnalyser):
    running_sum = []
    while True:
        running_sum.append(networkAnalyser.sum_of_messages())
        if env.now == 49:
            break
        yield env.timeout(1)
    
    print(running_sum)

def main():
    env = simpy.Environment()
    
    network = Network(env)
    network_analyser = NetworkAnalyser(env,network)
    env.process(analyse(env,network_analyser))

    network.addNode(Node(env, (7,8) , None, 2, 22))
    start_delayed(env, network.idToNode['22'].alive(), 20)

    network.addNode(Node(env, (2,5) , None, 2, 23))
    start_delayed(env, network.idToNode['23'].alive(), 30)

    env.process(draw(env,network))

    
    
    
    env.process(counter_proc(env))
    env.run(until=50)

    [print(f'Node: {node.id} have rank: {node.rank} and parent {node.parent}') for node in network.nodes]  


    table = '6'
    print(f'\nRouting table id: {table}')
    for id, connection in network.idToNode[table].routing_table_easy_read.items():
        print(f'Target: {id}   |  Next hop: {connection}')
  
    myFigure.show_static()

if __name__ == '__main__':
    main()