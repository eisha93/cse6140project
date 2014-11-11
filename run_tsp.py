#!/usr/bin/python

import networkx as nx
import time
import os
import sys
import math

import nearestneighbor as nn
import branchandbound as bb

class RunTSP:
    def create_graph(self, filename):
        """
        Reads the graph from the given file and returns the graph object
        as a networkx graph.
        """
        # init graph
        G = nx.Graph()

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
                elif line.startswith('NODE_COORD_SECTION'):
                    yes = 0
                    for l in f:
                        if l.startswith('EOF'):
                        	break
                        else:
                        	#print l
                        	data = list(map(lambda x: float(x), l.split()))
                        	G.add_node(data[0], x_coord=data[1], y_coord=data[2])
                else:
                    print "HALP"
        f.close()
        

        #add the edges (need edge between every pair of nodes)
        for u in G.nodes():
            for v in G.nodes():
                if u!=v:
                    if tsp_ewt == 'EUC_2D':
                        xd = G.node[u]['x_coord'] - G.node[v]['x_coord']
                        yd = G.node[u]['y_coord'] - G.node[v]['y_coord']
                        G.add_edge(u,v, weight=round(math.sqrt(xd*xd + yd*yd)))
                    elif tsp_ewt == 'GEO':
                        lat_u,long_u = self.lat_long(G, u)
                        lat_v,long_v = self.lat_long(G, v)
                        q1 = math.cos(long_u - long_v)
                        q2 = math.cos(lat_u - lat_v)
                        q3 = math.cos(lat_u + lat_v)
                        G.add_edge(u,v, weight=(int)(6378.388*math.acos(.5*((1.0+q1)*q2 - (1.0-q1)*q3))+1.0))
        return G

    def lat_long(self, G, num):
        pi = 3.141592
        deg = round(G.node[num]['x_coord'])
        min = G.node[num]['x_coord'] - deg
        latitude = pi * (deg + 5.0 * min/3.0) / 180
        deg = round(G.node[num]['y_coord'])
        min = G.node[num]['y_coord'] - deg
        longitude = pi * (deg + 5.0 * min/3.0) / 180
        return latitude,longitude

    def main(self):

        filename = sys.argv[1]
        #cutoff_time = sys.argv[2]
        #algorithm = sys.argv[3]
        #random_seed = sys.argv[4]

        G = self.create_graph(filename)
        #nn_tour,nn_cost = nn.nntour(G) #nearest neighbor
        #print nn_cost
        #print nn_tour

        bb_tour,bb_cost = bb.bbtour(G) #branch and bound
        print bb_cost
        print bb_tour

if __name__ == '__main__':
    runtsp = RunTSP()
    runtsp.main()
