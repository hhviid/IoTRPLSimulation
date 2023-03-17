import simpy
from visualizer import myFigure
from rpl import Network
import json

"""
TODO:

* Implement DAO message (rework initial structure)
* Implement functions in Geometry.py to
* Implement routing tables with DAO messages
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

def draw(network):
    figure = myFigure()

    for node in network.nodes:
        figure.add_point(node.pos[0],node.pos[1],node.id)
        if node.rank != 0 and node.parent != None:
            figure.add_line(
                node.pos[0],
                node.pos[1],
                network.idToNode[f'{node.parent}'].pos[0],
                network.idToNode[f'{node.parent}'].pos[1])

    figure.show()


def main():
    env = simpy.Environment()
    
    network = Network(env)

    env.process(counter_proc(env))
    env.run(until=100)

    [print(f'Node: {node.id} have rank: {node.rank} and parent {node.parent}') for node in network.nodes]  


    table = '3'
    print(f'\nRouting table id: {table}')
    for id, connection in network.idToNode[table].routing_table_easy_read.items():
        print(f'Target: {id}   |  Next hop: {connection}')
  
    draw(network)



if __name__ == '__main__':
    main()