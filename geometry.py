import math as math

#math help functions 
def withinRadius(pos1, pos2, radius):
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])

    if dx>radius:
        return False
    if dy>radius: 
        return False
    return True

def distance(pos1, pos2):
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return math.sqrt(dy**2 + dx**2)

def generate_parallel_tree(number_of_nodes):
    pass

def generate_random_nodes(number_of_nodes):
    pass

if __name__ == '__main__':
    pass