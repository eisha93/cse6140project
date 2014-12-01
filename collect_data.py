import run_tsp
import time
import hillClimbing as hc

rt = run_tsp.RunTSP()
G, opt_sol = rt.create_graph('ch150.tsp')

qs = [.1,.15,.2,.25]
algorithm = 'hill_climbing'

times = [120, 180, 240, 300, 360, 420]
filename = 'ch150.tsp'
random_seed = 1

datafile = open('ch150rawdata.txt', 'w')
alldata = open('ch150data.txt', 'w')

next = 1

for q in qs:
	for cutoff_time in times:
		count = 0
		for i in range(10):
			trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(random_seed) + ".trace"
			start_hc = time.time()
			hc_tour, hc_cost, q_yes_no = hc.hctour(G, trfilename, opt_sol, cutoff_time, q)
			datafile.write(str(q) + "," + str(cutoff_time) + "," + str(i+1) + "," + str(q_yes_no) + "\n")
			if q_yes_no=='yes':
				count += 1
		alldata.write(str(q)+","+str(cutoff_time)+","+str(count)+"\n")