from geometry import withinRadius
from geometry import distance

from copy import deepcopy



class Network(object):
    def __init__(self, env) -> None:
        self.env = env
        self.nodes = []
        self.idToNode = {}


    def setup(self):
        for node in self.nodes:
            self.idToNode[f'{node.id}'] = node 

        self.initNodeConnections()

        self.env.process(self.nodes[0].initiliazeNetwork())
        [self.env.process(node.alive()) for node in self.nodes]

    def initNodeConnections(self):
        [ innerNode.addConnection(outerNode)
          for innerNode in self.nodes 
          for outerNode in self.nodes 
          if withinRadius(innerNode.pos, outerNode.pos, innerNode.radioRadius) and
          innerNode.id != outerNode.id]

    def addNode(self, node):
        for other_node in self.nodes:
            if withinRadius(node.pos, other_node.pos, node.radioRadius):
                node.addConnection(other_node)
        self.nodes.append(node)
        self.idToNode[f'{node.id}'] = node

    def kill_node(self, node_id):
        node_to_kill = self.idToNode[f'{node_id}']
        node_to_kill.kill()

        for node in list(filter(lambda node: True if f'{node_to_kill.id}' in node.connectionsOut else False, self.nodes)):
            node.connectionsOut.pop(f'{node_to_kill.id}')

        yield self.env.timeout(1)


class MessageType(object):
    def __init__(self, message_type) -> None:
        self.message_type = message_type

class DIOMessage(MessageType):
    def __init__(self,
                ground_flag,
                destination_advertisment_trigger,
                destination_supported,
                DAG_preference,
                instance_id,
                DAG_id,
                version_number = 1):
        super().__init__('dio')
        self.ground_flag = ground_flag
        self.destination_advertisment_trigger = destination_advertisment_trigger
        self.destination_supported = destination_supported
        self.DAG_preference = DAG_preference
        self.sequence_number = 0
        self.instance_id = instance_id
        self.DAG_rank = 0
        self.DAG_id = DAG_id
        self.version_number = version_number

class DAOMessage(MessageType):
    def __init__(self,
                 d_flag,
                 dao_sender_id,
                 last_node_id
                 ):
        super().__init__('dao')
        self.d_flag = d_flag 
        self.dao_sender_id = dao_sender_id
        self.last_node_id = last_node_id

class DISMessage(MessageType):
    def __init__(self, 
                 dis_sender_id,
                 node) -> None:
        super().__init__('dis')
        self.dis_sender_id = dis_sender_id
        self.node = node
        

class NodeConnection(object):
    def __init__(self, env, distance) -> None:
        self.env = env
        self.items = []
        self.empty = True
        self.distance = distance

    def sendMessage(self, message):
        self.items.append(message)
        self.empty = False

    def readMessage(self) -> MessageType:
        msg = self.items.pop(0)
        if not self.items:
            self.empty = True
        return msg

class networkInteface():
    def __init__(self) -> None:
        self.connections_in = []
        self.connections_out = []
    

