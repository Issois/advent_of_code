
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

	# print(lo[:,Z])
	# print(maximum)
	loz_grp=[[] for _ in range(maximum[Z]+1)]
	for bl_idx,loz in enumerate(lo[:,Z]):
		# if loz not in loz_grp:
			# loz_grp[loz]=[]
		# print(loz)
		loz_grp[loz].append(bl_idx)

	# print(blocks[:,:,A])

	for idx,lg in enumerate(loz_grp):
		print(idx,lg)
	return


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

	full_blocks=[set() for _ in range(blocks.shape[0])]

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
			full_blocks[idx].add(tuple(block[XY]))
		# print(locs)

	# print(full_blocks)


	# return


	supports={i:set() for i in range(-1,blocks.shape[0])}
	is_supported_by={i:set() for i in range(-1,blocks.shape[0])}

	field=np.zeros((2,*maximum[XY]+1),dtype=int)

	field[BLK_IDX,:,:]=-1
	# field[BLK_IDX,0,0]=10
	# field[BLK_IDX,1,0]=20
	# print(field)
	# print(full_blocks)
	can_be_deleted=set()

	for height,block_indices in enumerate(loz_grp):
		if len(block_indices)>0:
			for bidx in block_indices:
				# print(height,blocks[bidx])
				# block=blocks[bidx]
				max_h=-1


				for subblock in full_blocks[bidx]:
					# print(subblock)
					last_x,last_y=subblock
					# print()
					# return
					field_bidx,field_h=field[:,last_x,last_y]
					# print(field_h,field_bidx)
					if field_h>max_h:
						supporting_bidxs={field_bidx}
						max_h=field_h
					elif field_h==max_h:
						supporting_bidxs.add(field_bidx)

				# print(supporting_bidxs)
				# print(max_h)
				supports[bidx]|=supporting_bidxs
				for supporting in supporting_bidxs:
					is_supported_by[supporting].add(bidx)

				if orientation[bidx]==Z:

					field[:,last_x,last_y]=bidx,max_h+len(full_blocks[bidx])
				else:
					for subblock in full_blocks[bidx]:
						field[:,subblock[X],subblock[Y]]=bidx,max_h+1

				# print(supports[bidx])
				# print(field[CURR_H])
				# print("######")
				# return
	for i in range(-1,blocks.shape[0]):
		if len(supports[i])>1:

			# print(f"{supports[i]} support {i}, they can be deleted.")
			can_be_deleted|=supports[i]
		if len(is_supported_by[i])==0:
			# print(f"{i} supports nothing, it can be deleted.")
			can_be_deleted|={i}

	# print(can_be_deleted)
	answer=len(can_be_deleted)

	print(f"ANSWER: {answer}")

	# 582 too high.





main()
