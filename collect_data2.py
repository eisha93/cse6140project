import run_tsp
import time
import simAnneal as sa

rt = run_tsp.RunTSP()
G, opt_sol = rt.create_graph('ch150.tsp')

qs = [.1,.2,.3]
algorithm = 'simulated_annealing'

times = [600, 1200, 1800]
filename = 'ch150.tsp'
random_seed = 1

datafile = open('ch150rawdata.txt', 'w')
alldata = open('ch150data.txt', 'w')

next = 1

seeds = [1,34,54,12,65,73,53,74,255,67]

for q in qs:
	for cutoff_time in times:
		count = 0
		for i in range(10):
			trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(i+1) + ".trace"
			start_hc = time.time()
			hc_tour, hc_cost, q_yes_no = sa.simAnneal(G, trfilename, opt_sol, cutoff_time, seeds[i], q)
			datafile.write(str(q) + "," + str(cutoff_time) + "," + str(i+1) + "," + str(q_yes_no) + "\n")
			if q_yes_no=='yes':
				count += 1
		alldata.write(str(q)+","+str(cutoff_time)+","+str(count)+"\n")

G, opt_sol = rt.create_graph('ch150.tsp')

qs = [.1,.2,.3]
algorithm = 'simulated_annealing'

times = [600, 1200, 1800]
filename = 'gr202.tsp'
random_seed = 1

datafile = open('gr202rawdata.txt', 'w')
alldata = open('gr202data.txt', 'w')

next = 1

for q in qs:
	for cutoff_time in times:
		count = 0
		for i in range(10):
			trfilename = filename[:(len(filename)-4)] + "_" + algorithm + "_" + str(cutoff_time) + "_" + str(i+1) + ".trace"
			start_hc = time.time()
			hc_tour, hc_cost, q_yes_no = sa.simAnneal(G, trfilename, opt_sol, cutoff_time, seeds[i], q)
			datafile.write(str(q) + "," + str(cutoff_time) + "," + str(i+1) + "," + str(q_yes_no) + "\n")
			if q_yes_no=='yes':
				count += 1
		alldata.write(str(q)+","+str(cutoff_time)+","+str(count)+"\n")