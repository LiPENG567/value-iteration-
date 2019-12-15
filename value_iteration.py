from timeit import default_timer as timer
start = timer()
infinity = 2**32

def Rewa(state):
	"""define reward function"""
	sta = state
	row = sta[0]
	col = sta[1]
	rewa = Reward[row][col]
	# print reward 

	return rewa

def actions(state):
	"""define acitions"""
	statee = state
	row = statee[0]
	col = statee[1]

	if statee in terminal:
		return [None]
	
	else:
		if row <= 0: ## move up
			moveup = (row,col)
			moveup_a = (row,col)
			moveup_c = (row,col)

		else:
			if(grid[row-1][col]==None):
				moveup = (row,col)
			else:
				moveup = (row-1,col)

			if(grid[row-1][col-1] == None or col-1<0):
				moveup_a = (row,col)
			else:
				moveup_a = (row-1,col-1)

			# if((grid[row-1][col+1] == None and col+1<=N) or col+1>N):
			if(col+1>N-1):# be careful with range
				moveup_c = (row,col)
			if col+1<N:
				if grid[row-1][col+1] == None:
					moveup_c = (row,col)
				else:
					moveup_c = (row-1,col+1)


		if row == N-1: ## move down
			movedown = (row,col)
			movedown_a = (row,col)
			movedown_c = (row,col)

		else:
			if(grid[row+1][col]==None):
				movedown = (row,col)
			else:
				movedown = (row+1,col)

			if(grid[row+1][col-1] == None or col-1<0):
				movedown_a = (row,col)
			else:
				movedown_a = (row+1,col-1)

			# if((grid[row-1][col+1] == None and col+1<=N) or col+1>N):
			if(col+1>N-1):# be careful with range
				movedown_c = (row,col)
			if col+1<N:
				if grid[row+1][col+1] == None:
					movedown_c = (row,col)
				else:
					movedown_c = (row+1,col+1)
			# print movedown,movedown_a,movedown_c


		if col <= 0: ## move left
			moveleft = (row,col)
			moveleft_a = (row,col)
			moveleft_c = (row,col)

		else:
			if(grid[row][col-1]==None):
				moveleft = (row,col)
			else:
				moveleft = (row,col-1)

			if(grid[row-1][col-1] == None or row-1<0):
				moveleft_a = (row,col)
			else:
				moveleft_a = (row-1,col-1)

			# if((grid[row-1][col+1] == None and col+1<=N) or col+1>N):
			if(row+1>N-1):# be careful with range
				moveleft_c = (row,col)
			if row+1<N:
				if grid[row+1][col-1] == None:
					moveleft_c = (row,col)
				else:
					moveleft_c = (row+1,col-1)
		# print moveleft,moveleft_a,moveleft_c



		if col == N-1: ## move right
			moveright = (row,col)
			moveright_a = (row,col)
			moveright_c = (row,col)

		else:
			if(grid[row][col+1]==None):
				moveright = (row,col)
			else:
				moveright = (row,col+1)

			if(grid[row-1][col+1] == None or row-1<0):
				moveright_a = (row,col)
			else:
				moveright_a = (row-1,col+1)

			# if((grid[row-1][col+1] == None and col+1<=N) or col+1>N):
			if(row+1>N-1):# be careful with range
				moveright_c = (row,col)
			if row+1<N:
				if grid[row+1][col+1] == None:
					moveright_c = (row,col)
				else:
					moveright_c = (row+1,col+1)


		actionlist = [[moveup,moveup_a,moveup_c],[movedown,movedown_a,movedown_c],[moveleft,moveleft_a,moveleft_c],[moveright,moveright_a,moveright_c]]
		# print actionlist
		return actionlist

def T(state,action):
	"""define transition model"""
	act = action
	stat = state
	if act == None:
		return [(0.0,stat)]
	else:
		intent = act[0]
		anti = act[1]
		clock = act[2]
		# print [[P,intent],[(1-P)/2,anti],[(1-P)/2,clock]]
		return [(P,intent),((1-P)/2,anti),((1-P)/2,clock)]


