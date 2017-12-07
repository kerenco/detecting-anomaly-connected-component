import networkx as nx
import VertexCreator as vc


# class GraphCreator creates new graph from the following files
# - tested file - test_mask.txt
# - labels file - labels.txt
# - scores file - preds.txt
# - edges file - cora.cites
# - index file - idx_map.txt format(edge-real-value, position-by-row-in-the-files)
# the constructor also gets -epsilon to filter vertices with score_color < epsilon
class GraphCreator:
    def __init__(self, edges_file_name, tested_file_name, label_file_name, score_file_name, index_file_name):
        # creating new graph using network-x package
        self.graph = nx.Graph()
        # getting list of all vertices (with attributes) from the relevant files
        vertices_creator = vc.VertexCreator(tested_file_name, label_file_name, score_file_name)
        vertices_list = vertices_creator.get_all()

        # creating a list of tuples [(real-edge-value, row-location-in-files)....], sorted by the
        # location of the vertices in the files
        map_file = open(index_file_name)
        index_sorted = []
        next_index = map_file.readline()
        while next_index != "":
            next_index = next_index.replace(",", " ")
            next_index = next_index.split()
            # append tuple
            index_sorted.append((int(next_index[0]), int(next_index[1])))
            next_index = map_file.readline()
        index_sorted.sort(key=lambda x: x[1])

        # adding vertices to the graph as tuples ( vertex-number, vertex-attributes ) using the list of vertices
        # and the index_sorted list that indicates the real value of an edge
        for i in range(0, len(vertices_list)):
            self.graph.add_node(int(index_sorted[i][0]), data=vertices_list[i])

        # open edges file and read all the file until the end
        edges_file = open(edges_file_name)
        next_edge_from_file = edges_file.readline()
        while next_edge_from_file != "":
            # get the edge as list of two integers
            curr_edge = next_edge_from_file.split()
            # and edge only if the two nodes exists
            if self.graph.has_node(int(curr_edge[0])) and self.graph.has_node(int(curr_edge[1])):
                self.graph.add_edge(int(curr_edge[0]), int(curr_edge[1]))
            # read next line from the file
            next_edge_from_file = edges_file.readline()

    def get_graph(self):
        return self.graph
