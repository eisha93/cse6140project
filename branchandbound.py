import copy
import time

def bbtour(G, cutoff_time):
	start_time = time.time()
	nodes = G.nodes()
	F = [] #list of solutions (a partial solution is a list?)
	#best_cost = find_cost(nodes, G)
	#best_soln = copy.deepcopy(nodes)
	#best_soln.append(nodes[0]) #make it a cycle?
	best_cost = float("inf")
	best_soln = None
	print best_cost

	#add each node as a "partial" solution to F? as in you want to look at all possible
	#solns for all possible nodes right?
	for node in nodes:
		F.append([node])

	#print "F: "+str(F)
	while F:
		if (time.time() - start_time)/60 >= cutoff_time:
			return best_soln, best_cost
		#choose partial soln in F to expand by lower bound (and remove from F)
		#expand 
		#for each new config
			#check new config, if soln then update best appropriately
			#else add new config to F
		#print "before choose"
		partial_soln = choose(F, G)
		#print "partial soln: " + str(partial_soln)
		F.remove(partial_soln)
		#print "before expand"
		new_configs = expand(partial_soln, G) #what happens when i return an empty list
		#print "new configs: " + str(new_configs)
		for config in new_configs:
			if (time.time() - start_time)/60 >= cutoff_time:
				return best_soln, best_cost
			#'check' new config
			is_soln = check(config, G)
			if is_soln == 1:
				#return ["BLAH"],-1
				temp = find_cost(config, G)
				#print "before temp cost: " + str(temp) + ", best cost: " + str(best_cost)
				if temp < best_cost:
					best_soln = copy.deepcopy(config)
					best_soln.append(config[0])
					best_cost = temp #make it a cycle
				#print "after temp cost: " + str(temp) + ", best cost: " + str(best_cost)
				print "best cost is " + str(best_cost) + " and soln is " + str(best_soln)
				#assert(False)
				#print "heyyyy " + str(best_cost)
			else:
				if lower_bound(config, G) < best_cost:
					#print "F: " + str(F)
					F.append(config)
	return best_soln, best_cost

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


#choose best config in list of partial solns based off of partial solns in F
def choose(F, G):
	best = None
	#print "F choose: " + str(F)
	cost = float("inf")

	for soln in F:
		#print "soln: " + str(soln)
		temp = lower_bound(soln, G)
		#print "soln2"  + str(soln)
		if best == None:
			lenbest = 0
		else:
			lenbest = len(best)
		if len(soln) > lenbest:
				cost = temp
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

def lower_bound(soln, G):
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
	nodes = G.nodes()
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


