from rpl import Network
from visualizer import nodeDrawer
import matplotlib.pyplot as plt


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
    nodeDrawer.show_static()

class NetworkAnalyser():
    def __init__(self, env, network):
        self.network = network
        self.env = env

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