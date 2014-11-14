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



