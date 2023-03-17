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
    
if __name__ == '__main__':
    pass 