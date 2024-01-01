import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from scipy.signal import convolve2d
import numpy as np
import sys



def array(*vals):
	return np.array(vals)


ROW=0
COL=1

POS=0
DIRE=1
LEVEL=2
TDIRE=2
TLEVEL=3

DIRE_COUNT=4
LEVEL_COUNT=3

NO=0
EA=1
SO=2
WE=3

LV1=0
LV2=1
LV3=2

OFFS=0
NAME=1

OFFS_FROM_DIRE={
	NO:(array(-1, 0),"NO"),
	EA:(array( 0, 1),"EA"),
	SO:(array( 1, 0),"SO"),
	WE:(array( 0,-1),"WE"),
}

def main():
	with open("example1" if "e" in sys.argv else "input") as f:
		cost=np.array([[int(y) for y in x] for x in f.read().split("\n")])
	result=0
	# plt.imshow(cost)
	# plt.show()
	# return
	sub=7
	# result=find_path1(cost[:sub,:sub])
	# result=find_path2(cost[:sub,:sub])
	result=find_path2(cost)

	print(f"ANSWER: {result}")

def find_path2(cost):

	max_int=np.iinfo(np.int64).max
	total=np.zeros((*cost.shape,DIRE_COUNT,LEVEL_COUNT),dtype=np.int64)+max_int
	total[0,0,:,:]=0

	print("Get all neighbours.")
	neighbours_from_loc=get_all_neighbours(cost)

	max_checks=len(neighbours_from_loc)

	sorted_checks=sorted(neighbours_from_loc,key=lambda elem:elem[ROW]+elem[COL])
	needs_to_be_checked=np.zeros((max_checks),dtype=bool)
	index_from_location={loc:idx for idx,loc in enumerate(sorted_checks)}

	# for loc,idx in index_from_location.items():
		# print(f"{loc=},{idx=}")
	# return




	meta=cost,total,neighbours_from_loc

	start_checks=[(0,1,EA,LV1),(1,0,SO,LV1)]
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
			# print(f"[{number_of_checks}] {loct_str(location)}. Q:{len(checks)}")
		# checks.extend()

	# print(f"max possible checks {max_checks}")
	# print(len(neighbours_from_loc))

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
		# print(f"{new_neigh_total=},{neigh_total=},{loct_str(neigh)=}")
		if new_neigh_total<neigh_total:
			total[neigh]=new_neigh_total
			neighbours_to_check.append(neigh)
	return neighbours_to_check

def find_path1(cost):

	total=np.zeros((*cost.shape,4,3),dtype=np.int32)+np.iinfo(np.int32).max
	# total=np.zeros((*cost.shape,4,3))
	# total[:,:,:,:]=np.nan

	# total[0,0,]=0
	# print(cost[:2,:2])
	# checks=np.nonzero(total)
	# checks=[(r,c) for r,c in zip(*checks)][::-1]
	checks=[(array(0,1),EA,LV1),(array(1,0),SO,LV1)]
	currently_staged=set()
	for location in checks:
		loc_tup=(*location[POS],*location[DIRE:])
		total[loc_tup]=cost[tuple(location[POS])]
		currently_staged.add(loc_tup)


	check_count={}
	total_checks=cost.shape[ROW]*cost.shape[COL]*4*3


	number_of_checks=0
	unique_checks=0

	while len(checks)>0:
		location=checks.pop()
		loc_tup=(*location[POS],*location[DIRE:])
		currently_staged.remove(loc_tup)

		if loc_tup not in check_count:
			check_count[loc_tup]=0
		check_count[loc_tup]+=1

		number_of_checks+=1
		if number_of_checks%1000==0:
			print(f"Checked {number_of_checks} total. {len(checks)} in queue.")


		new_unique_checks=len(check_count)
		if new_unique_checks>unique_checks+100:
			unique_checks=new_unique_checks
			print(f"Checked {unique_checks} out of {total_checks}")

		# if unique_checks%1000==0:

		this_total=total[loc_tup]
		# get_total(total,location)
		# print(f"Checking {loc_str(location)}={this_total}")
		for neigh in get_neighbours(location,cost.shape):
			neigh_tup=(*neigh[POS],*neigh[DIRE:])
			neigh_total=total[neigh_tup]
			# print(neigh_total)
			neigh_cost=cost[tuple(neigh[POS])]
			new_neigh_total=this_total+neigh_cost
			# if np.isnan(neigh_total):
			if new_neigh_total<neigh_total:
				# print(f"  Found better path for: {loc_str(neigh)} from {neigh_total} down to {new_neigh_total}.")
				total[neigh_tup]=new_neigh_total

				if neigh_tup not in currently_staged:
					checks.append(neigh)
					currently_staged.add(neigh_tup)

	return np.min(total[-1,-1,:,:])


