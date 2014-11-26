import numpy as np
import branchAndBound as bb
import copy
import time
import networkx as nx


def simAnneal(G, iters, ):
	errorTol = .0001
	root = nx.G(0)
	e = eval(root)
	its = 0
	emin = 

	while its < iters and e > errorTol:
		T = temp(k/kmax)
		node = neighbors(s)
		eVal = eval(node)
		if P(eVal, energy, T) > random():
			s = node
			eVal = energy
		its++

def neighbors(node):
	#finds neighbor given a node
	return

def eval(node):
	#finds the evaluation of the current state
	return