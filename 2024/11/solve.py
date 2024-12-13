
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
	if old_stone==0:
		return [1]
	elif (stone_len:=len(stone_str:=str(old_stone)))%2==0:
		return [int(stone_str[:stone_len//2]),int(stone_str[stone_len//2:])]
	else:
		return [old_stone*2024]


def solve_2(inp):
	answer=0
	
	total_blink_count=75
	
	graph={}
	stones=inp.copy()
	while len(stones)>0:
		stone=stones.pop()
		new_stones=generate_new_stones(stone)
		if stone not in graph:
			graph[stone]=new_stones
			stones.extend(new_stones)
	
	blinks={stone:{0:1} for stone in graph}
	stones=inp.copy()

	for sidx,stone in enumerate(stones):
		print(sidx,stone)
		check_list=[(stone,total_blink_count)]
		while len(check_list)>0:
			cur_stone,cur_blink_count=check_list[-1]

			if cur_blink_count not in blinks[cur_stone]:
				children=graph[cur_stone]
				every_child_checked=True
				for child in children:
					if cur_blink_count-1 not in blinks[child]:
						check_list.append((child,cur_blink_count-1))
						every_child_checked=False
				
				if every_child_checked:
					blinks[cur_stone][cur_blink_count]=0
					for child in children:
						blinks[cur_stone][cur_blink_count]+=blinks[child][cur_blink_count-1]
					check_list.pop()
			else:
				check_list.pop()

	for stone in stones:
		answer+=blinks[stone][total_blink_count]

	# 236804088748754 is correct.
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split(" ")
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
