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
 
class Node(object):
    def __init__(self, env, pos, parent, radius) -> None:
        self.env = env
        self.pos = pos
        self.parent = parent
        self.siblings = []
        self.children = []
        self.radioRadius = radius

class RootNode(Node,object):
    def __init__(self, env, pos, parent, radius) -> None:
        super().__init__(env, pos, parent, radius)

    def initiliazeNetwork(self):
        pass #broadcast DIO message




def main():
    env = simpy.Environment()
    test = TestClass(env)
    env.run(until=50)
    


if __name__ == '__main__':
    main()