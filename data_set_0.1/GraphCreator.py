import networkx as nx
import VertexCreator as vc


# class GraphCreator creates new graph from the following files
# - edges file
# - vertex data file
# the constructor also gets the number of vertices to be in every component
class GraphCreator:
    def __init__(self, edges_file_name, data_file_name, connected_size):
        # creating new graph using network-x package
        self.graph = nx.Graph()
        # getting list of all vertices (with attributes) from the relevant files
        vertices_creator = vc.VertexCreator(data_file_name)
        vertices_list = vertices_creator.get_all(connected_size)

        for vertex in vertices_list:
            self.graph.add_node(int(vertex.vertex_num), data=vertex)

        # open edges file and read all the file until the end
        edges_file = open(edges_file_name)
        curr_edge = edges_file.readline()
        while curr_edge != "":
            # get the edge as list of two integers
            curr_edge = curr_edge.split()
            # and edge only if the two nodes exists
            if self.graph.has_node(int(curr_edge[0])) and self.graph.has_node(int(curr_edge[1])):
                self.graph.add_edge(int(curr_edge[0]), int(curr_edge[1]))
            # read next line from the file
            curr_edge = edges_file.readline()

    def get_graph(self):
        return self.graph
