import numpy as np
import branchAndBound as bb
import copy
import time
import networkx as nx
import random
import math

def simAnneal(G,trfilename, opt_sol):
	trfile = open(trfilename, 'w')
	num_iter = 200
	iterations = 0
	alpha = .99
	t = 1.0e+300
	t_end = 0.001
	emin = opt_sol 
	curr_soln = list(np.random.permutation(G.nodes()))
	#initializing first solution
	best_soln = curr_soln
	e = bb.find_cost(curr_soln, G)
	best_cost = e
	all_combs = all_node_combos(G)

	while iterations < num_iter and t > t_end:
		#alpha = iterations/num_iter
		t = temp(t,alpha)
		some_neighbor = find_some_neighbor(curr_soln, G, all_combs)
		energy = bb.find_cost(some_neighbor, G)
		if energy > e or P(e, energy, t) > random.random():
			curr_soln = some_neighbor
			best_soln = curr_soln
			e = energy
			best_cost = e
		iterations+= 1

	best_soln.append(best_soln[0])
	return best_soln, best_cost

def all_node_combos(G):
	all_combos = []
	n = len(G.nodes()) - 1

	for i in range(1,n):
		for j in range(1,n):
			if i<j:
				all_combos.append((i,j))
	return all_combos

def find_some_neighbor(curr_soln, G, all_combs):
	neighbors = find_neighbors(curr_soln, G, all_combs)
	return random.choice(neighbors)

def find_neighbors(curr_soln, G, all_combs):
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

