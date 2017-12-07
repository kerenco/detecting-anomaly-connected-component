########################################################################################################################
# Oved Nagar 7.12.17                                                                                                   #
########################################################################################################################

import GraphCreator as gc
import os

# class GraphCreator creates new graph from the following files
# - tested file - test_mask.txt
# - labels file - lables.txt
# - scores file - preds.txt
# - edges file - cora.cites
# - index file - idx_map.txt format(edge-real-value, position-by-row-in-the-files)
# the constructor also gets -epsilon to filter vertices with score_color < epsilon
print("this program will convert graph representation from 5 files")
print("- tested/not tested file")
print("- color file")
print("- scores file file")
print("- edges file")
print("- index file (format - edge-real-value, position-by-row-in-the-files)")
tested_file_name = input("enter tested or not file name:\t")
color_file_name = input("enter color file name:\t")
score_file_name = input("enter score file name:\t")
edges_file_name = input("enter edges file name:\t")
index_file_name = input("enter index file name:\t")
print("\n-------------------------------------------------------------------------------------\n")

g_create = gc.GraphCreator(edges_file_name, tested_file_name, color_file_name, score_file_name, index_file_name)
G = g_create.get_graph()

print("the output files will be")
print("- edges file")
print("- vertices-data file - (vertex-color-color_score)")
print("\n-------------------------------------------------------------------------------------\n")

if not os.path.exists("new graph"):
    os.makedirs("new graph")

new_edges_name = input("enter new Graph edges file name:\t")
new_data_name = input("enter new Graph data file name:\t")
new_edges_file = open("new graph/" + new_edges_name, "w+")
new_data_file = open("new graph/" + new_data_name, "w+")

print("\n-------------------------------------------------------------------------------------\n")

for edge in G.edges():
    new_edges_file.write(str(edge[0]) + " " + str(edge[1]) + "\n")

for v in G.nodes():
    vertex = G.node[v]['data']
    data = str(v) + " " + str(vertex.color) + " " + str(vertex.colorScore) + " " + str(vertex.test) + "\n"
    new_data_file.write(data)

new_data_file.close()
new_edges_file.close()
print("success!")
