#MST APPROX ALGORITHM
import itertools
import time
import networkx as nx
from random import randint

#the 'main' function
def MST_approx_tour(G, trfilename, cutoff_time):
	trfile = open(trfilename, 'w')
	start_time = time.time()
	T = MST(G)
	best_path, best_cost = find_tour(T,G, start_time, trfile, cutoff_time)
	return best_path, best_cost

# finds MST of G
def MST(G):
	return nx.minimum_spanning_tree(G)

#finds tour T* on Eularien graph;
def find_tour(G, oG, start_time, trfile, cutoff_time):
	#use oG because it must be from the original graph's edge's values
	nodes = list(nx.dfs_preorder_nodes(G))
	p_sol = []
	tsum = 0
	for i in range(0, len(nodes)):
		if i < len(nodes)-1:
			if (time.time() - start_time) >= cutoff_time:
				return p_sol, tsum
			else:
				p_sol.append(nodes[i])
				tsum += oG[nodes[i]][nodes[i+1]]['weight']
				trfile.write(str(time.time() - start_time) + ', ' + str(tsum) + '\n')
	return nodes,tsum
