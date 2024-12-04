
import numpy as np
import sys
def main():
	with open(sys.argv[2]) as f:
		inp=f.read().split("\n")
	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]

	print(f"ANSWER: {solve(inp)}")

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

	# print(new_pos,arr[new_pos])

	return arr[tuple(new_pos)]==WORD[idx] and check(arr,new_pos,dire,idx+1)



def solve_2(inp):
	result=None
	return result

main()
