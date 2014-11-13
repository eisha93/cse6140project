#MST APPROX ALGORITHM
import itertools
import networkx as nx
from random import randint

#the 'main' function
def MST_approx_tour(G):
	T = MST(G)
	T = double_edges(T)
	T_prime = find_tour(T)
	C = tour(T_prime)
	return C

# finds MST of G
def MST(G):
	return nx.minimum_spanning_tree(G)
#double every edge of MST to obtain an Eularien graph
def double_edges(G):
	G.add_edges_from(nx.edges(G))
	#check edges are actutally doubled

#finds tour T* on Eularien graph;
def find_eulerian_tour(G):
	if nx.is_eulerian(G):

	else:
		print 'the graph G is not Eularian'

# outputs tour that visits vertices of G in the order of their first appearance in T*
def tour(G):
