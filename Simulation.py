import simpy
from analyser import NetworkAnalyser, message_analysis, root_routing_table_analysis,time_to_node_deaths, time_battery_distribution
import configurations as cfg

import matplotlib.pyplot as plt

"""
TODO:
* Implement local repair 
* Implemement different DODAG priorities
"""
            
def main():
    env = simpy.Environment()

    #simulation = cfg.binary_tree_simulation_no_events(env, 5, view=12)
    #simulation = cfg.spawn_node_late_kill_later(env)
    simulation = cfg.spawn_node_late_kill_later(env, 5)
    simulation.setup_analyser(NetworkAnalyser(env,simulation.network))
    simulation.add_analysis(message_analysis)
    simulation.add_analysis(root_routing_table_analysis)
    simulation.add_analysis(time_to_node_deaths)
    simulation.add_analysis(time_battery_distribution)
    simulation.run()
    
def plot_avg_death_time():
    import itertools as it
    def get_avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0) / len(x)
    
    n_nodes = [50]
    _, ax = plt.subplots()
    _, ax2 = plt.subplots()


    for n_node in n_nodes:
        with open(f'deathtimes{n_node}.txt') as file:
            lines = [line.rstrip() for line in file]

        new_list = [[int(val) for val in line[:-1].split(",")] for line in lines]
        result = list(map(get_avg, it.zip_longest(*new_list)))

        ax.scatter(result,range(len(result)))
        ax2.scatter(n_node, result[1])


    ax.set_xlabel('time step')
    ax.set_ylabel('#node death')
    ax.set_title('time to death of nodes')
    ax.legend(n_nodes)
    ax2.legend(n_nodes)
    ax2.set_xlabel('number of nodes')
    ax2.set_ylabel('time to first death')
    ax2.set_title('time to first death in network')
    plt.show()



if __name__ == '__main__':
    #for x in range(50): 
    #    main()
    #plot_avg_death_time()
    main()