def value_iteration(mdp,epsilon=0.0001):
	"""define value iteration function"""
	states = mdp['states']
	# print states
	U1 = {s:0 for s in states}
	R = mdp['Rp']
	gamma = mdp['gamma']
	tranmodel = mdp['tranmodel']
	# print R,gamma,tranmodel
	
	while True:
		U = U1.copy()
		delta = 0
		for s in states:
			U1[s] = Rewa(s)+gamma*max([sum([p*U[s1] for (p,s1) in T(s,a)]) for a in actions(s)])
			# print s,U1[s],U[s1]
			if abs(U1[s]-U[s]) > delta:
				delta = abs(U1[s]-U[s])
		# print "delta = ", delta
		if delta < epsilon*(1-gamma)/gamma:
			return U

def optimal_policy(mdp,U):
	"""define the optimal policy"""
	U = U
	states = mdp['states']
	Wall = mdp['wall']
	pi = {}
	mm = None
	for s in states:
		maxexp = -1e20
		actt = []
		# mm = None
		for a in actions(s):

			if a == None:
				mm = "E"
			else:
				exp = sum([p*U[s1] for (p,s1) in T(s,a)])
				if exp > maxexp:
					maxexp = exp
					actt = a
					indx = actions(s).index(actt)
					# print indx
					if indx == 0:
						mm = "U"
					if indx == 1:
						mm = "D"				
					if indx == 2:
						mm = "L"
					if indx == 3:
						mm = "R"	
		pi[s] = mm
		# print pi

	# print pi
	RR = []
	for r in range(N):
		AA = []
		for c in range(N):
			ss = (r,c)
			if ss in Wall: # in wall, no reduction of the value is done
				# print ss
				aa = "N"
			else:
				aa = pi.get(ss)
				# print aa
			AA.append(aa)
		RR.append(AA)
	return RR



input = open('input.txt','r')
N = input.readline().replace('\n','').replace('\r','')
N = int(N)
Grid = []
for r in range(N):
	# print N
	A = []
	for c in range(N):
		a = 0
		A.append(a)
	Grid.append(A)


Nw = input.readline().replace('\n','').replace('\r','')
# print Nw
W = []
for i in range(int(Nw)):
	NN = input.readline().replace('\n','').replace('\r','')
	l=NN.split(",")
	r = int(l[0])
	c = int(l[1])
	l=(r-1,c-1)
	W.append(l)
# print W

for a in W:
	# print a
	r = a[0]
	c = a[1]
	Grid[r][c]=None

# print grid

Nter = input.readline().replace('\n','').replace('\r','')
# print Nter 
terminal = []
for i in range(int(Nter)):
	NN = input.readline().replace('\n','').replace('\r','')
	l=NN.split(",")
	# print l
	r = int(l[0])
	c = int(l[1])
	Rt = int(l[2])
	Grid[r-1][c-1] = Rt
	l = (r-1,c-1)
	# print l
	terminal.append(l)
# print terminal
states = []
for r in range(N):
	for c in range(N):
		if Grid[r][c] is not None:
			ab = (r,c)
			states.append(ab)
# print states

P = input.readline().replace('\n','').replace('\r','')
P = float(P)
# print P

Rp = input.readline().replace('\n','').replace('\r','')
Rp = float(Rp)
# print Rp

for r in range(N):
	for c in range(N):
		if Grid[r][c] == 0 and (r,c) not in terminal:
			Grid[r][c] = Rp
			
Reward = Grid
grid = Grid
# print grid

gamma = input.readline().replace('\n','').replace('\r','')
gamma = float(gamma)
# print gamma


mdp = {"reward":Reward, "tranmodel":P, "Rp":Rp,'gamma':gamma,'terminal':terminal,'states':states,'wall':W} # globle varibale

opt = optimal_policy(mdp,value_iteration(mdp,epsilon=0.0001))

filename = 'output.txt'
with open(filename,'w') as zaili:
	for i in range(N):

		buf = ",".join(opt[i])
		zaili.write(buf+"\n")
		#zaili.write(str(a)+","+str(b)+","+str(c)+","+str(d)+","+str(e)+'\n')

end = timer()
print (end-start)