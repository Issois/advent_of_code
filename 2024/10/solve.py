
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(arr):
	answer=0
	# print(arr)
	heads=np.array(np.nonzero(arr==0)).T

	for head in heads:
		positions=[head]
		peaks=set()
		while len(positions)>0:
			position=positions.pop()
			current_height=arr[tuple(position)]
			if current_height==9:
				# print(head,position)
				# answer+=1
				peaks.add(tuple(position))
			else:
				for dire in DIREV[::2]:
					new_position=position+dire
					if is_in_range(new_position,arr):
						new_height=arr[tuple(new_position)]
						if new_height-current_height==1:
							positions.append(new_position)
		answer+=len(peaks)

	# print(heads)


	return answer

# def is_trail(arr,pos,)

def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)

def solve_2(inp):
	answer=0
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")
	inp=np.array([[int(num) for num in row] for row in inp])
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

DIREV=np.array([
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
