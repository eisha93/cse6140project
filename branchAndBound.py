from __future__ import division
import copy
import time
import numpy as np
import nearestNeighbor as nn
import networkx as nx


def bbtour(G, cutoff_time):
	start_time = time.time()
	i=0
	#best = list(np.random.permutation(G.nodes()))
	#bcost = find_cost(best,G)
	#while i<50:
#		nodes = list(np.random.permutation(G.nodes()))
#		ncost = find_cost(nodes,G)
#		if ncost<bcost:
#			best = nodes
#			bcost = ncost
#		i+=1
	F = [] #list of solutions (a partial solution is a list?)
	#best_cost = find_cost(nodes, G)
	#best_soln = copy.deepcopy(nodes)
	#best_soln.append(nodes[0]) #make it a cycle?
	#best_cost = find_cost(nodes,G)
	#best_soln = copy.deepcopy(nodes)
	#best_soln.append(best_soln[0])
	
	best_soln, best_cost = nn.nntour(G)

	print best_soln
	print best_cost
	#return -1
	#add each node as a "partial" solution to F? as in you want to look at all possible
	#solns for all possible nodes right?
	for node in G.nodes():
		F.append([node])

	first = 1
	rest = 0
	#print "F: "+str(F)
	while F:
		if (time.time() - start_time) >= cutoff_time:
			return best_soln, best_cost
		#choose partial soln in F to expand by lower bound (and remove from F)
		#expand 
		#for each new config
			#check new config, if soln then update best appropriately
			#else add new config to F
		
		#let's try where the first expand picks the "best" out of all the singletons...

		#if first == 1:
			#call choose_lowerbound --> picks partial based off of lower bound
		#	partial_soln = choose(F,G) #choose_lowerbound
		#	if rest == 0:
		#		first = 0
		#lse:
			#call the choose that picks longest partial soln... 
		#	partial_soln = choose(F, G)
		
		partial_soln = choose_lowerbound(F,G)
		#print "WTF " + str(partial_soln)
		#print partial_soln
		F.remove(partial_soln)

		new_configs = expand(partial_soln, G) #do I ever return an empty list
		
		for config in new_configs:
			if (time.time() - start_time) >= cutoff_time:
				return best_soln, best_cost
			#'check' new config
			is_soln = check(config, G)
			if is_soln == 1:
				first = 1
				#rest = 1
				temp = find_cost(config, G)
				
				if temp < best_cost:
					best_soln = copy.deepcopy(config)
					best_soln.append(config[0])
					best_cost = temp #make it a cycle
				return best_cost,best_soln
				#print "best cost is " + str(best_cost) + " size F is " + str(len(F))
				print str(best_soln) + ", " + str(best_cost)
			else:
				if lower_bound_mst(config, G) < best_cost:
					#print "F: " + str(F)
					F.append(config)
					print "lb is " + str(lower_bound_minonetree(config, G)) + " config is " + str(config)
				#else:
					#print best_soln
					#print best_cost
					#return -1
					#print "pruned" + str(config)
	return best_soln, best_cost

def find_cost_min_tree(G):
	#LARGEST of min 1-trees is a decent lower bound...?

	nodes = G.nodes()
	nodes2 = G.nodes()

	best = 0

	#print "nodes :" + str(nodes)
	#print nodes2

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
			#print "nodes: " + str(nodes)
			min_node2 = min(nodes, key = lambda u: G.edge[node][u]['weight'])
			path += G.edge[node][min_node2]['weight']

		nodes.append(min_node)

		nodes.append(node)

		if path > best:
			best = path
		#print path

	return best

def find_cost(config, G):
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
	#need to check that we visit each node in the graph 
	#shouldn't have duplicates because expand should take care of that...
	if config is None:
		print "HELP"
	for node in G.nodes():
		if node not in config:
			return 0
	return 1

def choose_minonetree(F,G):
	best_soln = None
	best_cost = float("inf")
	best_ratio = float("inf")
	#min lb/numnodes

	for soln in F:
		cost = lower_bound_minonetree(soln, G)
		length = len(soln)

		ratio = float(cost/length)
		#print "ratio: " + str(ratio) + ", cost: " + str(cost) + ", len: " + str (length)

		if ratio < best_ratio:
			best_soln = soln
			best_cost = cost
			best_ratio = ratio
	return best_soln



def choose_lowerbound(F, G):
	best = None
	#print "F choose: " + str(F)
	cost = float("inf")

	for soln in F:
		#print "lol"
		#print "soln: " + str(soln)
		temp = lower_bound_mst(soln, G)
		#print str(temp) + "kill me"
		#print "soln2"  + str(soln)
		#if best == None:
		#	lenbest = 0
		#else:
		#	lenbest = len(best)
		#if len(soln) > lenbest:
		#		cost = temp
		#		best = soln

		if temp<cost:
			#print str(soln) + " LOL"
			cost = temp
			best = soln
			#if temp == cost: 
				#if the lower bounds are ==, pick the one with more nodes (more likely to get a solution faster)
			#	if best!=None:
			#		if len(soln) > len(best):
			#else:
			#	cost = temp
			#	best = soln
		
	#print "in choose: " + str(best)
	return best

def lower_bound_minonetree(soln, G):
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

#choose best config in list of partial solns based off of partial solns in F
def choose(F, G):
	best = None
	#print "F choose: " + str(F)
	cost = float("inf")

	for soln in F:
		#print "soln: " + str(soln)
		#temp = lower_bound(soln, G)
		#print "soln2"  + str(soln)
		if best == None:
			lenbest = 0
		else:
			lenbest = len(best)
		if len(soln) > lenbest:
				#cost = temp
				best = soln

		#if temp<=cost:
		#	if temp == cost: 
		#		#if the lower bounds are ==, pick the one with more nodes (more likely to get a solution faster)
		#		if best!=None:
		#			if len(soln) > len(best):
		#				cost = temp
		#				best = soln
		#	else:
		#		cost = temp
		#		best = soln
			#print "whee" + str(best)
	#print "in choose: " + str(best)
	return best

