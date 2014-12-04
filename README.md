cse6140project
==============

Created for CSE6140: Algorithms, final class project. Fall 2014. Georgia Institute of Technology.

The executable can be run as such:

python run_tsp.py 'filename' 'cutofftime' 'algorithm' 'randomseed'

	<filename> is the direct path to any input file, for example: burma14.tsp,

	<cutofftime> is the time in seconds after which the program should stop running if it hasn't already,

	<algorithm> is one of 'branch_and_bound', 'nearest_neighbor', 'mst_approx', 'hill_climbing', 'simulated_annealing',

	<randomseed> is a random seed given to initialize the random number generator for the local search algorithms.

Calling the execuatable as above will create two files: a solution file which prints simply the most optimal tour and cost found, and a trace
file which has a trace of all solutions found in increasingly optimal order.

All input files must be in the same folder as the code to function properly (HMM MAYBE NOT). The input files must be in the same format as given in 
the TSPLIB documentation which is readily available online. There are 6 main files concerning code and development:

	-run_tsp.py: main file, parses input files, creates graph structure, calls respective algorithm

	-branchAndBound.py: runs branch and bound algorithm (exact)

	-nearestNeighbor.py: runs nearest neighbor algorithm (approximation, greedy heuristic)

	-mstApprox.py: runs MST (minimum spanning tree) approximation algorithm

	-hillClimbing.py: runs hill climbing algorithm (iterated local search)

	-simulatedAnnealing.py: runs simulated annealing algorithm (local search)

This project makes use of the NetworkX package in Python and as such, to function properly networkx must be installed on the machine to run this code. 
Additional packages required are: INSERT HERE.