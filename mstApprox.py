#MST APPROX ALGORITHM
import itertools
import networkx as nx
from random import randint

#the 'main' function
def MST_approx_tour(G):
	T = MST(G)
	total_edges_cost = find_tour(T,G)
	return total_edges_cost

# finds MST of G
def MST(G):
	return nx.minimum_spanning_tree(G)

#finds tour T* on Eularien graph;
def find_tour(G, oG):
	#use oG because it must be from the original graph's edge's values
	nodes = list(nx.dfs_preorder_nodes(G))
	tsum = 0
	for i in range(0, len(nodes)):
		if i < len(nodes)-1:
			tsum += oG[nodes[i]][nodes[i+1]]['weight']
	return nodes,tsum
