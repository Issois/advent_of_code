
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(garden):
	answer=0

	searched=np.zeros_like(garden,dtype=int)
	# x=
	while (nonsearched:=np.array(np.nonzero(1-searched)).T).shape[0]>0:
		pos=nonsearched[0]
		plant=garden[tuple(pos)]
		area=0
		border=0

		check_list=set([tuple(pos)])
		while len(check_list)>0:
			pos_tup=check_list.pop()
			searched[pos_tup]=1
			area+=1
			for dire in DIREV[::2]:
				new_pos=np.array(pos_tup)+dire
				new_pos_tup=tuple(new_pos)
				if not is_in_range(new_pos,garden) or garden[new_pos_tup]!=plant:
					border+=1
				else:
					if searched[new_pos_tup]==0:
						check_list.add(new_pos_tup)

		answer+=area*border

	# 1546338 is correct.
	return answer


def solve_2(garden):
	answer=0

	searched=np.zeros_like(garden,dtype=int)

	while (nonsearched:=np.array(np.nonzero(1-searched)).T).shape[0]>0:
		pos=nonsearched[0]
		plant=garden[tuple(pos)]
		area=0
		border_count=0
		borders=[]

		check_list=set([tuple(pos)])
		while len(check_list)>0:
			pos_tup=check_list.pop()
			searched[pos_tup]=1
			area+=1
			for dire in range(0,8,2):
				new_pos=np.array(pos_tup)+DIREV[dire]
				new_pos_tup=tuple(new_pos)
				if not is_in_range(new_pos,garden) or garden[new_pos_tup]!=plant:

					borders.append((pos_tup,dire))
				else:
					if searched[new_pos_tup]==0:
						check_list.add(new_pos_tup)

		borders_grouped={dire:[] for dire in range(0,8,2)}

		for pos_tup,dire in borders:
			borders_grouped[dire].append(np.array(pos_tup))

		for dire,borders in borders_grouped.items():
			check_dire=DIREV[(dire+2)%8]
			groups=[]

			for border_index_1 in range(len(borders)):
				for border_index_2 in range(border_index_1,len(borders)):
					if np.all(borders[border_index_1]+check_dire==borders[border_index_2]) or np.all(borders[border_index_1]-check_dire==borders[border_index_2]):
						groups.append(set([border_index_1,border_index_2]))

			group_index=1
			while group_index<len(groups):
				found=[]
				for comp_index in range(group_index-1,-1,-1):
					if len(groups[group_index]&groups[comp_index])>0:
						found.append(comp_index)
				for found_index in found:
					groups[group_index].update(groups[found_index])
				for found_index in found:
					groups.pop(found_index)
					group_index-=1
				group_index+=1
			borders=set(range(len(borders)))
			for group in groups:
				borders=borders-group
			border_count+=len(borders)+len(groups)
		answer+=border_count*area

	# 979863 is too high.
	# 978590 is correct.
	return answer


def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")
	return np.array([list(row) for row in inp])


def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)

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
