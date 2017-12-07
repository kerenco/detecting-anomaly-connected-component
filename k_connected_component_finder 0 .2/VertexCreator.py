class ComponentList:
    def __init__(self, connected_size):
        # this list will hold groups of size t = 1..k that their sum is under epsilon and the vertex is part of them
        # the list will be saved in the following format
        # <components of all sizes>[<components of size t>[<the component itself>[]]] e.g
        # t = 1 [[[0]],
        # t = 2 [[0, 1], [0, 2], [0, 3]]
        # t = 3 [[0, 1 , 3], [0, 1, 4], [0, 2, 4]]]
        self.components = [None] * connected_size
        for i in range(0, connected_size):
            self.components[i] = {}
        self.weights = [None] * connected_size
        for i in range(0, connected_size):
            self.weights[i] = {}

    def add_comp(self, size, comp, weight):
        comp = sorted(comp)
        # self.components[size - 1] is a dictionary for components of size 'size'
        if str(comp) not in self.components[size - 1]:
            self.components[size - 1][str(comp)] = (comp, weight)

    def get_dict_for_size(self, size):
        return self.components[size - 1]

    def get_len_for_size(self, size):
        return len(self.components[size - 1])


# class Vertex holds a vertex attributes
# - tested = 0/1
# - color 0-7
# - score - odds by the algorithm that the vertex is in that color
class Vertex:
    # simple constructor - only initiate object values with the input values
    def __init__(self, vertex_num, color_in, color_score_in, tested, connected_size):
        self.vertex_num = vertex_num
        self.test = tested
        self.color = color_in
        self.colorScore = color_score_in
        self.valid = True
        self.comp_list = ComponentList(connected_size)

    def add_comp(self, size, comp, weight):
        self.comp_list.add_comp(size, comp, weight)

    def get_len_for_size(self, size):
        return self.comp_list.get_len_for_size(size)

    def get_dict_for_size(self, size):
        return self.comp_list.get_dict_for_size(size)

    # print function
    def __str__(self):
        return str(self.vertex_num) + " -tested: " + str(self.test) + "|| color: " + \
               str(self.color) + "|| score: " + str(self.colorScore)

    # print function
    def __repr__(self):
        return str(self.vertex_num) + " -tested: " + str(self.test) + "|| color: " + \
               str(self.color) + "|| score: " + str(self.colorScore)


# class VertexCreator creates new vertices from the following files
# - vertex data file
class VertexCreator:
    # constructor - creating file objects as attributes for each file from input
    def __init__(self, tested_file_name):
        # opening all relevant files
        self.data_file = open(tested_file_name, "r")

    # reads from all files one vertex
    # the file attributes will be promoted to the next vertex on all files
    def get_next_vertex(self, connected_size):
        # expected data line format - <vertex_num> <color> <score> <tested>
        data = self.data_file.readline()
        if data != "":
            data = data.split()
            v = Vertex(data[0], data[1], data[2], data[3], connected_size)
            return v
        return 0

    # the function read all the vertices from the files and returns them in a list
    def get_all(self, connected_size):
        # creating empty list to hold all the vertices
        vertex_list = []
        # loop over all vertices in the files
        vertex_i = self.get_next_vertex(connected_size)
        while vertex_i != 0:
            vertex_list.append(vertex_i)
            vertex_i = self.get_next_vertex(connected_size)
        return vertex_list
