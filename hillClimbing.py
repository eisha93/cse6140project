import numpy as np
import branchAndBound as bb
import copy

tabu = []

def hillclimb(G, all_combs):
	curr_soln = list(np.random.permutation(G.nodes()))
	#print "huh " + str(curr_soln)
	curr_cost = bb.find_cost(curr_soln, G)
	maxIter = 1000
	iterations = 0
	#print curr_cost

	tabu.append(curr_soln)

	while iterations<maxIter:
		#print iterations
		#print "huh2 " + str(curr_soln)
		
		temp_cost, next_soln = find_next_soln(curr_soln, G, all_combs)

		#print next_soln

		#print "huh3 " + str(curr_soln) + " nextsoln " + str(next_soln)
		#temp_cost = bb.find_cost(next_soln)
		if temp_cost >= curr_cost:
			#print "woo" + str(iterations)
			return curr_cost,curr_soln #meaning we have reached the "peak"
		curr_cost = temp_cost
		#print curr_cost
		curr_soln = next_soln

		iterations += 1
	#print str(curr_soln)
	return curr_cost,curr_soln


def find_next_soln(curr_soln, G, all_combs):
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
	all_combos = []
	n = len(G.nodes()) - 1

	for i in range(1,n):
		for j in range(1,n):
			if i<j:
				all_combos.append((i,j))
	return all_combos

def find_successors(curr_soln, G, all_combs):
	#print "calling find successors"
	#given a current solution find its "neighbors"?
	#use 2-OPT to find all possible variations of the curr_soln --> find all possible variations of swapping
	successors = []

	n = len(G.nodes()) - 1
	#print str(bb.find_cost(curr_soln)) + "AOGHOSG"
	
	#print all_combs
	for (i,j) in all_combs:
		if i<j:
			#temp = copy.deepcopy(curr_soln)
			#print "HAI" + str(curr_soln) #+ " " + str(bb.find_cost(curr_soln,G))
			new_route = []
			new_route[0:i] = copy.deepcopy(curr_soln[0:i])
			new_route[i:j] = list(reversed(curr_soln[i:j]))
			new_route[j:n+1] = copy.deepcopy(curr_soln[j:n+1])
			successors.append(new_route)
	return successors


def hctour(G):
	num_iter = 1
	iterations = 0

	best_soln = None
	best_cost = float("inf")

	all_combs = all_combinations(G)

	while iterations < num_iter:
		#print "hi" + str(iterations)
		new_cost,new_soln = hillclimb(G, all_combs)

		if best_soln is None:
			best_soln = new_soln
			best_cost = new_cost
		if new_cost < best_cost:
			best_cost = new_cost
			best_soln = new_soln

		iterations += 1

	best_soln.append(best_soln[0])

	return best_soln, best_cost
