import simpy
from copy import deepcopy



#math help functions 
def withinRadius(pos1, pos2, radius):
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])

    if dx>radius:
        return False
    if dy>radius: 
        return False
    return True


class Network(object):
    def __init__(self, env) -> None:
        self.env = env
        self.nodes = []

        self.nodes.append(RootNode(env, (1,2) , None, 2, 1))
        self.nodes.append(Node(env, (1,2) , None, 2, 2))
        self.nodes.append(Node(env, (1,3) , None, 2, 3))
        self.nodes.append(Node(env, (3,5) , None, 2, 4))
        self.nodes.append(Node(env, (3,6) , None, 2, 5))
        self.nodes.append(Node(env, (1,4) , None, 2, 6))
        self.nodes.append(Node(env, (5,8) , None, 2, 7))


        self.initNodeConnections()

        env.process(self.nodes[0].initiliazeNetwork())
        
        [env.process(node.alive()) for node in self.nodes]

    def initNodeConnections(self):
        [ innerNode.addConnection(outerNode)
          for innerNode in self.nodes 
          for outerNode in self.nodes 
          if withinRadius(innerNode.pos, outerNode.pos, innerNode.radioRadius) and
          innerNode.id != outerNode.id]

       # for innerNode in self.nodes:
        #    for outerNode in self.nodes:
         #       if innerNode.id != outerNode.id:
          #          if withinRadius(innerNode.pos, outerNode.pos, innerNode.radioRadius):
           #             print("worked")
            #            innerNode.addConnection(outerNode)


class MessageType(object):
    def __init__(self,
                 message_type,
                 ground_flag,
                 destination_advertisment_trigger,
                 destination_supported,
                 DAG_preference,
                 instance_id,
                 DAG_id) -> None:
        self.message_type = message_type
        self.ground_flag = ground_flag
        self.destination_advertisment_trigger = destination_advertisment_trigger
        self.destination_supported = destination_supported
        self.DAG_preference = DAG_preference
        self.sequence_number = 0
        self.instance_id = instance_id
        self.DAG_rank = 0
        self.DAG_id = DAG_id


class NodeConnection(object):
    def __init__(self, env) -> None:
        self.env = env
        #self.connection = simpy.Store(self.env, capacity=10)
        self.items = []
        self.empty = True

    def sendMessage(self, message):
        self.items.append(message)
        self.empty = False

    def readMessage(self) -> MessageType:
        print("file being read")
        msg = self.items.pop(0)
        if not self.items:
            self.empty = True
        return msg

class Node(object):
    def __init__(self, env, pos, parent, radius, id) -> None:
        self.env = env
        self.rank = 99
        self.id = id
        self.pos = pos
        self.parent = parent
        self.siblings = []
        self.children = []
        self.connectionsOut = {}
        self.connectionsIn = {}
        self.routingTable = {}
        self.radioRadius = radius

    def addConnection(self, node):
        if not (f"{node.id}" in self.connectionsOut): 
            connection = NodeConnection(self.env)
            self.connectionsOut[f'{node.id}'] = connection
            node.connectionsIn[f'{self.id}'] = connection

    def broadcastMessage(self,message):
        for _, connection in self.connectionsOut.items():
            connection.sendMessage(message)

    def alive(self):
        while True:
            yield self.env.timeout(5) #sleep time
            print(f'I id: {self.id} Aweken' )
            for _, connection in self.connectionsIn.items():
                if not connection.empty:
                    self.message_intepreter(connection.readMessage())
                    

    def message_intepreter(self,message):
        if message.message_type == 'dio':
            self.read_dio_message(message)

    def read_dio_message(self,message):
        if message.DAG_rank < self.rank:
            self.parent = message.instance_id
            self.routingTable[f'{message.instance_id}'] = self.connectionsOut[f'{message.instance_id}']
            self.rank = message.DAG_rank + 1 
            newMessage = deepcopy(message)
            newMessage.DAG_rank += 1 
            newMessage.instance_id = self.id
            self.broadcastMessage(newMessage)

        if message.DAG_rank == self.rank:
            self.siblings.append(message.instance_id)


class RootNode(Node,object):
    def __init__(self, env, pos, parent, radius, id) -> None:
        super().__init__(env, pos, parent, radius, id)
        self.rank = 0
        self.parent = None

    def initiliazeNetwork(self):
        self.broadcastMessage(self.construct_dio_message())
        yield self.env.timeout(1)

    def construct_dio_message(self):
        return MessageType(
            'dio',
            True,
            True,
            True,
            0b111,
            self.id,
            0b1000100101
        )

def counter_proc(env):
    counter = 0
    while True:
        print(counter)
        yield env.timeout(1)
        counter += 1

def main():
    env = simpy.Environment()
    
    network = Network(env)

    #node1 = Node(env, (1,2) , None, 2, 1)
    #node2 = Node(env, (3,5) , None, 2, 2)
    #rootnode = RootNode(env, (3,6) , None, 2, 3)

    #node1.addConnection(node2)


    #env.process(node1.alive())
    #env.process(node2.alive())

    env.process(counter_proc(env))
    env.run(until=50)

    [print(f'Node: {node.id} have rank: {node.rank} and parent {node.parent}') for node in network.nodes]    


if __name__ == '__main__':
    main()