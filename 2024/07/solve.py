
import numpy as np
import sys
# import matplotlib.pyplot as plt

def add(a,b):return a+b
def mul(a,b):return a*b
def concat(a,b):return int(str(a)+str(b))

def solve_1(inp):
	return solve_internal(inp,[add,mul])
def solve_internal(inp,ops):
	answer=0
	for result,nums in inp:
		calcs=[nums[0]]
		for num in nums[1:]:
			new_calcs=[]
			for calc in calcs:
				for op in ops:
					new_calc=op(calc,num)
					if new_calc<=result:
						new_calcs.append(new_calc)
			calcs=new_calcs
		for calc in calcs:
			if calc==result:
				answer+=calc
				break
	return answer



def solve_2(inp):
	return solve_internal(inp,[add,mul,concat])

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")
	data=[]
	for line in inp:
		result,nums=line.split(":")
		nums=[int(num) for num in nums.strip().split(" ")]
		data.append((int(result),nums))
	return data


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
