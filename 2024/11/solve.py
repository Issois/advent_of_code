
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(inp):
	answer=0
	
	blink_count=25
	stones=inp
	for _ in range(blink_count):
		# print(_)
		new_stones=[]
		for stone in stones:
			if stone==0:
				new_stones.append(1)
				pass
			elif (stone_len:=len(stone_str:=str(stone)))%2==0:
				new_stones.append(int(stone_str[:stone_len//2]))
				new_stones.append(int(stone_str[stone_len//2:]))
			else:
				new_stones.append(stone*2024)
		stones=new_stones

	# 199986 is correct.
	answer=len(stones)


	return answer

def generate_new_stones(old_stone):
	# new_stones=[]
	if old_stone==0:
		return [1]
	elif (stone_len:=len(stone_str:=str(old_stone)))%2==0:
		return [int(stone_str[:stone_len//2]),int(stone_str[stone_len//2:])]
	else:
		return [old_stone*2024]
	# return new_stones


def solve_2(inp):
	answer=0
	
	graph={}
	stones=inp.copy()
	while len(stones)>0:
		print(len(stones))
		stone=stones.pop()
		new_stones=generate_new_stones(stone)
		if stone not in graph:
			graph[stone]=new_stones
			stones.extend(new_stones)
	
	# blinks
	
	blinks={stone:{} for stone in graph}
	# print(len(graph))

	for stone in stones:
		# blink_count=75
		# cur_stone=stone
		check_list=[(stone,75)]
		while len(check_list)>0:
			cur_stone,cur_blink_count=check_list[-1]


			# if cur_stone not in blinks:
			# 	blinks[cur_stone]={}
			if cur_blink_count not in blinks[cur_stone]:
				children=graph[cur_stone]
				for child in children:

					check_list.append((child,cur_blink_count-1))
			else:
				pass

			# blinks[cur_stone][cur_blink_count]=None


	# stone=inp[0]
	# for stone in inp:



	# loop_size=0
	# visited=set()
	# path=[]
	# while stone not in visited:
	# 	visited.add(stone)
	# 	path.append(stone)
	# 	stone=graph[stone][0]
	
	# print(path,stone)
	# print(len(path))

	# v(x,n)=v(c1(x),n-1)+v(c2(x),n-1)
	# v(x,0)=1


	# for k,v in graph.items():
	# from pprint import pprint
	# pprint(graph)
		# if v.
	

		



	
	# blink_count=75
	# stones=inp
	# prev_stones=set()

	# for _ in range(blink_count):
	# 	print(_,len(stones))
	# 	new_stones=[]
	# 	prev_stones.update(stones)
	# 	for stone in stones:
	# 		if stone==0:
	# 			new_stones.append(1)
	# 			pass
	# 		elif (stone_len:=len(stone_str:=str(stone)))%2==0:
	# 			for new_stone in [int(stone_str[:stone_len//2]),int(stone_str[stone_len//2:])]:
	# 				if new_stone not in prev_stones:
	# 					new_stones.append(new_stone)
	# 			# new_stones.append(int(stone_str[stone_len//2:]))
	# 		else:
	# 			new_stone=stone*2024
	# 			if new_stone not in prev_stones:
	# 				new_stones.append(new_stone)
	# 	stones=new_stones

	answer=len(stones)

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
