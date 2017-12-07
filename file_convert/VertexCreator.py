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
            self.components[i] = []
        self.weights = [None] * connected_size
        for i in range(0, connected_size):
            self.weights[i] = []

    def add_comp(self, size, comp, weight):
        to_add = []
        to_add.append(sorted(comp))
        to_add.append(weight)
        if to_add not in self.components[size - 1]:
            self.components[size - 1].append(comp)
            self.weights[size - 1].append(weight)

    def get_len_for_size(self, size):
        return len(self.components[size - 1])

    def get_comp(self, size, index):
        if len(self.components[size - 1]) < index:
            print('Out Of Range')
        else:
            return [self.components[size - 1][index], self.weights[size - 1][index]]


# class Vertex holds a vertex attributes
# - tested = true/false
# - color 0-7
# - score - odds by the algorithm that the vertex is in that color
class Vertex:
    # simple constructor - only initiate object values with the input values
    def __init__(self, tested, color_in, color_score_in):
        self.test = tested
        self.color = color_in
        self.colorScore = color_score_in
        self.valid = True
        self.comp_list = ComponentList(0)

    def add_comp(self, size, comp, weight):
        self.comp_list.add_comp(size, comp, weight)

    def get_len_for_size(self, size):
        return self.comp_list.get_len_for_size(size)

    def get_comp(self, size, index):
        return self.comp_list.get_comp(size, index)

    # print function
    def __str__(self):
        return "tested: " + str(self.test) + "|| color: " + str(self.color) + "|| score: " + str(self.colorScore)

    # print function
    def __repr__(self):
        return "tested: " + str(self.test) + "|| color: " + str(self.color) + "|| score: " + str(self.colorScore)


# class VertexCreator creates new vertices from the following files
# - tested file - test_mask.txt
# - labels file - lables.txt
# - scores file - preds.txt
class VertexCreator:
    # constructor - creating file objects as attributes for each file from input
    def __init__(self, tested_file_name, label_file_name, score_file_name):
        # opening all relevant files
        self.tested_file = open(tested_file_name, "r")
        self.label_file = open(label_file_name, "r")
        self.score_file = open(score_file_name, "r")

    # reads from all files one vertex
    # the file attributes will be promoted to the next vertex on all files
    def get_next_vertex(self):
        # checking if the i-th vertex was tested or not

        t = self.tested_file.readline()
        if t == "":
            return 0
        if t == "True\n":
            tested = 1
        else:
            tested = 0

        # get color for the i-th vertex
        label = self.label_file.readline()
        label = label.replace(']', " ", 1)
        label = label.replace('[', " ", 1)
        label = label.split()
        i = color = 0
        for i in range(0, 7):
            if label[i] == '1':
                color = i
                break

        # getting row of scores from the file for the i-th vertex
        curr_score = self.score_file.readline() + self.score_file.readline()
        # clean string
        curr_score = curr_score.replace(']', " ", 1)
        curr_score = curr_score.replace('[', " ", 1)
        curr_score = curr_score.split()
        color_score = float(curr_score[i])
        v = Vertex(tested, color, color_score)
        return v

    # the function read all the vertices from the files and returns them in a list
    def get_all(self):
        # creating empty list to hold all the vertices
        vertex_list = []
        # loop over all vertices in the files
        vertex_i = self.get_next_vertex()
        while vertex_i != 0:
            # get next will return 1 if score > epsilon, in that case the program skips to the next vertex
            if vertex_i != 1:
                # adding vertex to the list
                vertex_list.append(vertex_i)
            vertex_i = self.get_next_vertex()
        return vertex_list
