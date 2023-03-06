import simpy


class TestClass(object):
    def __init__(self,env) -> None:
        self.env = env
        self.action = env.process(self.run())
    
    def run(self) -> None:
        while True:
            print("test")
            yield self.env.timeout(10)


#math help functions
def withinRadius(pos1, pos2, radius):
    pass


class Network(object):
    def __init__(self, env) -> None:
        self.env = env
        self.nodes = []

class MessageType(object):
    def __init__(self) -> None:
        self.test = 1 

class NodeConnection(object):
    def __init__(self, env) -> None:
        self.env = env
        self.connection = simpy.Store(self.env, capacity=10)

    def sendMessage(self) -> None:
        test = MessageType()
        self.connection.put(test)

    def readMessage(self) -> MessageType:
        msg = yield self.connection.get()
        print(msg.test)
        return msg


class Node(object):
    def __init__(self, env, pos, parent, radius, id) -> None:
        self.env = env
        self.id = id
        self.pos = pos
        self.parent = parent
        self.siblings = []
        self.children = []
        self.connections = {}
        self.routingTable = {}
        self.radioRadius = radius

    def addConnection(self, node):
        connection = NodeConnection(self.env)
        self.connections[f'{node.id}'] = connection
        node.connections[f'{self.id}'] = connection

    def alive(self):
        while True:
            yield self.env.timeout(5)
            pass 

class RootNode(Node,object):
    def __init__(self, env, pos, parent, radius) -> None:
        super().__init__(env, pos, parent, radius)

    def initiliazeNetwork(self):
        pass #broadcast DIO message




def main():
    env = simpy.Environment()
    
    node1 = Node(env, (1,2) , None, 2, 1)
    node2 = Node(env, (3,5) , None, 2, 2)

    node1.addConnection(node2)
    node1.connections['2'].sendMessage()
    env.process(node2.connections['1'].readMessage())

    env.run(until=50)
    


if __name__ == '__main__':
    main()