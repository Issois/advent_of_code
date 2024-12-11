
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(inp):
	# solve_internal(inp)
# def solve_internal(inp):
	# pr_inp(inp)
	inp_cp=inp.copy()

	answer=0
	nodes=set()
	antennas=set()
	for row in inp:
		antennas.update(row)
	antennas.remove(".")

	for antenna in antennas:
		indices=np.array(np.nonzero(inp==antenna)).T
		# indices=np.nonzero(inp==antenna)

		cnt=indices.shape[0]
		for a1_iidx in range(cnt):
			for a2_iidx in range(a1_iidx+1,cnt):
				a1_idx=indices[a1_iidx]
				a2_idx=indices[a2_iidx]

				delta=a2_idx-a1_idx
				p1=a2_idx+delta
				p2=a1_idx-delta

				for pos in [p1,p2]:
					if is_in_range(inp,pos):
						nodes.add(tuple(pos))
						inp_cp[tuple(pos)]="#"

		# return
	# print()
	# pr_inp(inp_cp)
	answer=len(nodes)
	# print(antennas)

	# 291 is correct.
	return answer

def pr_inp(inp):
	print("\n".join(["".join(row) for row in inp]))

def is_in_range(arr,pos):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)

def solve_2(inp):

	answer=0
	nodes=set()
	antennas=set()
	for row in inp:
		antennas.update(row)
	antennas.remove(".")

	for antenna in antennas:
		indices=np.array(np.nonzero(inp==antenna)).T
		# indices=np.nonzero(inp==antenna)

		cnt=indices.shape[0]
		for a1_iidx in range(cnt):
			for a2_iidx in range(a1_iidx+1,cnt):
				a1_idx=indices[a1_iidx]
				a2_idx=indices[a2_iidx]

				print(a1_idx,a2_idx)

				delta=a2_idx-a1_idx

				# k=0
				for k_start,step in ((0,1),(-1,-1)):
					k=k_start
					while True:
						pos=a1_idx+(k*delta)
						print(pos)
						if is_in_range(inp,pos):
							nodes.add(tuple(pos))
							k+=step
						else:
							break

	answer=len(nodes)

	# 1015 is correct.
	return answer




def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")
	inp=np.array([list(line) for line in inp])
	return inp


def main():
	inp=get_input(FILE_PATH)
	answer=solve(inp)
	print(f"ANSWER: {answer}")





RIDDLE_NUMBER=sys.argv[1]
FILE_PATH=sys.argv[2]

X=0
Y=1
Z=2

ROW=0
COL=1

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

solve=getattr(sys.modules[__name__],"solve_"+RIDDLE_NUMBER)
main()