def get_all_neighbours(cost):
	neighbours_from_loc={}
	rc=np.array(np.nonzero(cost))[:,1:].T
	allowed_positions=set([tuple(x) for x in rc])
	count=0
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
				count+=1

				if dire==SO:
					if level>=row:
						# print(f"{loct_str(location)}: level can not be reached.")
						continue

				if dire==EA:
					if level>=col:
						# print(f"{loct_str(location)}: level can not be reached.")
						continue

				if dire==NO:
					delta=(cost.shape[ROW]-1)-row
					if level>=delta:
						# print(f"{loct_str(location)}: level can not be reached.")
						continue

				if dire==WE:
					delta=(cost.shape[COL]-1)-col
					if level>=delta:
						# print(f"{loct_str(location)}: level can not be reached.")
						continue


				neighbours=[]
				for neigh_dire in OFFS_FROM_DIRE:
					if (neigh_dire-dire)%4!=2:
						neigh_level=level+1 if dire==neigh_dire else LV1
						if neigh_level<=LV3:
							neigh_row,neigh_col=array(row,col)+OFFS_FROM_DIRE[neigh_dire][OFFS]
							# is_inside=0<=neigh_pos[ROW]<cost.shape[ROW] and 0<=neigh_pos[COL]<cost.shape[COL]
							if (neigh_row,neigh_col) in allowed_positions:
								neighbours.append((neigh_row,neigh_col,neigh_dire,neigh_level))

				# print(f"Added {loct_str(location)} with {len(neighbours)} neighbours.")
				neighbours_from_loc[location]=neighbours
	return neighbours_from_loc

def loct_str(location):
	# print(location[TDIRE])
	return f"({location[ROW]:3},{location[COL]:3}) {OFFS_FROM_DIRE[location[TDIRE]][NAME]}, LV{location[TLEVEL]+1}"

def loc_str(location):
	return f"({location[POS][ROW]:3},{location[POS][COL]:3}) {OFFS_FROM_DIRE[location[DIRE]][NAME]}-wards, LV{location[LEVEL]+1}"

def get_neighbours(location,shape):
	# not OOB
	# not opposite dire
	# level<=3
	# if same dire:
	#  level+1
	# else:
	#  level=1
	new_locations=[]

	if np.all(location[POS]==(array(*shape)-1)):
		# print("   ARRIVED AT FINAL LOCATION")
		return new_locations

	allowed_dire_deltas=set([1,3])
	if location[LEVEL]<LV3:
		allowed_dire_deltas.add(0)

	for new_dire,(offs,name) in OFFS_FROM_DIRE.items():
		dire_delta=(new_dire-location[DIRE])%4
		if dire_delta in allowed_dire_deltas:
			new_pos=location[POS]+OFFS_FROM_DIRE[new_dire][OFFS]
			is_inside=0<=new_pos[ROW]<shape[ROW] and 0<=new_pos[COL]<shape[COL]
			if is_inside:
				new_level=location[LEVEL]+1 if location[DIRE]==new_dire else LV1
				new_locations.append((new_pos,new_dire,new_level))

	return new_locations



main()
		#

		# checlk




	# print(checks)

	# for row in range(total.shape[ROW]):
		# for col in range(total.shape[COL]):
		# 	# if
	# print(total)






	# img=np.zeros((50,50))
	# img[20,25]=1

	# fig,ax=plt.subplots()
	# kernel=np.array([0,1,1,1,0,1,0,1,0]).reshape((3,3))
	# # kernel=1-kernel
	# # kernel[1,1]=10
	# kernel=1.1*kernel/np.sum(kernel)

	# i=0

	# aximg=ax.imshow(img)


	# def update(frame):
	# 	nonlocal img,kernel,aximg,i
	# 	i+=1
	# 	if i>50:
	# 		kernel=1-kernel
	# 		i=0
	# 	img=convolve2d(img,kernel,mode="same",boundary="fill",fillvalue=0)
	# 	img[img>1]=1
	# 	aximg.set_data(img)
	# 	# print(img)
	# 	return None

	# ani=animation.FuncAnimation(fig=fig,func=update,frames=40,interval=20)

	# plt.show()


	# plt.imshow(img)
	# plt.show()






	# print(f"ANSWER: {result}")
