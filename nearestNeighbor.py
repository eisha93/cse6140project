"""
This file runs the nearest neighbor approximation algorithm on a graph input.
It randomly selects a starting node and then performs a nearest neighbor search and selects the 
next vertex in the tour by choosing the closest unvisited node (meaning the node that has the smallest
edge cost to the current node). To improve the performance of the algorithm, instead of only
running the search for one random vertex, it performs a nearest neighbor search from all vertices in the 
graph. It then returns the most optimal tour found and its cost.
"""
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
	"""Given a graph, performs nearest neighbor search as detailed above. Every time a more optimal solution is found it
	is written to the tracefile along with the time at which it was found."""
	trfile = open(trfilename, 'w')
	start_time = time.time()

	best_tour = None
	best_cost = float("inf")

	#runs nearest neighbor using each vertex as a starting point
	for node in G.nodes():
		#keep track of nodes that are not visited and those that are visited (ultimately the tour)
		not_visited = G.nodes()
		visited = [node]
		not_visited.remove(node)
		tour = 0.0

		#while we still have some nodes that are not part of the tour
		while not_visited:
			#finds closest unvisited neighbor to current node
			min_node = min(not_visited, key = lambda u: G.edge[visited[-1]][u]['weight'])
			tour += G.edge[visited[-1]][min_node]['weight']
			visited.append(min_node)
			not_visited.remove(min_node)

		#once we have the entire tour, we need to add the cost to get back to the first node to create the cycle
		tour += G.edge[visited[-1]][visited[0]]['weight'] 
		visited.append(visited[0]) 

		if best_tour is None:
			best_tour = visited
			best_cost = tour
			trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
		if tour < best_cost:
			best_tour = visited
			best_cost = tour
			trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
	
	return best_tour, best_cost



