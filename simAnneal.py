import numpy as np
import branchAndBound as bb
import nearestNeighbor as nn
import copy
import time
import networkx as nx
import random
import math

def simAnneal(G,trfilename, opt_sol, cutoff_time, seed):
	random.seed(seed)
	trfile = open(trfilename, 'w')
	start_time = time.time()
	alpha = .95
	t = 1.0e+20 #lower
	t_end = 0.001
	curr_soln, e = nn.nntour(G, 'fake')
	#print curr_soln
	#curr_soln = list(np.random.permutation(G.nodes()))
	#initializing first solution
	best_soln = curr_soln
	#e = bb.find_cost(curr_soln, G)
	best_cost = e
	trace_cost = e
	all_combs = all_node_combos(G)
	while t > t_end:
		if (time.time()-start_time) >= cutoff_time:
			print 'ran out of time'
			return best_soln, best_cost
		else:
			some_neighbor, energy = find_some_neighbor(curr_soln, G, all_combs)
			if energy < e or P(e, energy, t) > random.random():
				curr_soln = some_neighbor
				best_soln = curr_soln
				e = energy
				best_cost = e
				#print best_cost
				if best_cost < trace_cost:
					trace_cost = best_cost
					trfile.write(str(time.time() - start_time) + ", " + str(best_cost)+"\n")
				#print best_cost
			t = temp(t,alpha)

	best_soln.append(best_soln[0])
	return best_soln, best_cost

def all_node_combos(G):
	all_combos = []
	n = len(G.nodes()) - 1

	for i in range(1,n):
		for j in range(1,n):
			if i<j:
				all_combos.append((i,j))
	#print all_combos
	return all_combos

def find_some_neighbor(curr_soln, G, all_combs):
	neighbors = find_neighbors(curr_soln, G, all_combs)
	k = int(round(.3*len(neighbors),0))
	nays = []
	for n in neighbors:
		rank = bb.find_cost(n, G)
		nays.append((n,rank))
	nays = sorted(nays, key = lambda nb: nb[1])
	#print nays[:k]
	random_n = random.choice(nays[:k])
	r_n = random_n[0]
	cost_n = random_n[1]
	return r_n, cost_n

def find_neighbors(curr_soln, G, all_combs):
	#print all_combs
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

def temp(start_temp,alpha):
	T=start_temp*alpha
	return T

def P(prev_score, next_score, temp):
	if next_score > prev_score:
		return 1.0
	else:
		return math.exp( -abs(next_score-prev_score)/temp)

