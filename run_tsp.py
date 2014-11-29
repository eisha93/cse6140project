#!/usr/bin/python

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
    #pass in the direct filename to this method, returns an undirected graph with edges between every pair of cities (don't need to modify this)
    def create_graph(self, filename):
        # init graph
        G = nx.Graph()
        yes = 1
        #iterates through file to set appropriate variables
        with open(filename, "r") as f: 
            while (yes == 1):                     
                line = f.readline()
                line = line.rstrip()
                #sets name
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
                        	#print l
                            #splits each node data into node index, node x_coordinate, y_coordinate
                        	data = list(map(lambda x: float(x), l.split()))
                        	G.add_node(data[0], x_coord=data[1], y_coord=data[2])
                #else:
                    #print "HALP"
        f.close()
        #add the edges (need edge between every pair of nodes)
        for u in G.nodes():
            for v in G.nodes():
                if u!=v:
                    if tsp_ewt == 'EUC_2D':
                        xd = G.node[u]['x_coord'] - G.node[v]['x_coord']
                        yd = G.node[u]['y_coord'] - G.node[v]['y_coord']
                        G.add_edge(u,v, weight=round((math.sqrt(xd*xd + yd*yd)))) #should this be round() or (int)
                    elif tsp_ewt == 'GEO':
                        lat_u,long_u = self.lat_long(G, u)
                        lat_v,long_v = self.lat_long(G, v)
                        q1 = math.cos(long_u - long_v)
                        q2 = math.cos(lat_u - lat_v)
                        q3 = math.cos(lat_u + lat_v)
                        G.add_edge(u,v, weight=(int)((6378.388*math.acos(.5*((1.0+q1)*q2 - (1.0-q1)*q3))+1.0)))
        #return the graph object and what the known optimal solution is
        return G, tsp_opt

    #for geo coordinates (don't need to modify this)
    def lat_long(self, G, num):
        pi = 3.141592
        deg = (int)(G.node[num]['x_coord'])
        min = G.node[num]['x_coord'] - deg
        latitude = pi * (deg + 5.0 * min/3.0) / 180.0
        deg = (int)(G.node[num]['y_coord'])
        min = G.node[num]['y_coord'] - deg
        longitude = pi * (deg + 5.0 * min/3.0) / 180.0
        return latitude,longitude

    #ignore this method, purely for testing purposes
    def testing(self, G):
        p = itertools.permutations(G.nodes())
        for x in p:
            temp = bb.find_cost(x,G)
            if temp == 3323:
                print "YES " + str(temp)
                break
            elif temp == 3454:
                print "eh "

    #ignore this method, purely for testing purposes
    def make_p_graph(self):
        p = nx.Graph()
        for x in range(1,5):
            p.add_node(x)
            #print x
        p.add_edge(1, 2, weight = 1)
        p.add_edge(2,3, weight = 2)
        p.add_edge(1,3, weight = 3)
        p.add_edge(1, 4, weight = 1)
        p.add_edge(4,3, weight = 2)
        p.add_edge(2,4,weight=3)
        #print p.edges()
        return p

    #main method. 
    def main(self):
        #optimals = [3323, 6859, 7542, 21282, 6528, 40160]

        filename = sys.argv[1]
        cutoff_time = int(sys.argv[2])
        algorithm = sys.argv[3]
        #random_seed = sys.argv[4]
        random_seed = 1
        G, opt_sol = self.create_graph(filename)

        #for finding relative error
        #opt_sol = None
        #if filename == 'burma14.tsp':
        #    opt_sol = optimals[0]
        #elif filename == 'ulysses16.tsp':
        #    opt_sol = optimals[1]
        #elif filename == 'berlin52.tsp':
        #    opt_sol = optimals[2]
        #elif filename == 'kroA100.tsp':
        #    opt_sol = optimals[3]
        #elif filename == 'ch150.tsp':
        #    opt_sol = optimals[4]
        #elif filename == 'gr202.tsp':
        #    opt_sol = optimals[5]
        #else:
        #    print "You didn't give the right filename, try again"
        #    exit()
        #begin testing for 5 algorithms
        #uncomment out whichever ones that you need to test
        #
        #

        if algorithm == 'branch_and_bound' or algorithm == 'mst_approx' or algorithm == 'nearest_neighbor':
            solfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + ".sol"
            trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + ".trace"
        else:
            solfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(random_seed) + ".sol"
            trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(random_seed) + ".trace"

        solfile = open(solfilename, 'w')
        #trfile = open(trfilename, 'w')

        tour = G.nodes()
        cost = float("inf")

        if algorithm == 'branch_and_bound':
            #Branch and Bound
            print 'NOW RUNNING BRANCH AND BOUND'
            print 'testing ' + filename
            start_bb = time.time()
            bb_tour,bb_cost = bb.bbtour(G, cutoff_time, trfilename) #branch and bound
            end_bb = (time.time() - start_bb) #in seconds
            if bb_tour is None:
                print "give me more time yo"
            #else:
            #    solfile.write(str(bb_cost))
            #    tour = ""
            #    for node in bb_tour:
            #        tour += str(node)

                #print bb_cost
                #print bb_tour
            bb_rel_err = float(abs(bb_cost - opt_sol))/float(opt_sol)
            print bb_rel_err
            tour = bb_tour
            cost = bb_cost
        elif algorithm == 'mst_approx':
            #MST approximation
            print 'NOW RUNNING MST APPROXIMATION'
            print 'testing ' + filename
            start_mst = time.time()
            mst_tour, mst_cost = mst.MST_approx_tour(G, trfilename)
            end_mst = (time.time() - start_mst) #in seconds
            mst_rel_err = float(abs(mst_cost - opt_sol))/float(opt_sol)
            print 'cost: ' + str(mst_cost)
            print 'time: ' + str(end_mst)
            print 'error: ' + str(mst_rel_err)
            tour = mst_tour #FIX ME
            cost = mst_cost #FIX ME

        elif algorithm == 'nearest_neighbor':
            #Nearest Neighbor approximation
            print 'NOW RUNNING NEAREST NEIGHBOR'
            print 'testing ' + filename
            start_nn = time.time()
            nn_tour,nn_cost = nn.nntour(G, trfilename)
            end_nn = (time.time() - start_nn) #in seconds
            print "cost: " + str(nn_cost)
            print "time: " + str(end_nn)
            print nn_tour
            nn_rel_error = float(abs(nn_cost - opt_sol))/float(opt_sol)
            print "error: " + str(nn_rel_error)
            tour = nn_tour
            cost = nn_cost

        elif algorithm == 'hill_climbing':
            #hillClimbing local search
            print 'NOW RUNNING HILL CLIMBING LOCAL SEARCH'
            print 'testing ' + filename
            start_hc = time.time()
            hc_tour,hc_cost = hc.hctour(G, trfilename, opt_sol) #hill climbing
            end_hc = (time.time() - start_hc) #in seconds
            print "time: " + str(end_hc)
            print "length: " + str(hc_cost)
            hc_rel_err = float(abs(hc_cost - opt_sol))/float(opt_sol)
            print "err: " + str(hc_rel_err)
            print ""
            tour = hc_tour
            cost = hc_cost

        elif algorithm == 'simulated_annealing':
            print "NOW RUNNING SIMULATED ANNEALING LOCAL SEARCH"
            print 'testing' + filename
            start_sa = time.time()
            sa_tour, sa_cost = sa.simAnneal(G, trfilename, opt_sol)
            end_sa = (time.time() - start_sa) # in seconds
            print 'time: ' + str(end_sa)
            print 'length ' + str(sa_cost)
            sa_rel_err = float(abs(sa)cost - opt_sol))/float(opt_sol)
            print 'err: ' + str(sa_rel_err)
            print ''
            tour = sa_tour
            cost = sa_cost

        else:
            print "you failed enter the correct name for an algorithm"

        solfile.write(str(cost)+"\n")
        tour_str = ""
        for node in tour:
            tour_str += str(node) + ","
        tour_str = tour_str[:(len(tour_str)-1)] #delete the last comma
        solfile.write(tour_str+"\n")


        #iterated local search - NOT YET STARTED
        #print 'NOW RUNNING ITERATED LOCAL SEARCH'
        # print 'testing ' + filename
        #start_ils = time.time()
        #PLACE CALL TO FXN HERE
        #end_ils = (time.time() - start_ils) * 1000 #to convert to millis
        #ils_rel_err = float(abs(ils_cost - opt_sol))/float(opt_sol)
        
        #
        #
        #
        #
        #
        #
        #FOR RANDOM TESTING FUNCTIONS AND METHODS
        #PLACE ALL RANDOM CODE HERE, NOT ABOVE! 
        #
        
        #p is a small 3 node graph TESTING ONLY 
        #P = self.make_p_graph()
        
        # cutoff_time = float("inf") #in minutes
        

if __name__ == '__main__':
    runtsp = RunTSP()
    runtsp.main()
