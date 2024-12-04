
import numpy as np
import sys
def main():
	with open(sys.argv[2]) as f:
		inp=f.read().split("\n")
	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]

	print(f"ANSWER: {solve(inp)}")
X=0
Y=1
WORD="XMAS"
DIRE=np.array([
	[-1, 0],
	[-1, 1],
	[ 0, 1],
	[ 1, 1],
	[ 1, 0],
	[ 1,-1],
	[ 0,-1],
	[-1,-1],
])


def solve_1(inp):
	# conv={"X":0,"M":1,"A":2,"S",3}
	xs=[]
	rowc=len(inp)
	colc=len(inp[0])
	inp=np.array([list(row) for row in inp],dtype=str)
	# arr=np.zeros((rowc,colc))
	for row in range(rowc):
		for col in range(colc):
			if inp[row,col]==WORD[0]:
				xs.append(np.array((row,col)))
	result=0

	for start in xs:
		for dire in DIRE:
			if check(inp,start,dire,1):
				result+=1

	return result

def check(arr,pos,dire,idx):
	if idx>=len(WORD):
		return True
	new_pos=pos+dire
	if np.any(new_pos<0) or np.any(new_pos>=arr.shape):
		return False

	return arr[tuple(new_pos)]==WORD[idx] and check(arr,new_pos,dire,idx+1)



def solve_2(inp):
	result=0


	rowc=len(inp)
	colc=len(inp[0])
	inp=np.array([list(row) for row in inp],dtype=str)

	a_cnt=0

	for row in range(1,rowc-1):
		for col in range(1,colc-1):
			pos=np.array([row,col])
			char=inp[tuple(pos)]
			if char=="A":
				a_cnt+=1
				mas=[]
				dires=DIRE[1::2,:]
				xs=inp[pos[X]+dires[:,X],pos[Y]+dires[:,Y]]
				if (((xs[0]=="M" and xs[2]=="S")
				  or (xs[0]=="S" and xs[2]=="M")
				  )   and(
				     (xs[1]=="M" and xs[3]=="S")
				  or (xs[1]=="S" and xs[3]=="M")
					)):
					result+=1
	return result

main()
