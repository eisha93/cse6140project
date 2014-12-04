"""This file performs a hill climbing iterated local search on the given input graph."""
import numpy as np
import branchAndBound as bb
import copy
import time
import random
tabu = []

#hill climbing with restart 
#This method calls hillclimb (above) "num_iter" times -- each time the method returns a locally optimal solution. Calling hillclimb multiple times allows us to not only find a local optimum
#but greatly increases our chances of finding the globally optimal solution. 
def hctour(G, trfilename, opt_sol, cutoff_time, seed):
	"""Hill climbing with restart - calls hillclimb() 'num_iter' times, each time the method returns a locally optimal solution. Since we call hillclimb() multiple times, we
	greatly increase our chances of finding the globally optimal solution."""
	trfile = open(trfilename, 'w')
	start_time = time.time()
	num_iter = 50
	iterations = 0

	best_soln = None
	best_cost = float("inf")

	#gets all the possible pairs of nodes (1,2),(1,3) -- used in 2-opt exchange
	all_combs = all_combinations(G)
	curr_best_sol = best_soln

	#calls hillclimb multiple times to find globally optimal solution
	while iterations < num_iter:
		if (time.time()-start_time) >= cutoff_time:
			return best_soln, best_cost, 'no'

		new_cost,new_soln= hillclimb(G, all_combs, opt_sol, cutoff_time, start_time, trfile, best_cost, seed)

		#if it finds a better solution than previous solution, reset best solution
		if best_soln is None:
			best_soln = new_soln
			best_cost = new_cost
		if new_cost < best_cost:
			best_cost = new_cost
			best_soln = new_soln
		iterations += 1

	#makes it a cycle
	best_soln.append(best_soln[0])

	return best_soln, best_cost

def hillclimb(G, all_combs, opt_sol, cutoff_time, start_time, trfile, curr_best_sol, seed):
	"""Performs actual hill climbing to find most likely what will be a locally optimal solution, given a random initial solution."""
	random.seed(seed)
	curr_soln = list(np.random.permutation(G.nodes()))
	curr_cost = bb.find_cost(curr_soln, G)
	maxIter = 5000
	iterations = 0
	
	while iterations<maxIter:
		if (time.time() - start_time) >= cutoff_time:
			return curr_cost,curr_soln

		#at each step of "climbing the hill" the algorithm looks in its "neighborhood" of the current solution; find_next_soln returns the 'best' soln in the current soln's neighborhood
		temp_cost, next_soln = find_next_soln(curr_soln, G, all_combs)

		if temp_cost >= curr_cost:
			return curr_cost,curr_soln #meaning we have reached the "peak" in the space of all solutions

		curr_cost = temp_cost
		curr_soln = next_soln

		if curr_cost < curr_best_sol:
			trfile.write(str(time.time() - start_time) + ", " + str(curr_cost)+"\n")
			curr_best_sol = curr_cost
		iterations += 1
	return curr_cost,curr_soln

def find_next_soln(curr_soln, G, all_combs):
	"""Given a current solution, returns the best solution in its neighborhood. Uses find_successors() which performs a 2-opt exchange to return neighborhood of all possible
	solutions obtained by reversing some part of the current solution's route."""
	successors = find_successors(curr_soln, G, all_combs)
	best_soln = None
	best_cost = float("inf")

	for soln in successors:
		#evaluate each, see which one is best
		soln_cost = bb.find_cost(soln, G)
		if best_soln is None:
			best_soln = soln
			best_cost = soln_cost
		if soln_cost < best_cost:
			best_soln = soln
			best_cost = soln_cost
	return best_cost,best_soln

def all_combinations(G):
	"""Returns all possible pairings of nodes. Used in 2-opt exchange."""
	all_combos = []
	n = len(G.nodes()) - 1

	for i in range(1,n):
		for j in range(1,n):
			if i<j:
				all_combos.append((i,j))
	return all_combos

def find_successors(curr_soln, G, all_combs):
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


