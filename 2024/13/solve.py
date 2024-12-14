
import numpy as np
import sys
import re
# import matplotlib.pyplot as plt

RGX=re.compile(r'\d+')

def solve_1(machines):
	answer=0
	cost=np.array([3,1])

	for machine in machines:
		mat=machine[:2].T
		inv=np.linalg.inv(mat)
		result_f=inv@machine[2].T
		result=np.round(result_f).astype(int)
		if np.all(mat@result==machine[2]) and np.all(result_f>0) and np.all(result_f<=100):
			answer+=np.dot(result,cost)

	# 16169 is too low.
	# 27157 is correct.

	return answer

def solve_2(machines):
	answer=0
	return answer



def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n\n")
	vals=[]
	for block in inp:
		lines=block.split("\n")
		val=np.zeros((3,2),dtype=int)
		for idx,line in enumerate(lines):
			val[idx]=[int(num) for num in RGX.findall(line)]
		vals.append(val)
	return vals


def main():
	inp=get_input(FILE_PATH)
	answer=solve(inp)
	print(f"ANSWER: {answer}")





RIDDLE_NUMBER=sys.argv[1]
FILE_PATH=sys.argv[2]

solve=getattr(sys.modules[__name__],"solve_"+RIDDLE_NUMBER)
main()
