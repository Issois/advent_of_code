
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(inp):
	answer=0
	arr=np.zeros(len(inp)+1)
	arr[0]=50
	for index,element in enumerate(inp):
		arr[index+1]=int(element[1:])*(-1 if element[0]=="L" else 1)+arr[index]

	arr=arr%100
	answer=np.sum(arr==0)
	return answer

def solve_2(inp):
	answer=0
	pos=50
	for element in inp:
		floor=pos//100
		previouslyAt0=pos%100==0
		dire=-1 if element[0]=="L" else 1
		dire_str="-" if dire<0 else "+"
		amount=int(element[1:])
		pos+=amount*dire
		nowAt0=pos%100==0
		new_floor=pos//100

		floor_diff=abs(new_floor-floor)
		print(f"{dire_str}{amount:4.0f} = {pos:4.0f}",end="")
		if nowAt0:
			answer+=1
			print(" hit 0 ",end="")
		if (previouslyAt0 and dire==-1) or (nowAt0 and dire==1):
			floor_diff-=1
		answer+=floor_diff
		if floor_diff>0:
			print(f" passed {floor_diff}",end="")


		print("")
			

	return answer

	# 2658 is too low.
	# 3115 is too low.
	# 4629 is too low.
	# 7191 is wrong.
	# 6634 is correct!


def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")
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

def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)

solve=getattr(sys.modules[__name__],"solve_"+RIDDLE_NUMBER)
main()
