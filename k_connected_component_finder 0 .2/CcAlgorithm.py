########################################################################################################################
# Algorithm: give for every vertex v the component withe k vertices and sum under T that includes the vertex v         #
# In every step we find for every v_i in V the all the connected components with sum under T and with n vertices       #
# (I will refer it as Si_n).                                                                                           #
#                                                                                                                      #
# step 1 - for every v_i in V -  Si_1_1 = {v_i} --              only ome component                                     #
# step 2 - Si_2_j = Si_1 + (v_j reachable from Si_1_1){Sj_1_1} --   may be more then one - delete duplicate components #
# .                                                                                                                    #
# .                                                                                                                    #
# step n - Si_n_j = (l = 1..n-1){Si_l_k + (v_j reachable from Si_l_k){Sj_n-l}                                          #
########################################################################################################################

import GraphCreator as gc
import networkx as nx


class ConnectedAlgorithm:
    def __init__(self, edges_file_name, data_file_name, epsilon, connected_size):
        creator = gc.GraphCreator(edges_file_name, data_file_name, connected_size)
        self.G = creator.get_graph()
        self.eps = epsilon
        self.connected_size = connected_size

    def print_good_components(self):
        all_comp = {}
        count = 0
        for v in self.G:
            node = self.G.node[v]['data']
            if node.valid:
                node_comps = node.get_dict_for_size(self.connected_size)
                for key, value in node_comps.items():
                    if key not in all_comp:
                        count += 1
                        all_comp[key] = value

        for key, val in all_comp.items():
            weights_u = []
            for u in all_comp[key][0]:
                u = self.G.node[u]['data']
                weights_u.append(u.colorScore)
            print("component:\t" + all_comp[key][0].__str__())
            print("sum:\t\t" + weights_u.__str__() + " = " + str(all_comp[key][1])
                  + "\n--------------------------------------------------------------\n")
        print ("number of components:\t" + str(count))

    def get_graph(self):
        return self.G

    def get_reachable(self, comp):
        reachable = []
        for node in comp:
            # iterate over all reachable and add if its not already in the neighbors/comp_i
            for node_u in nx.all_neighbors(self.G, node):
                if self.G.node[node_u]['data'].valid and int(node_u) not in reachable and int(node_u) not in comp:
                    reachable.append(int(node_u))
        return reachable

    def get_reachable_comp_list(self, size, reachable):
        # loop over reachable nodes from some vertex
        comp_with_u = {}
        for node_u in reachable:
            u = self.G.node[node_u]['data']
            dict_comp_u = u.get_dict_for_size(size)
            # get components with requested size
            for key, value in dict_comp_u.items():
                if key not in comp_with_u:
                    comp_with_u[key] = value
        return comp_with_u

    def go(self):
        # first initialization for k = 1
        for i in self.G:
            v = self.G.node[i]['data']
            if float(v.colorScore) > self.eps or v.test == 0:
                v.valid = False
            else:
                v.add_comp(1, [i], v.colorScore)
                y = 0

        # first loop for recursive building of the components starting from components of size 1 going up until size = k
        for main_component_size in range(2, self.connected_size + 1):
            # print progress
            progress = (main_component_size-1)*(100 / self.connected_size)
            print('processing...' + str(int(progress)) + "%")

            # second loop iterates over all vertices
            for vertex in self.G:
                v = self.G.node[vertex]['data']
                # valid vertex is a vertex that can be in a CC withe k vertices withe weight under eps
                if not v.valid:
                    continue
                # third loop iterates over a specific vertex list of components under size = t
                for v_comp_size in range(1, main_component_size):
                    # main_component_size is the size of the component we need to compute in that iteration for all
                    # vertices, v_comp_size is the the size of the component we wish to extend
                    # there for we need the components C_j that hold u and holds the following conditions
                    # - the size of C_j + curr_iter_size = component_size
                    # - C_j doesnt share vertices with comp_i

                    dict_comp_v = v.get_dict_for_size(v_comp_size)

                    for key, value in dict_comp_v.items():
                        comp_i = value[0]
                        weight_comp_i = value[1]
                        reachable_comp_size = main_component_size - v_comp_size
                        # get all reachable nodes
                        reachable_nodes = self.get_reachable(comp_i)
                        # get all reachable components
                        # the return list will contain components followed by the weight
                        reachable_comp = self.get_reachable_comp_list(reachable_comp_size, reachable_nodes)
                        for ky, comp in reachable_comp.items():
                            comp_u = comp[0]
                            comp_u_weight = comp[1]
                            if (float(comp_u_weight) + float(weight_comp_i)) > self.eps:
                                continue
                            shared = False
                            for c_node in comp_u:
                                if comp_i.__contains__(int(c_node)):
                                    shared = True
                                    break

                            if not shared:
                                new_comp = comp_i + comp_u
                                new_comp_weight = float(weight_comp_i) + float(comp_u_weight)
                                v.add_comp(main_component_size, new_comp, new_comp_weight)

                # if there is no component of size k that answer the conditions then there is
                # also no component of size k+1
                if v.get_len_for_size(main_component_size) == 0:
                    v.valid = False
        # print progress
        print("processing...100%\n\n--------------------------------------------------------------")

