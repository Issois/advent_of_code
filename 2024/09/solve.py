
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(inp):
	answer=0
	sizes=inp[::2]
	spaces=inp[1::2]
	# print(sizes)
	# print(spaces)
	idx_file_start=0
	idx_inside_start=0
	idx_file_end=len(sizes)-1
	idx_inside_end=sizes[idx_file_end]-1
	idx_space_start=0
	idx_space_inside_start=0
	idx_result=0
	# idx_end=-1

	in_file=True

	result_index=0
	while True:
		if in_file:
			file_index=idx_file_start
			idx_inside_start+=1
			if idx_inside_start>=sizes[idx_file_start]:
				in_file=False
				idx_file_start+=1
		else:
			file_index=idx_file_end
			idx_space_inside_start+=1
			if idx_space_inside_start>=spaces[idx_space_start]:
				in_file=True
				idx_space_start+=1
			pass

		answer+=(file_index*result_index)
		result_index+=1

	return answer

def solve_2(inp):
	answer=0
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=np.array([int(ch) for ch in f.read()])
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
