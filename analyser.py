# this file should be an analyser on the netwrok

from rpl import Network

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
            for _,connection in node.connectionsOut.items():
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