def lower_bound_easy(soln, G):
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

def lower_bound_nn(soln, G):
	count = 0
	path = 0
	all_nodes = G.nodes()
	G_nodes = G.nodes()
	#lower bound = partial path we have
	for node in soln:
		all_nodes.remove(node)
		G_nodes.remove(node)
		if count == 0:
			count = 1
			i = node
			#call choose_lowe
		else:
			path += G.edge[i][node]['weight']
			i = node

	last = soln[-1]

	while all_nodes:
		min_node = min(all_nodes, key=lambda u: G.edge[last][u]['weight'])
		path += G.edge[min_node][last]['weight']
		all_nodes.remove(min_node)
		last = min_node

	return path

def lower_bound_mst(soln, G):
	count = 0
	path = 0
	all_nodes = G.nodes()
	G_nodes = G.nodes()
	#lower bound = partial path we have
	for node in soln:
		all_nodes.remove(node)
		G_nodes.remove(node)
		if count == 0:
			count = 1
			i = node
			#call choose_lowe
		else:
			path += G.edge[i][node]['weight']
			i = node

	#lower bound += exiting a and b	
	#min edge leaving a, to node in V-soln
	min_a = min(all_nodes, key=lambda u: G.edge[soln[0]][u]['weight'])

	#min edge leaving b
	min_b = min(all_nodes, key=lambda u: G.edge[soln[-1]][u]['weight'])

	exit_a = G.edge[soln[0]][min_a]['weight']
	exit_b = G.edge[soln[-1]][min_b]['weight']

	path += 1*(exit_a + exit_b) #lb is now partial soln + lower bound on exiting a and b

	#so all_nodes is now V-soln, find minimum spanning tree of those
	subgraph = G.subgraph(all_nodes)
	mst = nx.minimum_spanning_tree(subgraph)

	for gedge in mst.edges():
		path += G.edge[gedge[0]][gedge[1]]['weight']	

	return path


def lower_bound_take2(soln, G):
	count = 0
	path = 0
	all_nodes = G.nodes()
	G_nodes = G.nodes()
	#lower bound = partial path we have
	for node in soln:
		all_nodes.remove(node)
		G_nodes.remove(node)
		if count == 0:
			count = 1
			i = node
		else:
			path += G.edge[i][node]['weight']
			i = node

	#lower bound += exiting a and b	
	#min edge leaving a, to node in V-soln
	min_a = min(all_nodes, key=lambda u: G.edge[soln[0]][u]['weight'])

	#min edge leaving b
	min_b = min(all_nodes, key=lambda u: G.edge[soln[-1]][u]['weight'])

	exit_a = G.edge[soln[0]][min_a]['weight']
	exit_b = G.edge[soln[-1]][min_b]['weight']

	path += .5*(exit_a + exit_b) #lb is now partial soln + lower bound on exiting a and b

	all_nodes.append(soln[-1])
	all_nodes.append(soln[0]) #add a and b back in

	

	for node in G_nodes:
		all_nodes.remove(node)
		min_node = min(all_nodes, key = lambda u: G.edge[node][u]['weight'])
		path += .5*(G.edge[node][min_node]['weight'])
		all_nodes.remove(min_node)
		min_node2 = min(all_nodes, key = lambda u: G.edge[node][u]['weight'])
		path += .5*(G.edge[node][min_node2]['weight'])
		all_nodes.append(min_node)
		all_nodes.append(node)

	return path


#return lower bound on particular soln if soln is path from a-->T-->b
#lb = (length of path from a-->b) + (sum of min cost of leaving each vertex in V-T-a)
#def lower_bound(soln, G):
#	a = soln[0]
#	b = soln[-1]
#	T = copy.deepcopy(soln)
#	
#	T.remove(a)
#
#	if T!=[]:
#		T.remove(b)
#	
#	#print "T: " + str(T) + ", a: " + str(a) + ", b: " + str(b)
#
#	nodes = G.nodes()
#	all_nodes = G.nodes()
#
#	path = 0
#	count = 0
#	for node in soln:
#		if count == 0:
#			i = node
#			count = 1
#		else:
#			path += G.edge[i][node]['weight']
#			i=node
#
#	for node in T:
#		nodes.remove(node)
#	nodes.remove(a) #now nodes contains V-T-a
#
#	#find sum of min cost of leaving each vertex in V-T-a ('nodes')
#	for node in nodes:
#		#for each of these nodes find min cost of leaving it
#		all_nodes.remove(node)
#		min_node = min(all_nodes, key = lambda u: G.edge[node][u]['weight']) #should this be min cost leaving vertex to ALL other nodes, or only nodes in V-T-a?
#		all_nodes.append(node)
#		path += G.edge[node][min_node]['weight']
#	return path


#expands given config, randomly add vertex?
def expand(config, G):
	temp_config = copy.deepcopy(config)
	new_configs = []
	nodes = list(np.random.permutation(G.nodes()))
	#print "in expand config is " + str(temp_config)
	#first remove all the nodes that are in the partial soln
	for node in temp_config:
		nodes.remove(node)
	#print nodes
	#now for all the nodes create new configs that add one node to the existing partial soln
	#print "HELLO " + str(temp_config)

	for node in nodes:
		#print node
		temp_list = copy.deepcopy(temp_config)
		temp_list.append(node)
		new_configs.append(temp_list)
		#print temp_config

	#print "new configs in expand " + str(new_configs)
	return new_configs


