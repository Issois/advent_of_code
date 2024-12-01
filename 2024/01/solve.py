
import numpy as np
import sys
def main():
	with open(sys.argv[2]) as f:
		inp=f.read().split("\n")

	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]


	result=solve(inp)

	print(f"ANSWER: {result}")


def solve_1(inp):
	inp=np.array([[int(col) for col in row.split("   ")] for row in inp])
	inp=[np.sort(inp[:,ax]) for ax in range(inp.shape[1])]
	result=np.sum(np.abs(inp[0]-inp[1]))
	return result

def solve_2(inp):
	inp=np.array([[int(col) for col in row.split("   ")] for row in inp])

	cnt={}
	for num in inp[:,1]:
		if num not in cnt:
			cnt[num]=0
		cnt[num]+=1

	result=0

	for num in inp[:,0]:
		if num in cnt:
			result+=num*cnt[num]

	return result

main()
