import numpy as np
import branchAndBound as bb
import copy
import time
import networkx as nx
import random
import math

def simAnneal(G,move_operator,objective_function,max_evaluations,start_temp,alpha):
# init_function - the function used to create our initial solution
# move_operator - the function we use to iterate over all possible "moves" for a given solution
# objective_function - used to assign a numerical score to a solution - how "good" the solution is

# max_evaluations - used to limit how much search we will perform (how many times we'll call the objective_function)
# start_temp - the initial starting temperature for annealing
# alpha - should be less than one. controls how quickly the temperature reduces
	initial_tour = init_random_tour(len(nx.nodes(G)))

	errorTol = .0001
	start_temp = 0
	root = nx.G(0)
	e = eval(root)
	its = 0
	emin = .0001

	while its < iters and e > errorTol:
		T = temp(k/kmax)
		node = neighbors(s)
		energy = eval(node)
		if P(eVal, energy, T) > random():
			s = node
			eVal = energy
		its++

def neighbors(node):
	#finds neighbor given a node
	neighbor_list = nx.G.all_neighbors(node)
	return random.choice(neighbor_list)

def eval(node):
	#finds the evaluation of the current state
	return

def init_random_tour(tour_length):
   tour=range(tour_length)
   random.shuffle(tour)
   return tour

def temp_cooling(start_temp,alpha):
    T=start_temp
    while True:
        yield T
        T=alpha*T

def P(prev_score, next_score, temp):
	if next_score > prev_score:
        return 1.0
    else:
        return math.exp( -abs(next_score-prev_score)/temperature )

class ObjectiveFunction:
    '''class to wrap an objective function and 
    keep track of the best solution evaluated'''
    def __init__(self,objective_function):
        self.objective_function=objective_function
        self.best=None
        self.best_score=None
    
    def __call__(self,solution):
        score=self.objective_function(solution)
        if self.best is None or score > self.best_score:
            self.best_score=score
            self.best=solution
        return score