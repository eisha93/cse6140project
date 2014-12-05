#SIMULATED ANNEALING LOCAL SEARCH ALGORITHM
"""This file performs a SIMULATED ANNEALING iterated local search on the given input graph."""
import numpy as np
import branchAndBound as bb
import nearestNeighbor as nn
import copy
import time
import networkx as nx
import random
import math

def simAnneal(G,trfilename, opt_sol, cutoff_time, seed):
	"""Returns the best solution and best cost on a input graph for a specified starting and ending temperature with alpha cooling factor set to .85. """
	random.seed(seed)
	trfile = open(trfilename, 'w')
	start_time = time.time()
	alpha = .85
	t = 1.0e+10 #lower
	t_end = 0.001
	curr_soln, e = nn.nntour(G, 'fake')

	#initializing first solution
	best_soln = curr_soln
	best_cost = e
	trace_cost = e
	trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")

	all_combs = all_node_combos(G)
	while t > t_end:
		if (time.time()-start_time) >= cutoff_time:
			return best_soln, best_cost
		else:
			some_neighbor, n_cost = find_some_neighbor(curr_soln, G, all_combs)
			if n_cost < e or P(e, n_cost, t) > random.random():
				curr_soln = some_neighbor
				best_soln = curr_soln
				e = n_cost
				best_cost = e
				if best_cost < trace_cost: # updates the trace file with the next best cost
					trace_cost = best_cost
					trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
			t = temp(t,alpha)

	best_soln.append(best_soln[0])
	return best_soln, best_cost


#finds all combinations of each edge and two vertices.
def all_node_combos(G):
	"""Returns all possible pairings of nodes. Used in 2-opt exchange."""
	all_combos = []
	n = len(G.nodes()) - 1

	for i in range(1,n):
		for j in range(1,n):
			if i<j:
				all_combos.append((i,j))
	return all_combos

def find_some_neighbor(curr_soln, G, all_combs):
	"""Finds a random neighbor from the best k neighbors in the entire sorted neighborhood from best cost to worst cost."""
	neighbors = find_neighbors(curr_soln, G, all_combs)
	nays = {}
	for n in neighbors:
		rank = bb.find_cost(n, G)
		if rank not in nays:
			nays[rank] = n
	keylist = nays.keys()
	#defines k to be the top 5 percent of the current solution's neighbors in its neighborhood.
	k = int(round(.03*len(keylist),0))
	keylist = sorted(keylist)
	random_n = random.choice(keylist[:k]) #randomly chooses a neighbor from the top 5 percent
	r_n = nays[random_n]
	cost_n = random_n
	return r_n, cost_n

def find_neighbors(curr_soln, G, all_combs):
	#given a current solution find its "neighbors"
	#use 2-OPT to find all possible variations of the curr_soln --> find all possible variations of swapping
	"""Given a current solution, returns a list of the neighborhood of the current solution, where a neighborhood 
	is defined as all possible variations of a route (variation is obtained by reversing part of a route using 2-opt exchange)."""
	successors = []
	n = len(G.nodes()) - 1
	for (i,j) in all_combs:
		if i<j:
			new_route = []
			new_route[0:i] = copy.deepcopy(curr_soln[0:i])
			new_route[i:j] = list(reversed(curr_soln[i:j]))
			new_route[j:n+1] = copy.deepcopy(curr_soln[j:n+1])
			successors.append(new_route)
	return successors

def temp(start_temp,alpha):
	"""Updates the Temperature by mulitplying itself by alpha when called"""
	T=start_temp*alpha
	return T

def P(prev_score, next_score, temp):
	"""Reuturns a probability of accepting a worse solution based off the current temperature value"""
	return math.exp( -abs(next_score-prev_score)/temp)

