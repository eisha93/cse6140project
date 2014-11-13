import itertools
from random import randint

#s = random vertex v
#while not all vertices visited
	#select closest unvisited neighbor
	#go from v to w (add cost)
	#v = w
#go from v to s

#do we need to iterate through all possible nn tours? 
#as in, start at each node and find its nn tour and then find the min of all of those...?
def nntour(G):

	#why don't you work OH BUT YOU DO

	dict = {}
	for node in G.nodes():
		#print node
		not_visited = G.nodes()
		visited = [node]
		not_visited.remove(node)
		tour = 0.0

		while not_visited:
			min_node = min(not_visited, key = lambda u: G.edge[visited[-1]][u]['weight'])
			tour += G.edge[visited[-1]][min_node]['weight']
			assert(G.edge[visited[-1]][min_node]['weight'] > 0)
			#if node == 3:
				#print "adding" + str(G.edge[visited[-1]][min_node]['weight'])
			visited.append(min_node)
			assert(min_node in visited)
			not_visited.remove(min_node)
			assert(min_node not in not_visited)
		tour += G.edge[visited[-1]][visited[0]]['weight'] #add the cost to get back to the beginning cuz its a cycleeee
		visited.append(visited[0]) #make it a cycle????

		dict[tour] = visited
	#print dict
	min_cost = min(dict)
	min_tour = dict[min_cost]
	return min_tour, min_cost

def inordertour(G):
	tour = 0
	count = 0

	for node in G.nodes():
		if count == 0:
			i = node
			count = 1
		else:
			count = 1
			tour += G.edge[i][node]['weight']
			i = node
	return tour

def backwardstour(G):
	tour = 0
	count = 0
	G.nodes().reverse()

	for node in G.nodes():
		if count == 0:
			i = node
			count = 1
		else:
			count = 1
			tour += G.edge[i][node]['weight']
			i = node
	return tour

def randtour(G):
	
	tour = 10000
	while tour > 6000:
		tour = 0
		num_nodes = len(G.nodes())
		not_visited = G.nodes()
		node = randint(1,num_nodes)
		visited = [node]
		not_visited.remove(node)
		while not_visited:
			node = randint(1,num_nodes)
			while node in visited:
				node = randint(1, num_nodes)
			tour += G.edge[visited[-1]][node]['weight']
			visited.append(node)
			not_visited.remove(node)
	return tour

def ugh(G):
	blah = [3.0, 2.0, 4.0, 8.0, 1.0, 16.0, 13.0, 12.0, 7.0, 6.0, 15.0, 14.0, 10.0, 9.0, 5.0, 11.0]
	tour = 0
	count = 0
	for node in blah:
		if count == 0:
			count = 1
			i = node
		else:
			tour += G.edge[i][node]['weight']
			print "added weight of edge from " + str(i) + " to " + str(node) + ", " + str(G.edge[i][node]['weight'])
			i = node
	return tour


