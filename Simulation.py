import simpy


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

        self.nodes.append(Node(env, (1,2) , None, 2, 1))
        self.nodes.append(Node(env, (1,3) , None, 2, 2))
        self.nodes.append(RootNode(env, (1,2) , None, 2, 3))

        self.initNodeConnections()

    def initNodeConnections(self):
        [print("InnerNode ", innerNode.id, "have connection ", outerNode.id) and
          innerNode.addConnection(outerNode)
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
    def __init__(self, text = "empty") -> None:
        self.text = text


class NodeConnection(object):
    def __init__(self, env) -> None:
        self.env = env
        #self.connection = simpy.Store(self.env, capacity=10)
        self.items = []
        self.empty = True

    def sendMessage(self, message):
        test = MessageType(message)
        self.items.append(test)
        self.empty = False

    def readMessage(self) -> MessageType:
        msg = self.items.pop()
        if not self.items:
            self.empty = True
        return msg



class Node(object):
    def __init__(self, env, pos, parent, radius, id) -> None:
        self.env = env
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


    def broadcastMessage(self):
        for connection in self.connectionsOut.items():
            connection.sendMessage()

    def alive(self):
        while True:
            yield self.env.timeout(5) #sleep time
            print(f'I id: {self.id} Aweken' )
            for _, connection in self.connectionsIn.items():
                if not connection.empty:
                    print(connection.readMessage().text)



class RootNode(Node,object):
    def __init__(self, env, pos, parent, radius, id) -> None:
        super().__init__(env, pos, parent, radius, id)

    def initiliazeNetwork(self):
        pass #broadcast DIO message




def main():
    env = simpy.Environment()
    
    network = Network(env)

    #node1 = Node(env, (1,2) , None, 2, 1)
    #node2 = Node(env, (3,5) , None, 2, 2)
    #rootnode = RootNode(env, (3,6) , None, 2, 3)

    #node1.addConnection(node2)


    #env.process(node1.alive())
    #env.process(node2.alive())

    env.run(until=50)
    


if __name__ == '__main__':
    main()