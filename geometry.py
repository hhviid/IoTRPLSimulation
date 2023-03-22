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

def generate_binary_tree_no_root(number_of_layers, root_pos, radio_range):
    nodes = set()
    acc_relative_pos =  0
    for layer in range(1,number_of_layers+1):
        nodes_y_pos = (layer * radio_range) + root_pos[1]
        current_layer_pos = radio_range * 0.5**(layer-1)
        relativ_pos_from_root_middle = acc_relative_pos + current_layer_pos
        acc_relative_pos += current_layer_pos
        number_of_nodes_in_layer = 2**layer 
        spacing_between_nodes = (relativ_pos_from_root_middle*2)/(number_of_nodes_in_layer-1)
        for node_number in range(int((2**layer)/2)):
            x_relative = relativ_pos_from_root_middle - (node_number * spacing_between_nodes)
            nodes.add((root_pos[0] + x_relative, nodes_y_pos))
            nodes.add((root_pos[0] - x_relative, nodes_y_pos))

    return nodes

        

def generate_random_nodes(number_of_nodes, lower_limit, upper_limit):
    def rec_add_elem_out():
        def rec_add_elem(counter):
            element = (random.randint(lower_limit,upper_limit), random.randint(lower_limit,upper_limit))
            if counter == max_elements:
                return
            if element in nodes:
                rec_add_elem(counter + 1)
            else:
                nodes.add(element)
        rec_add_elem(0)

    max_elements = upper_limit-lower_limit + 1

    nodes = set()
    for _ in range(number_of_nodes):
        rec_add_elem_out()

    return nodes

if __name__ == '__main__':
    print(generate_binary_tree_no_root(2,(50,1),20))