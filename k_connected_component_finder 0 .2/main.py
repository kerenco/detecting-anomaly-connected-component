########################################################################################################################
# Oved Nagar 7.12.17                                                                                                   #
########################################################################################################################

import CcAlgorithm as cc

k = input("number of components ")
eps = input("sum limit ")

cAlgo = cc.ConnectedAlgorithm("data set 5/data_set_edge_5", "data set 5/data_set_data_5", float(eps), int(k))
G = cAlgo.get_graph()
cAlgo.go()
cAlgo.print_good_components()




b = 0
