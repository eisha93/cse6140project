#MST APPROX ALGORITHM
import itertools
import time
import networkx as nx
from random import randint

#the 'main' function
def MST_approx_tour(G, trfilename):
	trfile = open(trfilename, 'w')
	start_time = time.time()
	T = MST(G)
	best_path, best_cost = find_tour(T,G, start_time, trfile)
	return best_path, best_cost

# finds MST of G
def MST(G):
	return nx.minimum_spanning_tree(G)

#finds tour T* on Eularien graph;
def find_tour(G, oG, sTime, trfile):
	#use oG because it must be from the original graph's edge's values
	nodes = list(nx.dfs_preorder_nodes(G))
	tsum = 0
	for i in range(0, len(nodes)):
		if i < len(nodes)-1:
			tsum += oG[nodes[i]][nodes[i+1]]['weight']
			trfile.write(str(time.time() - sTime) + ', ' + str(tsum) + '\n')
	return nodes,tsum
