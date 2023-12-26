import numpy as np
def main():
	# with open("example1") as f:
	with open("input") as f:
		inp=f.read().split(",")

	asc=[[ord(y) for y in x] for x in inp]
	# print(asc)

	result=0
	for ords in asc:
		sub_result=hash_arr(ords)
		print(sub_result)
		result+=sub_result
	print(f"ANSWER: {result}")

def hash_arr(nums):
	s=0
	for num in nums:
		s=hash(num+s)
	return s
def hash(num):
	return (17*num)%256

main()