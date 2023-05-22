from rpl import Network
from visualizer import nodeDrawer
import matplotlib.pyplot as plt
from geometry import distance
import numpy as np


def message_analysis(env, analyser, timesteps):
    running_sum_dis = []
    running_sum_dao = []
    running_sum_dio = []
    while True:
        dao,dis,dio = analyser.sum_of_each_message_type()
        running_sum_dis.append(dis)
        running_sum_dao.append(dao)
        running_sum_dio.append(dio)
        if env.now == timesteps - 1:
            break
        yield env.timeout(1)

    fig, ax = plt.subplots()
    ax.plot(running_sum_dis)
    ax.plot(running_sum_dao)
    ax.plot(running_sum_dio)

    ax.legend(['dis','dao','dio'])
    ax.set_xlabel('Time step')
    ax.set_ylabel('Total messages in network')
    ax.set_title('Messages in network')

def root_routing_table_analysis(env, analyser, timesteps):
    running_size = []
    while True:
        running_size.append(analyser.length_of_routing_table('0'))
        if env.now == timesteps - 1:
            break
        yield env.timeout(1)

    total_nodes = analyser.get_total_nodes_in_network()

    _, ax = plt.subplots()
    ax.plot(list(map(lambda n: n/total_nodes,running_size)))
    ax.set_xlabel('Time step')
    ax.set_ylabel('cdf')
    ax.set_title('cdf of root routing table')

def time_to_node_deaths(env, analyser, timesteps):
    dead_nodes = []
    death_times = []
    while True:
        dead, node = analyser.any_node_dead(dead_nodes)
        if dead:
            death_times.append(env.now)
            dead_nodes.append(node)
        if env.now == timesteps - 1:
            break
        yield env.timeout(1)

    print(f'Death times: {death_times}')
    #_, ax = plt.subplots()
    #ax.scatter(death_times,range(len(death_times)))
    #ax.set_xlabel('time step')
    #ax.set_ylabel('#node death')
    #ax.set_title('time to death of nodes')


    # open file in write mode
    with open(r'deathtimes250.txt', 'a') as fp:
        for death_time in death_times:
            # write each item on a new line
            fp.write("%s, " % death_time)
        fp.write("\n")
        print('Done')

def time_battery_distribution(env, analyser, timesteps):
    battery_distribution = []
    test = []

    while True:
        battery_distribution.append(analyser.transform_list_to_histogram(analyser.get_all_current_battery_life(), 200))
        test.append(analyser.get_all_current_battery_life())
        if env.now == timesteps - 1:
            break
        yield env.timeout(1)

    _, ax = plt.subplots()

    
    
    battery_distribution_np = np.array(battery_distribution)
    test_np = np.array(test)
    image_to_show = np.empty(battery_distribution_np.shape)

    for index, inner in enumerate(battery_distribution_np):
        image_to_show[index] = np.flip(inner)

    hmm = []
    for inner in  image_to_show.T:
        output = []
        for i in range(0,len(inner),1):
            window = inner[i:i+1]
            output.append(sum(window))
        hmm.append(output)

    print(image_to_show)
    ax.imshow(hmm,
            cmap='Greens',
            interpolation='nearest',
            extent=[0,499,0,200],
            vmin=0,
            vmax=5)
    
    ax.set_xlabel('Discrete time step')
    ax.set_ylabel('Battery life')
    ax.set_title(f'Binary heatmap for {len(test_np[0]) + 1} nodes')
    
    #for data in test_np.T:
    #    ax.plot(data)


class NetworkAnalyser():
    def __init__(self, env, network):
        self.network = network
        self.env = env

    def any_node_dead(self, excluded_nodes):
        nodes_checked = [node for node in self.network.nodes if node.id not in excluded_nodes]
        for node in nodes_checked:
            if not node.is_alive:
                return True, node.id
        return False, "NaN"

    def get_all_current_battery_life(self):
        return [node.battery_life for node in self.network.nodes if node.rank != 0]
    
    def transform_list_to_histogram(self, battery_lifes, max_battery_life):
        histogram = [0] * max_battery_life
        for index in range(max_battery_life):
            for battery_life in battery_lifes:
                if battery_life == index:
                    histogram[index] += 1

        return histogram
            

    def sum_of_messages(self):
        sum = 0
        for node in self.network.nodes:
            for _,connection in node.connectionsOut.items():
                sum += len(connection.items)

        return sum
    
    def sum_of_each_message_type(self):
        dao = 0
        dis = 0
        dio = 0

        for node in self.network.nodes:
            dao_tmp, dis_tmp, dio_tmp = self.__sum_of_messages(node)
            dao += dao_tmp
            dis += dis_tmp
            dio += dio_tmp

        return dao,dis,dio

    def sum_of_each_message_type_one_node(self,nodeId):
        node = self.network.idToNode[nodeId]
        return self.__sum_of_messages(node)
    
    def length_of_routing_table(self, nodeId):
        return len(self.network.idToNode[nodeId].routingTable)
    
    def get_routing_table_closest_node(self, pos):
        closest_node, _ = self.closest_node_to_pos(pos)
        return self.get_routing_table_text(f'{closest_node}')
    
    def get_total_nodes_in_network(self):
        return len(self.network.nodes)
    
    def get_routing_table_text(self, nodeId):
        id_to_nodes = self.network.idToNode[nodeId].routing_table_easy_read
        return f'Node: {nodeId} \n\n' + "\n".join("{!r} : {!r}".format(k, v).replace("'","") for k, v in id_to_nodes.items()) 

    def closest_node_to_pos(self, pos):
        node_iterator = iter(self.network.nodes)
        closest_node = next(node_iterator)
        shortest_distance = distance(pos,closest_node.pos)
        for node in node_iterator:
            cur_distance = distance(pos, node.pos)
            if cur_distance < shortest_distance:
                shortest_distance = cur_distance
                closest_node = node
        return closest_node.id, closest_node.pos
    
    def __sum_of_messages(self, node):
        dao,dis,dio = 0,0,0

        for _,connection in node.connectionsIn.items():
            for message in connection.items:
                if message.message_type == 'dio':
                    dio += 1
                if message.message_type == 'dao':
                    dao += 1
                if message.message_type == 'dis':
                    dis += 1

        return dao,dis,dio
    
if __name__ == '__main__':
    pass 