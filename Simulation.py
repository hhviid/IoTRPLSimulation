import simpy
from analyser import NetworkAnalyser, message_analysis
import configurations as cfg

"""
TODO:
* Implement local repair 
* Implemement different DODAG priorities
"""
            
def main():
    env = simpy.Environment()

    simulation = cfg.binary_tree_simulation_1(env, 4)
    simulation.setup_analyser(NetworkAnalyser(env,simulation.network))
    simulation.add_analysis(message_analysis)
    simulation.run()
    
    [print(f'Node: {node.id} have rank: {node.rank} and parent {node.parent}') for node in simulation.network.nodes]  

    table = '0'
    print(f'\nRouting table id: {table}')
    for id, connection in simulation.network.idToNode[table].routing_table_easy_read.items():
        print(f'Target: {id}   |  Next hop: {connection}')
  

if __name__ == '__main__':
    main()