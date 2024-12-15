
import numpy as np
import sys
import re

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
	offset=10000000000000
	# offset=0
	pot=len(str(offset))-1
	# print(f"{pot=}")
	cost=np.array([3,1],dtype=int)

	for machine in machines:
		mat=machine[:2].T
		(a,b),(c,d)=mat
		det=(a*d)-(c*b)
		inv0=np.array([[d,-b],[-c,a]])

		inv=inv0/det

		inv=np.linalg.inv(mat)

		result_base=inv@machine[2].T

		result_add=[
			longdiv(d-b,det,prec=3*pot),
			longdiv(a-c,det,prec=3*pot),
		]
		nums={}
		for axis in [X,Y]:
			summ=result_base[axis]+small_num_from_decimals(result_add[axis][1][pot:])
			if close_to_int(summ,8):
				nums[axis]=int(result_base[axis]+big_num_from_decimals(result_add[axis][1][:pot]))+1

		if len(nums)==2:
			for axis in [X,Y]:
				answer+=nums[axis]*cost[axis]

	# 1040154114727100 is too high.
	# 104015411472710 is too low.
	# 104015411578548 is correct.
	return answer

def close_to_int(num,prec):
	decimals=num%1
	if decimals>0.5:
		decimals=1-decimals
	return decimals<10**-prec


def big_num_from_decimals(decimals):
	result=0
	# for idx in range(len(decimals)-1,-1,-1):
	for idx in range(len(decimals)):
		# print(type(decimals[idx]))
		result+=decimals[idx]*(10**(len(decimals)-1-idx))
	return result

def small_num_from_decimals(decimals):
	result=0

	for exp,decimal in enumerate(decimals):
		result+=decimal*(10**((-1)*(exp+1)))

	return result

def longdiv(a,b,prec=None):
	a=abs(a)
	b=abs(b)
	result=[0,[],False]
	div=a//b
	rest=a%b
	result[0]=div
	idx=1
	rests=set()
	while True:
		if prec is not None:
			if idx>=prec:
				break
		if rest in rests:
			result[2]=True
			if prec is None:
				break
		val=rest*10
		div=val//b
		rests.add(rest)
		rest=val%b
		result[1].append(int(div))
		idx+=1
	return result


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

	# for i in range(100):
	# 	print(10000000000000*(10**i))

	# return

	# i=np.arange(30,dtype=np.float)
	# x=np.float(0.5)+(np.float(10)**i)

	# print(np.nonzero(x%1<0.5)[0])
	# a=1
	# b=3
	# x=longdiv(a,b,400)
	# print(x)
	# print(a/b)

	# return


	inp=get_input(FILE_PATH)
	answer=solve(inp)
	print(f"ANSWER: {answer}")



X=0
Y=1

RIDDLE_NUMBER=sys.argv[1]
FILE_PATH=sys.argv[2]

solve=getattr(sys.modules[__name__],"solve_"+RIDDLE_NUMBER)
main()