class Node(object):
    class lose_battery(object):
        def __init__(self, amount):
            self.amount = amount

        def __call__(self, foo, *args, **kwargs):
            def inner_func(*args, **kwargs):
                args[0].battery_life -= self.amount
                if args[0].battery_life < 0:
                   args[0].is_alive = False
                foo(*args,**kwargs)
            return inner_func
        
    def __init__(self, env, pos, parent, radius, id, battery_life = 100) -> None:
        self.env = env
        self.is_alive = False
        self.rank = 99
        self.battery_life = battery_life
        self.id = id
        self.pos = pos
        self.parent = parent
        self.siblings = []
        self.children = []
        self.connectionsOut = {}
        self.connectionsIn = {}
        self.routingTable = {}
        self.routing_table_easy_read = {}
        self.radioRadius = radius
        self.latest_dio = None
        
    def read_item_generator(self):
        while True:
            for _, connection in self.connectionsIn.items():
                if not connection.empty:
                    self.message_intepreter(connection.readMessage())
                    yield 
            yield

    def addConnection(self, node):
        if not (f"{node.id}" in self.connectionsOut): 
            connection = NodeConnection(self.env, distance(node.pos, self.pos))
            self.connectionsOut[f'{node.id}'] = connection
            node.connectionsIn[f'{self.id}'] = connection
        
    @lose_battery(2)
    def broadcastMessage(self,message):
        if self.connectionsOut:
            for _, connection in self.connectionsOut.items():
                connection.sendMessage(message)

    @lose_battery(2)
    def unicast_message(self,message,target):
        self.routingTable[f'{target}'].sendMessage(message)

    def alive(self):
        self.is_alive = True
        tricle_timer = 0
        reader = self.read_item_generator()

        while self.is_alive:
            if self.parent == None:
                tricle_timer += 1

                if tricle_timer == 10:
                    self.broadcastMessage(DISMessage(self.id,self))
                    tricle_timer = 0

            next(reader)
            yield self.env.timeout(1) 
    
    def kill(self):
        self.reset()
        self.is_alive = False

    @lose_battery(1)
    def message_intepreter(self,message):
        if message.message_type == 'dio':
            self.read_dio_message(message)
        if message.message_type == 'dao':
            self.read_dao_message(message)
        if message.message_type == 'dis':
            self.read_dis_message(message)

    def read_dio_message(self,message):
        if self.check_for_higher_dodag_version(message):
            self.reset()
            
        #if you get dio from parent -> update network topology with DAO message 
        if message.instance_id == self.parent: 
            self.unicast_message(DAOMessage(False, self.id, self.id), self.parent)
            newMessage = deepcopy(message)
            newMessage.DAG_rank += 1 
            newMessage.instance_id = self.id
            self.latest_dio = newMessage
            self.broadcastMessage(newMessage)
        else:
            if self.is_better_connection(message):
                self.parent = message.instance_id

                self.routingTable[f'{message.instance_id}'] = self.connectionsOut[f'{message.instance_id}']
                self.routing_table_easy_read[f'{message.instance_id}'] = f'{message.instance_id}'

                self.rank = message.DAG_rank + 1 

                self.unicast_message(DAOMessage(False, self.id, self.id), self.parent)

                newMessage = deepcopy(message)
                newMessage.DAG_rank += 1 
                newMessage.instance_id = self.id
                self.latest_dio = newMessage
                self.broadcastMessage(newMessage)

        if message.DAG_rank == self.rank:
            self.siblings.append(message.instance_id)

    def read_dao_message(self,message):
        #if f'{message.dao_sender_id}' not in self.routingTable:
        self.routingTable[f'{message.dao_sender_id}'] = self.connectionsOut[f'{message.last_node_id}']
        self.routing_table_easy_read[f'{message.dao_sender_id}'] = f'{message.last_node_id}'

        messageCopy = deepcopy(message)
        messageCopy.last_node_id = self.id
        self.unicast_message(messageCopy, self.parent)

    def read_dis_message(self,message):
        self.addConnection(message.node)
        if self.latest_dio != None:
            self.routing_table_easy_read[f'{message.dis_sender_id}'] = f'{message.dis_sender_id}'
            self.routingTable[f'{message.dis_sender_id}'] = self.connectionsOut[f'{message.dis_sender_id}']
            self.unicast_message(self.latest_dio, message.dis_sender_id)

    def is_better_connection(self, message):        
        if message.DAG_rank == self.rank - 1:
            if self.connectionsOut[f'{self.parent}'].distance < self.connectionsOut[f'{message.instance_id}'].distance:
                return False
        
        if message.DAG_rank < self.rank:
            return True
        
        return False

    def check_for_higher_dodag_version(self, message):
        if self.latest_dio != None:
            return True if self.latest_dio.version_number < message.version_number else False
        else:
            return False

    def reset(self):
        self.rank = 99
        self.parent = None


class RootNode(Node,object):
    def __init__(self, env, pos, parent, radius, id, battery_life = 100) -> None:
        super().__init__(env, pos, parent, radius, id, battery_life)
        self.rank = 0
        self.parent = None
        self.tricle_timer = 0
        self.dodag_version_number = 0

    def alive(self):
        self.is_alive = True
        reader = self.read_item_generator()

        while True:
            self.tricle_timer += 1
            if self.tricle_timer == 90:
                self.tricle_timer = 0
                self.broadcastMessage(self.construct_dio_message(self.dodag_version_number))

            next(reader)
            yield self.env.timeout(1) 


    def global_repair(self):
        self.broadcastMessage(self.construct_dio_message(self.dodag_version_number + 1))
        yield self.env.timeout(1)        
    
    def initiliazeNetwork(self):
        self.broadcastMessage(self.construct_dio_message())
        yield self.env.timeout(1)

    def construct_dio_message(self, version_number = 1):
        self.dodag_version_number = version_number
        self.latest_dio =  DIOMessage(
            True,
            True,
            True,
            0b111,
            self.id,
            0b1000100101,
            version_number
        )
        return self.latest_dio
    
    def read_dao_message(self, message):
        self.routingTable[f'{message.dao_sender_id}'] = self.connectionsOut[f'{message.last_node_id}']
        self.routing_table_easy_read[f'{message.dao_sender_id}'] = f'{message.last_node_id}'

if __name__ == '__main__':
    pass