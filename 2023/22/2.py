
import numpy as np
import sys

X=0
Y=1
Z=2

XY=[X,Y]

A=0
B=1

# IDX=0

BLK_IDX=0
CURR_H=1

def main():
	with open(sys.argv[1]) as f:
		inp=f.read()

	blocks=np.array([
		[
			[
				int(coord) for coord in pos.split(",")
			] for pos in line.split("~")
		] for line in inp.split("\n")
	])

	# make x-y-coords non negative.
	minimum=np.min(blocks[:,:,:],axis=(0,1))
	maximum=np.max(blocks[:,:,:],axis=(0,1))

	blocks[:,:,XY]-=minimum[XY]
	maximum[XY]-=minimum[XY]
	minimum=np.zeros_like(minimum)

	# ...
	lo=np.min(blocks[:,:,:],axis=1)
	hi=np.max(blocks[:,:,:],axis=1)

	# print(lo[:Z])
	# print(lo)
	# print(hi)
	# return
	# print(maximum)
	loz_grp=[[] for _ in range(maximum[Z]+1)]
	for bl_idx,loz in enumerate(lo[:,Z]):
		# if loz not in loz_grp:
			# loz_grp[loz]=[]
		# print(loz)
		loz_grp[loz].append(bl_idx)

	# print(blocks[:,:,A])

	# for idx,lg in enumerate(loz_grp):
	# 	print(idx,lg)
	# return


	delta=blocks[:,B,:]-blocks[:,A,:]
	abs_delta=np.abs(delta)

	orientation=np.zeros(blocks.shape[0],dtype=int)-1

	for idx,row in enumerate(delta):
		nz=np.nonzero(row)[0]
		dim=len(nz)
		if dim==0:
			print(f"Row {idx+1}: Dim==0, set to 1->Z")
			orientation[idx]=Z
		elif dim==1:
			orientation[idx]=nz[0]
		else:
			print(f"Row {idx+1}: Dim==2 is invalid!")
			return


	# for idx,ori in enumerate(orientation[:50]):
	# 	print(idx,ori)

	# return

	all_block_ids=range(blocks.shape[0])

	# print(delta[22])
	# print(np.nonzero(delta[22]))
	# print(np.nonzero(delta[22])[1])
	# return
	# orientation=np.nonzero(delta)[1]
	# for delt in delta:
		# print(delt)
	# for idx,ori in enumerate(orientation[:50]):
		# print(idx,ori,delta[idx])
	# print(abs_delta)
	# print(delta)
	# delta[delta!=0]=
	# idx=0

	# full_blocks=[set() for _ in all_block_ids]
	full_blocks=[[] for _ in all_block_ids]

	for idx in all_block_ids:

		# print(abs_delta)
		# print(abs_delta[idx,orientation[idx]])
		# locs=set()
		start_block=blocks[idx,A,:]
		# print(idx,delta[idx,orientation[idx]],abs_delta[idx,orientation[idx]])
		# direction=delta[idx,orientation[idx]]/abs_delta[idx,orientation[idx]]
		# dir_vec=np.zeros((3))
		# dir_vec[orientation]=1
		for full_block_idx in range(abs_delta[idx,orientation[idx]]+1):
			# print(full_block_idx)
			# print(direction)
			block=start_block.copy()
			block[orientation[idx]]+=full_block_idx
			# print(block)
			full_blocks[idx].append(tuple(block[XY]))
		# print(locs)

	# Check if start and of full blocks match the corresponding entry.
	# for bid in all_block_ids:


	# return

	# print(full_blocks)


	# return


	under={i:set() for i in range(-1,blocks.shape[0])}
	over={i:set() for i in range(-1,blocks.shape[0])}

	field=np.zeros((2,*maximum[XY]+1),dtype=int)

	field[BLK_IDX,:,:]=-1
	# field[BLK_IDX,0,0]=10
	# field[BLK_IDX,1,0]=20
	# print(field)
	# print(full_blocks)

	for height,block_indices in enumerate(loz_grp):
		if len(block_indices)>0:
			for block_current in block_indices:
				# print(height,blocks[block_current])
				# block=blocks[block_current]
				max_h=-1


				for subblock in full_blocks[block_current]:
					# print(subblock)
					last_x,last_y=subblock
					# print()
					# return
					field_bidx,field_h=field[:,last_x,last_y]
					# print(field_h,field_bidx)
					if field_h>max_h:
						blocks_under={field_bidx}
						max_h=field_h
					elif field_h==max_h:
						blocks_under.add(field_bidx)

				# print(blocks_under)
				# print(max_h)
				under[block_current]|=blocks_under
				for block_under in blocks_under:
					over[block_under].add(block_current)

				if orientation[block_current]==Z:

					field[:,last_x,last_y]=block_current,max_h+len(full_blocks[block_current])
				else:
					for subblock in full_blocks[block_current]:
						field[:,subblock[X],subblock[Y]]=block_current,max_h+1

				# print(supports[bidx])
				# print(field[CURR_H])
				# print("######")
				# return

	marks={-1:set()}
	to_mark=list(over[-1])
	to_mark_set=set(to_mark)

	counts={bid:0 for bid in all_block_ids}
	counts[-1]=0

	# x={1,2}
	# y={1,3}
	# print(x|y)
	# print(x&y)
	# print(x^y)

	while len(to_mark)>0:
		block_current=to_mark.pop(0)
		print(f"Marking: {block_current} {to_mark}.")
		to_mark_set.remove(block_current)
		if under[block_current]<=set(marks.keys()):
			marks[block_current]=set.intersection(*[{block_under}|marks[block_under] for block_under in under[block_current]])
			for mark in marks[block_current]:
				counts[mark]+=1
			# print(f"Adding to mark: {over[block_current]}")
			to_mark.extend([bid for bid in over[block_current] if bid not in to_mark_set])
			to_mark_set|=over[block_current]
		else:
			print(f"Not all parents have been marked yet. Appending again.")
			to_mark.append(block_current)
			to_mark_set.add(block_current)

	# print(marks)
	# print(counts)
	answer=0
	for bid in all_block_ids:
		answer+=counts[bid]



	print(f"ANSWER: {answer}")

	# 57770 is correct.



main()
