#MST APPROX ALGORITHM
import itertools
import networkx as nx
from random import randint

#the 'main' function
def MST_approx_tour(G):
	#TODO timer start

#	for e in G.edges():

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
	#use oG because it must be from the original graph's edge's values
	nodes = list(nx.dfs_preorder_nodes(G))
	# nodes = [7.0, 6.0, 15.0, 5.0, 11.0, 9.0, 10.0, 16.0, 3.0, 2.0, 4.0, 8.0, 1.0, 13.0, 14.0, 12.0, 7.0]
	print nodes
	tsum = 0
	for i in range(0, len(nodes)):
		if i < len(nodes)-1:
			tsum += oG[nodes[i]][nodes[i+1]]['weight']
		#else:
			#print 'last connection'
			#print oG[nodes[0]][nodes[i]]['weight']
		#print [nodes[i], nodes[i+1]]
		#TODO output time stamp for lution trace output file
		#TODO output current best solution
		#tsum += oG.edge[e_pair[0]][e_pair[1]]['weight']
	#root = edges[0][0]
	#last_n =  edges[len(edges)-1][1]
	#tsum += oG.edge[root][last_n]['weight']
	print 'this is the sum of the edges in the optimal solution'
	print tsum
	return tsum
