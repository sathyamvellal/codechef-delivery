'''
Input as follows : 
T - number of test cases
n - number of stores including bakery 
m - number of one-way streets
b - number of time units till day ends
u - some store
v - another store
d - time required to go from u to d

T
n, m, b
u, v, d
u, v, d
.
.
.
n, m, b
u, v, d
u, v, d
.
.
.


What to do : 
read T
for i from 1 to T do:
	read n, m, b
	create nxn graph, G
	for j from 1 to m do:
		place a directed edge E from u to v with weight d

	##we now have to traverse the graph such that we reach max nodes within the limit b
	#define a solution to be a new path; not any of the previously traversed paths
	place the bakery (or 0) to the current soln and make this the current position
	while the current soln is not empty:
		#define the next possible node from the current pos to be a node not traversed before and not in a solution tried before
		while a next node is possible from the current pos and its duration is less than remaining time:
			#from the current pos move to the next possible node
			eatup the remaining time
			make the current pos, the new node
			mark the new node as visited
			add the new node to the current soln
		add current soln as one of the possible solns. Also make note of remaning time left

		duplicate the current soln
		while a new solution is not possible from the last element of the duplicate:
			remove the last element from the duplicate
			add to the remaining time

'''
import time, copy

solns = []

#G is the graph
#rt is the remainingTime (initially passed with value of 'b')
#cs is the current solution
#ds is the duplicate solution of the current soln
#curpos, curt - current pos and current remaining time (used in backtracking logic); futpos, futt - future pos and fut remaining time (used in backtracking logic)
#pos is the current pos
def solve(G, b):
	cs = []
	ds = []
	pos = 0
	nextpos = -1
	n = len(G)
	print()
	print()
	rt = b
	cs.append((0, rt))
	print(cs)

	while len(cs) > 0:
		def nextPossibleNode():
			#exaust all possible never visited nodes
			for j in range(n):
				if pos != j:
					#there shd be a path to the node, should not be visited, and should be reachable in the remaining time
					if G[pos][j]["d"] > 0 and G[pos][j]["v"] == -1 and G[pos][j]["d"] <= rt:
						return j
			#exaust all possible currently not visited nodes, but have been tried in previous solns
			for j in range(n):
				if pos != j:
					#there shd be a path to the node, should not be visited, and should be reachable in the remaining time
					if G[pos][j]["d"] > 0 and G[pos][j]["v"] == 0 and G[pos][j]["d"] <= rt:
						return j
			#if no such node is available
			return -1
		nextpos = nextPossibleNode()
		while nextpos != -1:
			print("selecting ", nextpos)
			rt -= G[pos][nextpos]["d"]
			G[pos][nextpos]["v"] = 1
			pos = nextpos
			cs.append((pos, rt))
			print(cs)
			time.sleep(0.5)
			nextpos = nextPossibleNode()
		print("done with a solution")
		solns.append((cs, rt))
		#time.sleep(5)
		
		ds = copy.deepcopy(cs)
		futpos, futt = ds.pop()
		curpos, curt = ds[-1]
		G[curpos][futpos]["v"] = 0
		def newSolutionPossible():
			print("pos: ", curpos)
			print(G[curpos])
			for j in range(n):
				if curpos != j:
					#choose a node only if its not selected previously => v = -1
					if G[curpos][j]["d"] > 0 and G[curpos][j]["v"] == -1 and G[curpos][j]["d"] <= curt:
						return True
			return False
		while not newSolutionPossible() and len(ds) > 1:
			futpos, futt = ds.pop()
			curpos, curt = ds[-1]
			G[curpos][futpos]["v"] = 0
			cs = copy.deepcopy(ds)
			pos = curpos
			rt = curt
		if len(ds) == 1 and not newSolutionPossible():
			cs = []
		print("proceeding to next solution")
		time.sleep(5)

T = int(input())

for i in range(T):
	n, m, b = [int(i) for i in input().split()]
	G = [[{"d": 0, "v": -1} for i in range(n)] for i in range(n)]
	for j in range(m):
		u, v, d = [int(i) for i in input().split()]
		G[u][v]["d"] = d

	for row in G:
		print(row)
	solve(G, b)
	print("solved! -------- ")
	for soln in solns:
		print(soln)
