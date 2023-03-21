import math as math
import random

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

def generate_random_nodes(number_of_nodes, lower_limit, upper_limit):
    def rec_add_elem_out():
        def rec_add_elem(counter):
            element = (random.randint(lower_limit,upper_limit), random.randint(lower_limit,upper_limit))
            counter += 1
            if counter == max_elements:
                return
            if element in nodes:
                rec_add_elem(counter)
            else:
                nodes.add(element)
        rec_add_elem(0)

    max_elements = upper_limit-lower_limit + 1

    nodes = set()
    for _ in range(number_of_nodes):
        rec_add_elem_out()

    return nodes

if __name__ == '__main__':
    print(generate_random_nodes(100,1,10))