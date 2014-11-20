#MST APPROX ALGORITHM
import itertools
import networkx as nx
from random import randint

#the 'main' function
def MST_approx_tour(G):
	#TODO timer start
	best_sol = None
	vertices_list = None

	T = MST(G)
	total_edges_cost = find_tour(T,G)

	#TODO timer end
	#TODO output solution file!! mk .txt file

	return total_edges_cost

# finds MST of G
def MST(G):
	return nx.minimum_spanning_tree(G)

#finds tour T* on Eularien graph;
def find_tour(G, oG):
	edges = list(nx.dfs_edges(G))
	tsum = 0
	for e_pair in edges:
		tsum += oG.edge[e_pair[0]][e_pair[1]]['weight']
	root = edges[0][0]
	last_n =  edges[len(edges)-1][1]
	#use oG because it must be from the original graph's edge values
	tsum += oG.edge[root][last_n]['weight']
	print 'this is the sum of the edges in the optimal solution'
	print tsum
	return tsum
