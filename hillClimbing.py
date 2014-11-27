import numpy as np
import branchAndBound as bb
import copy
import time

tabu = []

def hillclimb(G, all_combs, opt_sol):
	curr_soln = list(np.random.permutation(G.nodes()))
	#print "huh " + str(curr_soln)
	curr_cost = bb.find_cost(curr_soln, G)
	maxIter = 1000000
	iterations = 0
	#print curr_cost
	#best_cost = float("inf")
	#best_soln = None
	#tabu.append(curr_soln)

	q = .008 #.8%
	#7733
	while iterations<maxIter:
		#print iterations
		#print "huh2 " + str(curr_soln)
		
		#at each step of "climbing the hill" the algorithm looks in its "neighborhood" of the current solution
		#find_next_soln returns the 'best' soln in the current soln's neighborhood
		temp_cost, next_soln = find_next_soln(curr_soln, G, all_combs)
		#print temp_cost
		#print next_soln

		#ignore for now -- for trace files
		#if temp_cost <= (q*opt_sol) + opt_sol: 
			#print "LOLOLOLOL"

		if temp_cost >= curr_cost:
			return curr_cost,curr_soln #meaning we have reached the "peak"

		curr_cost = temp_cost
		curr_soln = next_soln

		iterations += 1
	#print str(curr_soln)
	return curr_cost,curr_soln

#given a current solution, returns the best solution in its neighborhood
def find_next_soln(curr_soln, G, all_combs):
	#find_successors uses 2opt exchange to return the neighborhood of all possible solutions obtained by reversing some part of the current solutions route
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

#given a current solution, returns a list of the neighborhood of the current solution
#neighborhood is defined as all possible variations of a route where a variation is obtained by reversing part of a route
def find_successors(curr_soln, G, all_combs):
	#given a current solution find its "neighbors"
	#use 2-OPT to find all possible variations of the curr_soln --> find all possible variations of swapping
	successors = []

	n = len(G.nodes()) - 1
	
	#print all_combs
	for (i,j) in all_combs:
		if i<j:
			new_route = []
			new_route[0:i] = copy.deepcopy(curr_soln[0:i])
			new_route[i:j] = list(reversed(curr_soln[i:j]))
			new_route[j:n+1] = copy.deepcopy(curr_soln[j:n+1])
			successors.append(new_route)
	return successors

#hill climbing with restart 
#This method calls hillclimb (above) "num_iter" times -- each time the method returns a locally optimal solution. Calling hillclimb multiple times allows us to not only find a local optimum
#but greatly increases our chances of finding the globally optimal solution. 
def hctour(G, trfilename, opt_sol):
	trfile = open(trfilename, 'w')
	#start_time = time.time()
	num_iter = 50
	iterations = 0

	best_soln = None
	best_cost = float("inf")

	#gets all the possible pairs of nodes (1,2),(1,3),...etc -- used in 2-opt exchange
	all_combs = all_combinations(G)

	#calls hillclimb multiple times to hopefully find optimal solution
	while iterations < num_iter:
		#print "hi" + str(iterations)
		new_cost,new_soln = hillclimb(G, all_combs, opt_sol)
		print new_cost

		#if it finds a better solution than previous solution, reset best solution
		if best_soln is None:
			best_soln = new_soln
			best_cost = new_cost
			#trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
		if new_cost < best_cost:
			best_cost = new_cost
			best_soln = new_soln
			#trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
		iterations += 1

	#makes it a cycle
	best_soln.append(best_soln[0])

	return best_soln, best_cost
