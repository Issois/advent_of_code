
import numpy as np
import sys
# import matplotlib.pyplot as plt

def get_section_index_from_index(index,sections):
	return np.nonzero(index<sections)[0][0]


def solve_1(inp):
	answer=0
	total_length=np.sum(inp)
	print("len:",total_length)
	sections=np.cumsum(inp)

	backward_index=total_length-1
	while (backward_section_index:=get_section_index_from_index(backward_index,sections))%2==1:
		backward_index-=1

	for forward_index in range(total_length):
		forward_section_index=get_section_index_from_index(forward_index,sections)
		is_space=forward_section_index%2==1
		if backward_index<forward_index:
			break

		if is_space:
			file=backward_section_index//2
			backward_index-=1
			while (backward_section_index:=get_section_index_from_index(backward_index,sections))%2==1:
				backward_index-=1
		else:
			file=forward_section_index//2
		answer+=forward_index*file

	# 6433134381063 is too high.
	# 6432869891895 is correct.
	return answer

def solve_2(inp):

	answer=0

	total_length=np.sum(inp)
	memory=np.zeros((total_length),dtype=int)-1
	insert_index=0
	print(inp)
	for index,length in enumerate(inp):
		if index%2==0:
			memory[insert_index:insert_index+length]=index//2
		insert_index+=length

	memory_str=memory.astype(str)
	memory_str[memory==-1]=" "
	print("".join(memory_str))

	spaces=dict(zip(*np.unique(inp,return_counts=True)))

	# return

	# answer=0

	# # spaces_arr=

	# print(spaces)
	# # for x in :
	# # 	print(x)

	# total_length=np.sum(inp)
	# print("len:",total_length)
	# sections=np.cumsum(inp)
	# # print(inp)
	# # return
	# backward_index=total_length-1
	# while (backward_section_index:=get_section_index_from_index(backward_index,sections))%2==1:
	# 	backward_index-=1

	# for forward_index in range(total_length):
	# 	print(f"{forward_index=}")
	# 	forward_section_index=get_section_index_from_index(forward_index,sections)
	# 	is_space=forward_section_index%2==1
	# 	if backward_index<forward_index:
	# 		break

	# 	if is_space:
	# 		file=backward_section_index//2
	# 		file_len=inp[backward_section_index]
	# 		if file_len
	# 		print(file,file_len)
	# 		return
	# 		# backward_index-=1
	# 		# while (backward_section_index:=get_section_index_from_index(backward_index,sections))%2==1:
	# 			# backward_index-=1
	# 	else:
	# 		file=forward_section_index//2
	# 	answer+=forward_index*file

	# 6433134381063 is too high.
	# 6432869891895 is correct.
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=np.array([int(ch) for ch in f.read()])
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
