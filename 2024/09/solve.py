
import numpy as np
import sys
# import matplotlib.pyplot as plt

def get_section_index_from_index(index,sections):
	return np.nonzero(index<sections)[0][0]


def solve_1(inp):
	answer=0
	total_length=np.sum(inp)
	print("len:",total_length)
	# sections=np.insert(np.cumsum(inp),0,0)
	sections=np.cumsum(inp)
	# is_space=np.arange(sections.shape[0])%2==1
	# is_file=np.logical_not(is_space)
	# print(is_space)
	# print(sections)
	# print(sections[is_space])
	# print()
	# result=np.zeros((total_length,2),dtype=int)


	backward_index=total_length-1
	while (backward_section_index:=get_section_index_from_index(backward_index,sections))%2==1:
		backward_index-=1


	for forward_index in range(total_length):
		forward_section_index=get_section_index_from_index(forward_index,sections)
		# print(forward_index,)
		# continue
		# if forward_index>backward_index:
			# print(forward_index,backward_index)
			# break
		# while forward_index>=sections[forward_section_index]:
		# 	forward_section_index+=1
		# print(forward_section_index)
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
		# result[forward_index,:]=(forward_index,file)
		# print(f"idx {forward_index} * {file}")

		# index_in_sections=np.nonzero(forward_index<sections)[0][0]-1
		# print(index_in_sections)
		# if is
		# pass


	# 6433134381063 is too high.
	# 6432869891895 is correct.
	return answer

def solve_2(inp):
	answer=0
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
