import run_tsp
import time
import hillClimbing as hc

rt = run_tsp.RunTSP()
G, opt_sol = rt.create_graph('ch150.tsp')

#qs = [.1,.2,.3]
algorithm = 'hill_climbing'

#times = [600, 1200, 1800]
filename = 'ch150.tsp'
random_seed = 1

datafile = open('ch150rawdata_hc.txt', 'w')
alldata = open('ch150data_hc.txt', 'w')

next = 1

seeds = [1,34,54,12,65,73,53,74,255,67]

q = -1
cutoff_time = 1800

for i in range(10):
	trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(i+1) + ".trace"
	start_hc = time.time()
	hc_tour, hc_cost, q_yes_no = hc.hctour(G, trfilename, opt_sol, cutoff_time, q, seeds[i])
	datafile.write(str(q) + "," + str(cutoff_time) + "," + str(i+1) + "," + str(q_yes_no) + "\n")
	print i

G, opt_sol = rt.create_graph('gr202.tsp')

#qs = [.1,.2,.3]
algorithm = 'hill_climbing'

times = [600, 1200, 1800]
filename = 'gr202.tsp'
random_seed = 1

datafile = open('gr202rawdata_hc.txt', 'w')
alldata = open('gr202data_hc.txt', 'w')

next = 1

for i in range(10):
	trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(i+1) + ".trace"
	start_hc = time.time()
	hc_tour, hc_cost, q_yes_no = hc.hctour(G, trfilename, opt_sol, cutoff_time, q, seeds[i])
	datafile.write(str(q) + "," + str(cutoff_time) + "," + str(i+1) + "," + str(q_yes_no) + "\n")
	print i