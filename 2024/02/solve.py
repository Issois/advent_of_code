
import numpy as np
import sys
def main():
	with open(sys.argv[2]) as f:
		inp=f.read().split("\n")
	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]

	print(f"ANSWER: {solve(inp)}")

def solve_1(inp):

	result=0
	for line in inp:
		arr=np.array(line.split(" "),dtype=int)
		diff=arr[1:]-arr[:-1]
		pos=diff>0
		neg=diff<0
		absd=np.abs(diff)
		one=absd>=1
		thr=absd<=3
		if (np.all(pos) or np.all(neg)) and np.all(one) and np.all(thr):
			result+=1


	return result

def solve_2(inp):
	result=None
	return result

main()
