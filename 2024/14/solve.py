
import numpy as np
import sys
import matplotlib.pyplot as plt

import re
RGX=re.compile(r'-?\d+')


def solve_1(inp):
	return solve_internal(inp,seconds=100)

def solve_internal(inp,seconds):
	answer=0
	robots,area=inp
	field=np.zeros(area,dtype=int)
	for robot in robots:
		final_location=robot[POS]+(seconds*robot[VEL])
		final_location=final_location%area
		field[tuple(final_location)]+=1

	answer=1
	answer*=np.sum(field[:(area[X]//2)   ,:(area[Y]//2)   ])
	answer*=np.sum(field[:(area[X]//2)   , (area[Y]//2)+1:])
	answer*=np.sum(field[ (area[X]//2)+1:,:(area[Y]//2)   ])
	answer*=np.sum(field[ (area[X]//2)+1:, (area[Y]//2)+1:])

	return answer

def solve_2(inp):
	answer=0
	robots,area=inp
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")

	arr=np.zeros((len(inp),2,2),dtype=int)
	for idx,line in enumerate(inp):
		vals=[int(num) for num in RGX.findall(line)]
		arr[idx,POS,X]=vals[0]
		arr[idx,POS,Y]=vals[1]
		arr[idx,VEL,X]=vals[2]
		arr[idx,VEL,Y]=vals[3]

	if file_path[-len("example1.input"):]=="example1.input":
		area=np.array((11,7),dtype=int)
	if file_path[-len("data.input"):]=="data.input":
		area=np.array((101,103),dtype=int)

	return arr,area


def main():
	inp=get_input(FILE_PATH)
	answer=solve(inp)
	print(f"ANSWER: {answer}")





RIDDLE_NUMBER=sys.argv[1]
FILE_PATH=sys.argv[2]

X=0
Y=1
Z=2

POS=0
VEL=1

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
