
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(inp):
	answer=0
	
	blink_count=25
	stones=inp
	for _ in range(blink_count):
		new_stones=[]
		for stone in stones:
			if stone==0:
				new_stones.append(1)
			elif (stone_len:=len(stone_str:=str(stone)))%2==0:
				new_stones.append(int(stone_str[:stone_len//2]))
				new_stones.append(int(stone_str[stone_len//2:]))
			else:
				new_stones.append(stone*2024)
		stones=new_stones

	# 199986 is correct.
	answer=len(stones)


	return answer

def solve_2(inp):
	answer=0
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split(" ")
	# return list(np.array(inp,dtype=int))
	return [int(num) for num in inp]


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
