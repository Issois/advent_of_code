
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

	# full_blocks=[set() for _ in range(blocks.shape[0])]
	full_blocks=[[] for _ in range(blocks.shape[0])]

	for idx in range(blocks.shape[0]):

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
	# for idx in range(blocks.shape[0]):

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
	blocks_that_can_be_deleted=set()

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


	# print(over)
	# print(under)

	for block in range(-1,blocks.shape[0]):
		# for block_over in over[block]:
		# 	if block not in under[block_over]:
		# 		print(f"ERROR {block} {block_over}")
		# 	else:
		# 		print(f"CORRC {block} {block_over}")

		can_be_deleted=False

		if len(over[block])==0:
			print(f"DEL {block:4.0f}: It supports nothing, it can be deleted. (supported by {under[block]})")
			can_be_deleted=True
		else:
			can_be_deleted=True
			for block_over in over[block]:
				# print(block_over)
				if len(under[block_over])==1:
					print(f"___ {block:4.0f}: Only {block} supports {block_over} so {block} can not be deleted.")
					can_be_deleted=False
					break
			if can_be_deleted:
				print(f"DEL {block:4.0f}: All blocks supported by {block} are supported by an additional block, {block} can be deleted.")
				for block_over in over[block]:
					print(f"  - {block:4.0f}: {block:4.0f} supports {block_over} which is supported by {under[block_over]}.")
		if can_be_deleted:
			blocks_that_can_be_deleted|={block}

	answer=len(blocks_that_can_be_deleted)

	print(f"ANSWER: {answer}")

	# 582 is too high.
	# 462 is too high.
	# 448 is correct!





main()
