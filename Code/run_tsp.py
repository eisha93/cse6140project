#!/usr/bin/python
"""
This file contains the RunTSP class, which is the main body that runs all the code.
Four arguments are passed in via command line: <filename> <cutoff_time> <algorithm> <random seed>
This class will then run the appropriate algorithm on the input file within the cutoff_time and 
return the most optimal tour found and the cost of that tour. Statistics are also calculated, namely 
the time taken to run the algorithm and the relative error of the solution returned as compared to the
actual optimal solution.
"""
import networkx as nx
import time
import os
import sys
import math
import itertools
import nearestNeighbor as nn
import branchAndBound as bb
import hillClimbing as hc
import mstApprox as mst
import simAnneal as sa
import cProfile
import re

class RunTSP:
	def create_graph(self, filename):
		"""This method takes in the path to a file in the current directory and returns the created graph and the known optimal solution."""
		G = nx.Graph()
		#iterates through file to set appropriate variables
		yes = 1
		with open(filename, "r") as f: 
			while (yes == 1):                     
				line = f.readline()
				line = line.rstrip()
				if line.startswith('NAME: '):
					tsp_name = line[6:]
				elif line.startswith('TYPE: '):
					tsp_type = line[6:]
				elif line.startswith('COMMENT: '):
					tsp_comment = line[9:]
				elif line.startswith('DIMENSION: '):
					tsp_dim = int(line[11:])
				elif line.startswith('EDGE_WEIGHT_TYPE: '):
					tsp_ewt = line[18:]
				elif line.startswith('EDGE_WEIGHT_FORMAT: '):
					tsp_ewf = line[20:]
				elif line.startswith('DISPLAY_DATA_TYPE: '):
					tsp_ddt = line[19:]
				elif line.startswith('OPTIMAL_COST: '):
					tsp_opt = int(line[14:])
				elif line.startswith('NODE_COORD_SECTION'):
					yes = 0
					for l in f:
						if l.startswith('EOF'):
							break
						else:
							#splits each node data into node index, node x_coordinate, y_coordinate
							data = list(map(lambda x: float(x), l.split()))
							G.add_node(data[0], x_coord=data[1], y_coord=data[2])
		f.close()
		#add the edges (need edge between every pair of nodes)
		for u in G.nodes():
			for v in G.nodes():
				if u!=v:
					#if the edge weight type is euclidean, we set the weights to be the euclidean distance
					if tsp_ewt == 'EUC_2D':
						xd = G.node[u]['x_coord'] - G.node[v]['x_coord']
						yd = G.node[u]['y_coord'] - G.node[v]['y_coord']
						G.add_edge(u,v, weight=round((math.sqrt(xd*xd + yd*yd)))) 
					#else if the edge weight type is geographical, we set the weights appropriately as in the TSPLIB documentation
					elif tsp_ewt == 'GEO':
						lat_u,long_u = self.lat_long(G, u)
						lat_v,long_v = self.lat_long(G, v)
						q1 = math.cos(long_u - long_v)
						q2 = math.cos(lat_u - lat_v)
						q3 = math.cos(lat_u + lat_v)
						G.add_edge(u,v, weight=(int)((6378.388*math.acos(.5*((1.0+q1)*q2 - (1.0-q1)*q3))+1.0)))
		return G, tsp_opt

	def lat_long(self, G, num):
		"""This method helps in calculating the geographical distances between nodes. Given the graph and a node, it returns the latitude and longitude."""
		pi = 3.141592
		deg = (int)(G.node[num]['x_coord'])
		min = G.node[num]['x_coord'] - deg
		latitude = pi * (deg + 5.0 * min/3.0) / 180.0
		deg = (int)(G.node[num]['y_coord'])
		min = G.node[num]['y_coord'] - deg
		longitude = pi * (deg + 5.0 * min/3.0) / 180.0
		return latitude,longitude

	#main method. 
	def main(self):
		"""The main method runs the entire code, given the command line arguments, it creates the graph and calls the appropriate algorithm."""
		filename = sys.argv[1]
		cutoff_time = int(sys.argv[2])
		algorithm = sys.argv[3]
		random_seed = sys.argv[4]
		G, opt_sol = self.create_graph(filename)
		
		#to set up appropriate solution and trace files
		if algorithm == 'branch_and_bound' or algorithm == 'mst_approx' or algorithm == 'nearest_neighbor':
			solfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + ".sol"
			trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + ".trace"
		else:
			solfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(random_seed) + ".sol"
			trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(random_seed) + ".trace"

		solfile = open(solfilename, 'w')

		tour = G.nodes()
		cost = float("inf")

		end_time = 0

		#depending on algorithm given, calls appropriate algorithm to calculate solution on input graph
		if algorithm == 'branch_and_bound':
			start_bb = time.time()
			bb_tour,bb_cost = bb.bbtour(G, cutoff_time, trfilename) #branch and bound
			end_bb = (time.time() - start_bb) #in seconds
			if bb_tour is None:
				print "No solution returned in given timeframe."
			bb_rel_err = float(abs(bb_cost - opt_sol))/float(opt_sol)
			tour = bb_tour
			cost = bb_cost
			#end_time = end_bb
		elif algorithm == 'mst_approx':
			start_mst = time.time()
			mst_tour, mst_cost = mst.MST_approx_tour(G, trfilename, cutoff_time)
			end_mst = (time.time() - start_mst) #in seconds
			mst_rel_err = float(abs(mst_cost - opt_sol))/float(opt_sol)
			tour = mst_tour 
			cost = mst_cost 
		elif algorithm == 'nearest_neighbor':
			start_nn = time.time()
			nn_tour,nn_cost = nn.nntour(G, trfilename)
			end_nn = (time.time() - start_nn) #in seconds
			nn_rel_error = float(abs(nn_cost - opt_sol))/float(opt_sol)
			tour = nn_tour
			cost = nn_cost
		elif algorithm == 'hill_climbing':
			start_hc = time.time()
			hc_tour,hc_cost = hc.hctour(G, trfilename, opt_sol, cutoff_time, random_seed)
			end_hc = (time.time() - start_hc) #in seconds
			hc_rel_err = float(abs(hc_cost - opt_sol))/float(opt_sol)
			tour = hc_tour
			cost = hc_cost
			end_time = end_hc
		elif algorithm == 'simulated_annealing':
			#print "NOW RUNNING SIMULATED ANNEALING LOCAL SEARCH"
			#print 'testing' + filename
			start_sa = time.time()
			sa_tour, sa_cost = sa.simAnneal(G, trfilename, opt_sol, cutoff_time, random_seed)
			end_sa = (time.time() - start_sa) # in seconds
			#print 'time: ' + str(end_sa)
			#print 'length ' + str(sa_cost)
			sa_rel_err = float(abs(sa_cost - opt_sol))/float(opt_sol)
			#print 'err: ' + str(sa_rel_err)
			#print ''
			tour = sa_tour
			cost = sa_cost
			end_time = end_sa

		else:
			print "Please enter a correct algorithm name."

		print str(algorithm) + "_" + str(filename) + "_" + str(random_seed)
		print "time: " + str(end_time)
		print "cost: " + str(cost)
		print "----"

		#writes cost and tour to solution file
		solfile.write(str(cost)+"\n")
		tour_str = ""
		for node in tour:
			tour_str += str(node) + ","
		tour_str = tour_str[:(len(tour_str)-1)] #delete the last comma
		solfile.write(tour_str+"\n")
		
#calls main function to execute entire code
if __name__ == '__main__':
	runtsp = RunTSP()
	runtsp.main()
