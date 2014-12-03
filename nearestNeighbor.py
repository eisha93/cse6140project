import itertools
from random import randint
import time

#s = random vertex v
#while not all vertices visited
	#select closest unvisited neighbor
	#go from v to w (add cost)
	#v = w
#go from v to s

#do we need to iterate through all possible nn tours? 
#as in, start at each node and find its nn tour and then find the min of all of those...?
def nntour(G, trfilename):
	trfile = open(trfilename, 'w')
	start_time = time.time()

	best_tour = None
	best_cost = float("inf")

	#dict = {}
	for node in G.nodes():
		#print node
		not_visited = G.nodes()
		visited = [node]
		not_visited.remove(node)
		tour = 0.0

		while not_visited:
			min_node = min(not_visited, key = lambda u: G.edge[visited[-1]][u]['weight'])
			tour += G.edge[visited[-1]][min_node]['weight']
			visited.append(min_node)
			not_visited.remove(min_node)
		tour += G.edge[visited[-1]][visited[0]]['weight'] #add the cost to get back to the beginning cuz its a cycleeee
		visited.append(visited[0]) #make it a cycle????

		if best_tour is None:
			best_tour = visited
			best_cost = tour
			trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
		if tour < best_cost:
			best_tour = visited
			best_cost = tour
			trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
		#dict[tour] = visited
	#print dict
	#min_cost = min(dict)
	#min_tour = dict[min_cost]
	#return min_tour, min_cost
	return best_tour, best_cost



