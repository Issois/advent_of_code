
import numpy as np
import sys
# import matplotlib.pyplot as plt

def gauss_sum(n):
	return ((n**2)+n)//2

def gauss_sum2(min,max):
	return gauss_sum(max)-gauss_sum(min-1)

def solve_1(inp):
	# arr=[[int(num) for num in inner.split("-")] for inner in inp[0].split(",")]
	arr=[inner.split("-") for inner in ("".join(inp)).split(",")]
	answer=0
	print(arr)
	for a,b in arr:
		# print("ab: ",a,b)
		# print("diff: ",int(b)-int(a))
		diff=len(b)-len(a)
		# ASSUME 0<=diff<=1
		# print(diff)
		if diff==0:
			if len(a)%2!=0:
				continue
		else:
			if len(a)%2==0:
				b="9"*len(a)
			else:
				a="1"+("0"*(len(b)-1))
		l=len(a)
		nums_str=[
			a[:l//2],a[l//2:],
			b[:l//2],b[l//2:],
		]
		nums=[int(num) for num in nums_str]
		if nums[0]<nums[1]:
			nums[0]+=1
		if nums[2]>nums[3]:
			nums[2]-=1
		hdiff=nums[2]-nums[0]
		print("halves: ",a,b,nums[0::2],hdiff)
		hlen=len(nums_str[0])
		gsum=gauss_sum2(nums[0],nums[2])
		xgsum=gsum*(10**hlen)
		print("Adding: ",gsum,xgsum)
		answer+=gsum+xgsum

		# 391664560577835 is too high.
		# 13919717792 is correct.	

	return answer


def solve_2(inp):
	answer=0
	return answer

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
