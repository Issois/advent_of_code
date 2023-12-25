import numpy as np


EMPTY=0
WALL=1
ROCK=3
MAP={".":EMPTY,"#":WALL,"O":ROCK}
IMAP={v:k for k,v in MAP.items()}
def main():
	# with open("example1_136") as f:
	with open("input") as f:
		inp=f.read().split("\n")


	arr=np.array([[MAP[y] for y in x] for x in inp],dtype=int)

	N=1000000000
	arrs=[arr.copy()]
	for cycles in range(1,N+1):
		twirl(arr)
		print(f"{cycles} cycles done.")

		found=False
		for prev_cycles,prev_arr in enumerate(arrs):
			if np.all(prev_arr==arr):
				print(f"After {cycles} cycles in same state as after {prev_cycles} cycles.")
				found=True
				break
		if not found:
			arrs.append(arr.copy())
		else:
			break
			# pass
	cycle_cycle=cycles-prev_cycles
	target_cycles=N%cycle_cycle
	if target_cycles<prev_cycles:
		print(f"And don't forget to add {cycle_cycle} if under {prev_cycles} ;)")
		target_cycles+=cycle_cycle
	print(f"Therefore with cc {cycle_cycle} after {N} cycles in same state as after {target_cycles} cycles.")

	arr=arrs[target_cycles]

	arr=(arr==ROCK).astype(int)
	weights=(np.arange(arr.shape[0])+1)[::-1]
	weights=(weights*np.ones(arr.shape,dtype=int)).T
	print(f"ANSWER: {np.sum(weights*arr)}")

def twirl(arr):
	for _ in range(4):
		arr=move_up(arr)
		arr=np.rot90(arr,axes=(1,0))
	return arr

# def move_up_fast(arr):
# 	row_count,col_count=arr.shape
# 	total_rocks=np.zeros((col_count),dtype=int)
# 	wall_filter_all=arr==WALL
# 	for row_idx in range(row_count-1,-1,-1):
# 		rock_filter=arr[row_idx]==ROCK
# 		# if np.any():
# 		wall_indices=np.nonzero(wall_filter_all[row_idx])[0]
# 		print(wall_indices)
# 		print(total_rocks[wall_indices])

# 		arr[row_idx,rock_filter]=EMPTY
# 		total_rocks+=rock_filter
# 		# ...


def move_up(arr):
	switches=1
	while switches>0:
		arr,switches=move_up_once(arr)
	return arr

def move_up_once(arr):
	diff=arr[1:,]-arr[:-1,]
	switch_to_rock=np.nonzero(diff==ROCK)
	switch_to_empty=(switch_to_rock[0]+1,switch_to_rock[1])
	arr[switch_to_rock]=ROCK
	arr[switch_to_empty]=EMPTY

	switches=switch_to_rock[0].shape[0]
	return arr,switches


main()