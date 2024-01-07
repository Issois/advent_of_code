import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from scipy.signal import convolve2d
import numpy as np
import sys



def array(*vals):
	return np.array(vals)


ROW=0
COL=1
DIRE=2
LEVEL=3

DIRE_COUNT=4
LEVEL_COUNT=10

NO=0
EA=1
SO=2
WE=3


OFFS=0
NAME=1

OFFS_FROM_DIRE={
	NO:(array(-1, 0),"NO"),
	EA:(array( 0, 1),"EA"),
	SO:(array( 1, 0),"SO"),
	WE:(array( 0,-1),"WE"),
}

def main():
	with open("example1.input" if "e" in sys.argv else "data.input") as f:
		cost=np.array([[int(y) for y in x] for x in f.read().split("\n")])
	result=0
	sub=7
	# result=find_path(cost)
	result=find_path(cost)

	print(f"ANSWER: {result}")

def find_path(cost):

	max_int=np.iinfo(np.int64).max
	total=np.zeros((*cost.shape,DIRE_COUNT,LEVEL_COUNT),dtype=np.int64)+max_int
	total[0,0,:,:]=0

	print("Get all neighbours.")
	neighbours_from_loc=get_all_neighbours(cost)

	max_checks=len(neighbours_from_loc)

	sorted_checks=sorted(neighbours_from_loc,key=lambda elem:elem[ROW]+elem[COL])
	needs_to_be_checked=np.zeros((max_checks),dtype=bool)
	index_from_location={loc:idx for idx,loc in enumerate(sorted_checks)}


	meta=cost,total,neighbours_from_loc

	start_checks=[(0,1,EA,0),(1,0,SO,0)]
	for location in start_checks:
		total[location]=cost[location[ROW],location[COL]]
		needs_to_be_checked[index_from_location[location]]=True

	round_count=0
	check_indices=np.nonzero(needs_to_be_checked)[0]
	check_count=check_indices.shape[0]
	while check_count>0:
		round_count+=1
		print(f"R: {round_count}, Checks: {check_count}")
		for check_index in check_indices:
			needs_to_be_checked[check_index]=False
			location=sorted_checks[check_index]
			for neigh in update_neighbours(location,meta):
				needs_to_be_checked[index_from_location[neigh]]=True

		check_indices=np.nonzero(needs_to_be_checked)[0]
		check_count=check_indices.shape[0]

	return np.min(total[-1,-1,:,:])

def update_neighbours(location,meta):
	cost,total,neighbours_from_loc=meta
	this_total=total[location]
	neighbours_to_check=[]
	# print(total[0,0,:,:])
	for neigh in neighbours_from_loc[location]:
		neigh_total=total[neigh]
		# print(total[neigh[ROW],neigh[COL],:,:])
		neigh_cost=cost[neigh[ROW],neigh[COL]]
		new_neigh_total=this_total+neigh_cost
		# print(f"{new_neigh_total=},{neigh_total=},{loc_str(neigh)=}")
		if new_neigh_total<neigh_total:
			total[neigh]=new_neigh_total
			neighbours_to_check.append(neigh)
	return neighbours_to_check

def get_all_neighbours(cost):
	neighbours_from_loc={}
	rc=np.array(np.nonzero(cost))[:,1:].T
	allowed_positions=set([tuple(x) for x in rc])
	# count=0
	rc_count=rc.shape[0]
	loop_counter=0
	for rc_index,(row,col) in enumerate(rc):
		loop_counter+=1
		if loop_counter%1000==0:
			print(f"{rc_index+1}/{rc_count}")
		for dire in range(DIRE_COUNT):
			for level in range(LEVEL_COUNT):
				# print(level)
				location=(row,col,dire,level)
				# count+=1

				if dire==SO:
					if level>=row:
						# print(f"{loc_str(location)}: level can not be reached.")
						continue

				if dire==EA:
					if level>=col:
						# print(f"{loc_str(location)}: level can not be reached.")
						continue

				if dire==NO:
					delta=(cost.shape[ROW]-1)-row
					if level>=delta:
						# print(f"{loc_str(location)}: level can not be reached.")
						continue

				if dire==WE:
					delta=(cost.shape[COL]-1)-col
					if level>=delta:
						# print(f"{loc_str(location)}: level can not be reached.")
						continue


				neighbours=[]
				for neigh_dire in OFFS_FROM_DIRE:
					dire_delta=(neigh_dire-dire)%4

					dont_go_back=dire_delta!=2
					if not dont_go_back: continue

					min_lvl4_for_turn=dire_delta==0 or level>=3
					if not min_lvl4_for_turn: continue

					neigh_level=level+1 if dire_delta==0 else 0
					max_lvl10_for_straight=neigh_level<=9
					if not max_lvl10_for_straight: continue

					neigh_row,neigh_col=array(row,col)+OFFS_FROM_DIRE[neigh_dire][OFFS]
					inside_field=(neigh_row,neigh_col) in allowed_positions
					if not inside_field: continue


					neighbours.append((neigh_row,neigh_col,neigh_dire,neigh_level))

				neighbours_from_loc[location]=neighbours

	return neighbours_from_loc

def loc_str(location):
	# print(location[DIRE])
	return f"({location[ROW]:3},{location[COL]:3}) {OFFS_FROM_DIRE[location[DIRE]][NAME]}, LV{location[LEVEL]+1}"

main()
