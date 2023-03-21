import simpy
from visualizer import nodeDrawer
from rpl import Network
from rpl import Node, RootNode
from analyser import NetworkAnalyser
from geometry import generate_random_nodes

from simpy.util import start_delayed

import matplotlib.pyplot as plt


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

def draw(env,network,size):
    figure = nodeDrawer()

    while True:
        for node in network.nodes:
            if node.is_alive:
                if node.battery_life > 0:
                    figure.add_point(node.pos[0],node.pos[1],node.id)
                else:
                    figure.add_single_point(node.pos[0],node.pos[1],'lightgray')
                if node.rank != 0 and node.parent != None:
                    figure.add_line(
                        node.pos[0],
                        node.pos[1],
                        network.idToNode[f'{node.parent}'].pos[0],
                        network.idToNode[f'{node.parent}'].pos[1])
            else:
                figure.add_single_point(node.pos[0],node.pos[1],'lightgray')

        figure.ax.set_title(f'Discrete time: {env.now}')
        figure.show(size)

        yield env.timeout(1)
        figure.clear()
        

def analyse(env,networkAnalyser):
    running_sum_dis = []
    running_sum_dao = []
    running_sum_dio = []
    #running_sum = []
    while True:
        dao,dis,dio = networkAnalyser.sum_of_each_message_type()
        #running_sum.append(networkAnalyser.sum_of_messages())
        running_sum_dis.append(dis)
        running_sum_dao.append(dao)
        running_sum_dio.append(dio)
        if env.now == 95:
            break
        yield env.timeout(1)

    fig, ax = plt.subplots()
    ax.plot(running_sum_dis)
    ax.plot(running_sum_dao)
    ax.plot(running_sum_dio)
    #ax.plot(running_sum)

    ax.legend(['dis','dao','dio'])
    plt.show()


def main():
    env = simpy.Environment()

    lower = 1
    upper = 10
    number_of_nodes = 40
    
    network = Network(env)
    for index, position in enumerate(generate_random_nodes(number_of_nodes, lower, upper)):
        if index == 0:
            network.addNode(RootNode(env, position, None, 2, index))
        else:
            network.addNode(Node(env, position, None, 2, index))

    network.setup()

    #network.addNode(Node(env, (7,8) , None, 2, 22))
    #start_delayed(env, network.idToNode['22'].alive(), 20)

    #network.addNode(Node(env, (2,5) , None, 2, 23))
    #start_delayed(env, network.idToNode['23'].alive(), 30)

    network_analyser = NetworkAnalyser(env,network)
    env.process(analyse(env,network_analyser))

    env.process(draw(env,network,upper+1)) 
    
    env.process(counter_proc(env))
    env.run(until=100)

    [print(f'Node: {node.id} have rank: {node.rank} and parent {node.parent}') for node in network.nodes]  


    table = '1'
    print(f'\nRouting table id: {table}')
    for id, connection in network.idToNode[table].routing_table_easy_read.items():
        print(f'Target: {id}   |  Next hop: {connection}')
  

    nodeDrawer.show_static()


if __name__ == '__main__':
    main()