import simpy
from visualizer import nodeDrawer
from rpl import Network
from rpl import Node, RootNode
from analyser import NetworkAnalyser
from geometry import generate_random_nodes, generate_binary_tree_no_root

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

def draw(env,network,figure,size):
    while True:
        for node in network.nodes:
            if node.is_alive:
                if node.battery_life > 0:
                    figure.add_point(node.pos[0],node.pos[1],node.rank)
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

        figure.ax.set_title(f'Discrete time: {env.now}  |  Last event: {figure.latest_event}')
        figure.show(size)

        yield env.timeout(1)
        figure.clear()
        

def analyse(env,networkAnalyser, time):
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
        if env.now == time:
            break
        yield env.timeout(1)

    fig, ax = plt.subplots()
    ax.plot(running_sum_dis)
    ax.plot(running_sum_dao)
    ax.plot(running_sum_dio)
    #ax.plot(running_sum)

    ax.legend(['dis','dao','dio'])
    plt.show()

def random_network(env,network, lower, upper, number_of_nodes):
    for index, position in enumerate(generate_random_nodes(number_of_nodes, lower, upper)):
        if index == 0:
            network.addNode(RootNode(env, position, None, 2, index, 200))
        else:
            network.addNode(Node(env, position, None, 2, index, 120))


def tree_network(env, network, root_pos, number_of_layers, radio_range):
    number_of_layers -= 1
    network.addNode(RootNode(env, root_pos, None, radio_range, 0))
    
    for index, position in enumerate(generate_binary_tree_no_root(number_of_layers, root_pos, radio_range),1):
        network.addNode(Node(env, position, None, radio_range, index, 500))

def update_title(env, figure, title):
    figure.latest_event = title + f" Time: {env.now}"
    yield env.timeout(1)

            
def main():
    env = simpy.Environment()

    lower = 1
    upper = 20
    number_of_nodes = 130
    
    network = Network(env)
    tree_network(env,network, (5, 1), 5, 2)
    #random_network(env,network, 1, 10, 60)
    network.setup()

    view = 14
    figure = nodeDrawer()
    env.process(draw(env,network,figure,view)) 

    start_delayed(env,network.idToNode['12'].kill(), 40)
    start_delayed(env,update_title(env, figure, "kill node 12"), 40)

    start_delayed(env,network.idToNode['0'].global_repair(), 60)
    start_delayed(env,update_title(env, figure, "Global repair"), 60)



    network_analyser = NetworkAnalyser(env,network)
    env.process(analyse(env,network_analyser, 100))
    
    env.run(until=101)


    [print(f'Node: {node.id} have rank: {node.rank} and parent {node.parent}') for node in network.nodes]  

    table = '1'
    print(f'\nRouting table id: {table}')
    for id, connection in network.idToNode[table].routing_table_easy_read.items():
        print(f'Target: {id}   |  Next hop: {connection}')
  

    nodeDrawer.show_static()


if __name__ == '__main__':
    main()