
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

import re
RGX=re.compile(r'-?\d+')


def solve_1(inp):
	return solve_internal(inp,seconds=100)

def solve_internal(inp,seconds):
	robots,area=inp
	field=move_robots(robots,area,seconds)
	answer=1
	answer*=np.sum(field[:(area[X]//2)   ,:(area[Y]//2)   ])
	answer*=np.sum(field[:(area[X]//2)   , (area[Y]//2)+1:])
	answer*=np.sum(field[ (area[X]//2)+1:,:(area[Y]//2)   ])
	answer*=np.sum(field[ (area[X]//2)+1:, (area[Y]//2)+1:])

	return answer

def move_robots(robots,area,seconds):
	field=np.zeros(area,dtype=int)
	for robot in robots:
		final_location=robot[POS]+(seconds*robot[VEL])
		final_location=np.floor(final_location)
		final_location=final_location.astype(int)
		final_location=final_location%area
		field[tuple(final_location)]+=1
	return field

def solve_2(inp):
	answer=0
	robots,area=inp
	max_steps=area[X]*area[Y]

	fig,ax=plt.subplots()
	artists=[]
	sums=[]
	for seconds in range(max_steps+1):
		if seconds%500==0:
			print(seconds)
		field=move_robots(robots,area,seconds)
		sums.append(np.sum(np.abs(field-field[:,::-1])))

	# print(sums)

	min_sum=1_000_000_000
	min_idx=None
	for idx,_sum in enumerate(sums):
		if _sum<min_sum:
			min_sum=_sum
			min_idx=idx

	answer=min_idx
	# plt.imshow(move_robots(robots,area,answer))
	# plt.show()
	# return

	# 8087 is correct.
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
