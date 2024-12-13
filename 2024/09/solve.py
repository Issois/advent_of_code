
import numpy as np
import sys
# import matplotlib.pyplot as plt
import pprint

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

	file_index=np.zeros(((len(inp)//2)+1,2),dtype=int)-1

	spaces={}
	biggest_space=0
	block_indices=np.insert(np.cumsum(inp),0,0)

	# print(file_index)
	# print(block_indices)

	for block_index,block_len in enumerate(inp):
		is_file=block_index%2==0
		if is_file:
			file_index[block_index//2]=(block_indices[block_index],block_len)
		else:
			if block_len>0:
				if block_len not in spaces:
					spaces[block_len]=[]
				spaces[block_len].append(block_indices[block_index])
				biggest_space=block_len if block_len>biggest_space else biggest_space

	
	# print(file_index)
	# pprint.pprint(spaces)
	# print(f"biggest space: {biggest_space}")
	with_print=False
	with_print=True
	# while True:
	for file_ident in range(file_index.shape[0]-1,0,-1):
		# input()
		file_pos,file_size=file_index[file_ident]
		# if with_print:
			# print(f"File @{file_ident}, {file_size} bytes",end="")
		# space_found=False
		leftmost_space_pos=None
		target_space_size=None
		for space_size in range(file_size,biggest_space+1):
			if space_size in spaces:
				space_pos=spaces[space_size][0]
				if space_pos<file_pos and (leftmost_space_pos is None or space_pos<leftmost_space_pos):
					leftmost_space_pos=space_pos
					target_space_size=space_size
		if leftmost_space_pos is not None:
			file_index[file_ident]=(spaces[target_space_size][0],file_size)
			if with_print:
				print(f"File @{file_ident}, {file_size} bytes: Found space left and moved to {file_index[file_ident,0]}")
			# space_found=True
			# break
				# else:
					# if with_print:
						# print(f": Found space right so no move {file_index[file_ident,0]}")
		# if space_found:
			space_pos=spaces[target_space_size].pop(0)
			if len(spaces[target_space_size])==0:
				del spaces[target_space_size]

			if target_space_size>file_size:
				# add new space in correct position in spaces.
				new_space_size=target_space_size-file_size
				new_space_pos=space_pos+file_size
				if new_space_size not in spaces:
					spaces[new_space_size]=[new_space_pos]
				else:
					# Possible optimization: Use binary search.
					for other_space_pos_index,other_space_pos in enumerate(spaces[new_space_size]):
						if new_space_pos<other_space_pos:
							spaces[new_space_size].insert(other_space_pos_index,new_space_pos)
							break

			if biggest_space not in spaces:
				biggest_space=0
				if len(spaces)>0:
					for space in spaces:
						biggest_space=space if space>biggest_space else biggest_space
			if biggest_space==0:
				break

			# if with_print:
				# print(file_index)
				# pprint.pprint(spaces)
				# print(f"biggest space: {biggest_space}")
		# else:
		# 	pass
		# 	if with_print:
		# 		print(": ...")
	# Calc checksum.
	for file_ident in range(file_index.shape[0]):
		file_pos,file_size=file_index[file_ident]
		for index in range(file_pos,file_pos+file_size):
			answer+=file_ident*index

	# 8668119806144 is too high.
	# 6440026877313 is too low.
	# 5869139897464 is also too low.
	# 6467290479134 is correct.
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
