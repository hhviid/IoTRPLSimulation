import simpy
from analyser import NetworkAnalyser, message_analysis, root_routing_table_analysis
import configurations as cfg

"""
TODO:
* Implement local repair 
* Implemement different DODAG priorities
"""
            
def main():
    env = simpy.Environment()

    simulation = cfg.spawn_node_late_kill_later(env)
    simulation.setup_analyser(NetworkAnalyser(env,simulation.network))
    simulation.add_analysis(message_analysis)
    simulation.add_analysis(root_routing_table_analysis)
    simulation.run()
    

if __name__ == '__main__':
    main()