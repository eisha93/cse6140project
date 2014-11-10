
def branchandbound(G):
	nodes = G.nodes()
	F = [] #list of solutions (a partial solution is a list?)
	B = {} #dict of best cost/soln?

	#add each node as a "partial" solution to F? as in you want to look at all possible
	#solns for all possible nodes right?
	for node in nodes:
		F.append([node])

	while F:
		#choose partial soln in F to expand by lower bound (and remove from F)
		#expand 
		#for each new config
			#check new config, if soln then update best appropriately
			#else add new config to F
