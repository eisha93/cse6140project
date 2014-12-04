"""This file performs the branch and bound algorithm on a given input graph."""
from __future__ import division
import copy
import time
import numpy as np
import nearestNeighbor as nn
import networkx as nx


def bbtour(G, cutoff_time, trfilename):
	"""Main method to execute branch and bound. Trace files are written to every time a better solution is found."""
	trfile = open(trfilename, 'w')
	start_time = time.time()

	#frontier set of partial solutions
	F = [] 
	
	#start with initial best as nearest neighbor approximation
	best_soln, best_cost = nn.nntour(G, 'random.txt')

	trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")

	
	#add each node as a 'partial' solution to F (essentially we want to look at all possible solutions so we need to start with all possible starting points)
	for node in G.nodes():
		F.append([node])

	#while we still have some partial solutions to check, we iterate continuously
	while F:
		#however if we run past the given cutoff time, we terminate and return the current best solution
		if (time.time() - start_time) >= cutoff_time:
			return best_soln, best_cost
		
		#many choose/lower bound functions were implemented; here we take the choose that chooses based off of partial solution length so that we get any partial solution in a reasonable amount of time
		choose = choose_length
		lower_bound = lower_bound_easy

		partial_soln = choose(F,G)
		F.remove(partial_soln)

		new_configs = expand(partial_soln, G) 

		#check each new partial solution after expanding
		for config in new_configs:
			if (time.time() - start_time) >= cutoff_time:
				return best_soln, best_cost

			is_soln = check(config, G)

			#if the new configuration is a full solution (all nodes), we check it against the current best solution
			if is_soln == 1:
				temp = find_cost(config, G)
				if temp < best_cost:
					best_soln = copy.deepcopy(config)
					best_soln.append(config[0])
					best_cost = temp #make it a cycle
					trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")

			#else we check its lower bound
			else:
				#if the lower bound is less than the current best solution we add it to the set F of partial solutions, else we prune
				if lower_bound(config, G) < best_cost:
					F.append(config)
	return best_soln, best_cost

def find_cost_min_tree(G):
	"""Given a subgraph, finds the cost of the min-1-tree."""
	nodes = G.nodes()
	nodes2 = G.nodes()

	for node in nodes2:
		path = 0
		nodes.remove(node)
		sub_graph = G.subgraph(nodes)
		mst = nx.minimum_spanning_tree(sub_graph)

		for gedge in mst.edges():
			path += G.edge[gedge[0]][gedge[1]]['weight']

		min_node = min(nodes, key = lambda u: G.edge[node][u]['weight'])
		path += G.edge[node][min_node]['weight']
		nodes.remove(min_node)

		if nodes!=[]:
			min_node2 = min(nodes, key = lambda u: G.edge[node][u]['weight'])
			path += G.edge[node][min_node2]['weight']

		nodes.append(min_node)
		nodes.append(node)

	return path

def find_cost(config, G):
	"""Given a solution, finds the cost of it (sum of all edges in between all nodes)."""
	count = 0
	path = 0
	for node in config:
		if count == 0:
			count = 1
			i = node
		else:
			path += G.edge[node][i]['weight']
			i = node
	path += G.edge[config[0]][config[-1]]['weight'] #make it a cycle
	return path

def check(config, G):
	"""Given a possible solution, checks if it is a complete/feasible solution, essentially that we visit all nodes in the graph."""
	if config is None:
		return 0
	for node in G.nodes():
		if node not in config:
			return 0
	return 1

def choose_minonetree(F,G):
	"""Chooses next partial solution to expand based off of a ratio of the minimum spanning tree bound and length of partial solution."""
	best_soln = None
	best_cost = float("inf")
	best_ratio = float("inf")

	for soln in F:
		cost = lower_bound_minonetree(soln, G)
		length = len(soln)

		ratio = float(cost/length)

		if ratio < best_ratio:
			best_soln = soln
			best_cost = cost
			best_ratio = ratio
	return best_soln

def lower_bound_minonetree(soln, G):
	"""Calculates a lower bound for the partial solution based off of its min-1-tree lower bound."""
	count = 0
	path = 0
	all_nodes = G.nodes()

	for node in soln:
		all_nodes.remove(node)
		if count == 0:
			count = 1
			i = node
		else:
			path += G.edge[i][node]['weight']
			i = node
	all_nodes.append(soln[-1])

	subgraph = G.subgraph(all_nodes)
	path += find_cost_min_tree(subgraph)

	return path

def choose_length(F, G):
	"""Choose best configuration in list of partial solutions based off of length partial solns in F."""
	best = None
	cost = float("inf")

	for soln in F:
		if best == None:
			lenbest = 0
		else:
			lenbest = len(best)
		if len(soln) > lenbest:
				best = soln

	return best

def lower_bound_easy(soln, G):
	"""Calculates lower bound based off of cost of existing path plus the minimum edge from every remaining node."""
	count = 0
	path = 0
	all_nodes = G.nodes()

	for node in soln:
		all_nodes.remove(node)
		if count == 0:
			count = 1
			i = node
		else:
			path += G.edge[i][node]['weight']
			i = node
	all_nodes.append(soln[-1])

	G_nodes = copy.deepcopy(all_nodes)

	for node in all_nodes:
		G_nodes.remove(node)
		min_node = min(G_nodes, key = lambda u: G.edge[node][u]['weight'])
		path += G.edge[node][min_node]['weight']
		G_nodes.append(node)

	return path

def lower_bound_mst(soln, G):
	"""Calculates lower bound based off of minimum spanning tree lower bound."""
	count = 0
	path = 0
	all_nodes = G.nodes()
	G_nodes = G.nodes()
	
	#first calculate cost of all nodes in current partial solution
	for node in soln:
		all_nodes.remove(node)
		G_nodes.remove(node)
		if count == 0:
			count = 1
			i = node
		else:
			path += G.edge[i][node]['weight']
			i = node

	#add cost to exit starting node and ending node in partial solution
	min_a = min(all_nodes, key=lambda u: G.edge[soln[0]][u]['weight'])
	min_b = min(all_nodes, key=lambda u: G.edge[soln[-1]][u]['weight'])

	exit_a = G.edge[soln[0]][min_a]['weight']
	exit_b = G.edge[soln[-1]][min_b]['weight']

	path += exit_a + exit_b

	#finds minimum spanning tree of nodes remaining in graph not in partial solution
	subgraph = G.subgraph(all_nodes)
	mst = nx.minimum_spanning_tree(subgraph)

	#adds cost of edges in minimum spanning tree
	for gedge in mst.edges():
		path += G.edge[gedge[0]][gedge[1]]['weight']	

	return path

def expand(config, G):
	"""Given current partial solution (config) returns set of expanded partial solutions by appending remaining vertices one by one to create each new partial solution."""
	temp_config = copy.deepcopy(config)
	new_configs = []
	nodes = list(np.random.permutation(G.nodes()))

	for node in temp_config:
		nodes.remove(node)

	for node in nodes:
		#print node
		temp_list = copy.deepcopy(temp_config)
		temp_list.append(node)
		new_configs.append(temp_list)

	return new_configs


