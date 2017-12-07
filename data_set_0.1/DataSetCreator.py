########################################################################################################################
# Oved Nagar 7.12.17                                                                                                   #
########################################################################################################################

import networkx as nx
import VertexCreator as vc
import random

eps = 0.1
num_of_components = 100
min_size_component = 3
max_size_component = 5
num_of_nodes_in_graph = 100000
num_edges_in_graph = 400000
edges_output_file = "data_set_edge_5"
data_output_file = "data_set_data_5"
component_out_file = "data_set_comp_5"

mark = [0] * (num_of_nodes_in_graph + 1)
vertex_list = []
G = nx.Graph()
for i in range(1, num_of_nodes_in_graph + 1):
    v = vc.Vertex(i, random.randint(0, 6), 0.3 + (random.random() * 0.7), 1, 0)
    G.add_node(i, data=v)

for i in range(1, num_edges_in_graph):
    G.add_edge(random.randint(1, num_of_nodes_in_graph), random.randint(1, num_of_nodes_in_graph))


def get_reachable(Graph, component):
    reachable_r = []
    for n in component:
        # iterate over all reachable and add if its not already in the neighbors/comp_i
        for node_u in nx.all_neighbors(Graph, n):
            if int(node_u) not in reachable_r and int(node_u) not in component and mark[node_u] == 0:
                marked_neighbor = False
                # check the the neighbor doesnt have more neighbors that are already in component
                for u_node in nx.all_neighbors(Graph, node_u):
                    if int(u_node) not in reachable_r and int(u_node) not in component and mark[u_node] == 1:
                        marked_neighbor = True
                        break
                if not marked_neighbor:
                    reachable_r.append(int(node_u))
    return reachable_r


connected_file = open(component_out_file, "w")
# list to save number of components created from each size 1..8
comp_sizes = [0] * max_size_component
# list to save number of components of each weight <= 0.1 - 0.12 - 0.15 - 0.18 - 0.2 - 0.22 - 0.25 - 0.28 - >2.8
comp_weights = [0] * 9

# create 100 components
comp_loop = num_of_components
i = 0
while i < comp_loop:
    # random start node and size of component
    comp = []
    size = random.randint(min_size_component, max_size_component)
    start = random.randint(1, num_of_nodes_in_graph)
    # mark as part of component or choose other node
    good_start_point = True
    if mark[start] == 1:
        good_start_point = False
    for u in nx.all_neighbors(G, start):
        if mark[u] == 1:
            good_start_point = False
    if not good_start_point:
        continue
    mark[start] = 1
    comp.append(start)
    # give new weight to node
    G.node[start]['data'].colorScore = random.random() * (eps*0.95 / size)
    weight = G.node[start]['data'].colorScore
    curr_node = start
    # choose one component from reachable nodes and add it
    size_loop = size
    j = 1
    while j < size_loop:
        reachable = get_reachable(G, comp)
        reach_node = random.choice(reachable)
        if mark[reach_node] == 1:
            continue
        # mark and give new weight
        mark[reach_node] = 1
        G.node[reach_node]['data'].colorScore = random.random() * (eps*0.95 / size)
        weight = weight + G.node[reach_node]['data'].colorScore
        comp.append(reach_node)
        j += 1

    comp_sizes[size - 1] += 1

    for node in comp:
        print(str(node) + " ", end="")
        connected_file.write(str(node) + " ")
    print(" = " + str(weight))
    connected_file.write("\n")
    connected_file.write(str(weight) + "\n")

    i += 1

    if weight <= 0.1:
        comp_weights[0] += 1
    if weight <= 0.12:
        comp_weights[1] += 1
    if weight <= 0.15:
        comp_weights[2] += 1
    if weight <= 0.18:
        comp_weights[3] += 1
    if weight <= 0.2:
        comp_weights[4] += 1
    if weight <= 0.22:
        comp_weights[5] += 1
    if weight <= 0.25:
        comp_weights[6] += 1
    if weight <= 0.28:
        comp_weights[7] += 1
    if weight <= eps:
        comp_weights[8] += 1

connected_file.write("number of components of weight..\n")
connected_file.write("0.1-0.12-0.15-0.18-0.2-0.22-0.25-0.28-eps\n")
for w in comp_weights:
    print(str(w) + " ", end="")
    connected_file.write(str(w) + " ")
print()
connected_file.write("\n")

connected_file.write("component size\n")
i = 0
for s in comp_sizes:
    print("size " + str(i) + ": " + str(s))
    connected_file.write(str(s) + " ")
    i += 1

edges_file = open(edges_output_file, "w")
data_file = open(data_output_file, "w")

for edge in G.edges():
    edges_file.write(str(edge[0]) + " " + str(edge[1]) + "\n")

for v in G.nodes():
    vertex = G.node[v]['data']
    data = str(v) + " " + str(vertex.color) + " " + str(vertex.colorScore) + " " + str(vertex.test) + "\n"
    data_file.write(data)

edges_file.close()
data_file.close()


b = 0





