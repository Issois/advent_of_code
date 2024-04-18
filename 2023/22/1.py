
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

	delta=blocks[:,B,:]-blocks[:,A,:]
	# print(delta)
	# delta[delta!=0]=
	# idx=0

	full_blocks=[set() for _ in range(blocks.shape[0])]

	for idx in range(blocks.shape[0]):

		abs_delta=np.abs(delta)
		orientation=np.nonzero(delta)[1]
		# print(orientation)
		# print(abs_delta)
		# print(abs_delta[idx,orientation[idx]])
		# locs=set()
		for around_block in range(abs_delta[idx,orientation[idx]]+1):
			loc=blocks[idx,A,:].copy()
			loc[orientation[idx]]+=(delta[idx,orientation[idx]]/abs_delta[idx,orientation[idx]])*around_block
			# print(loc)
			full_blocks[idx].add(tuple(loc[XY]))
		# print(locs)

	# print(full_blocks)


	# return


	supports={}
	is_supported_by={}

	field=np.zeros((2,*maximum[XY]),dtype=int)

	field[BLK_IDX,:,:]=-1


	for height,block_indices in enumerate(loz_grp):
		if len(block_indices)>0:
			for bidx in block_indices:
				# print(height,blocks[bidx])
				# block=blocks[bidx]
				max_h=-1

				for subblock in full_blocks[bidx]:
					print(subblock)
					print(field[:,*subblock])
					return
					field_h,field_bidx=field[:,subblock]
					print(field_h,field_bidx)
					if field_h>max_h:
						max_bidxs={field_bidx}
						max_h=field_h
					elif field_h==max_h:
						max_bidxs.add(field_bidx)

				print(max_bidxs)
				print(max_h)
				return




				# delta=block[A,:]-block[B,:]
				# delta[delta!=0]=1
				# orientation=np.nonzero(delta)[0]
				# if len(orientation)==0:
				# 	orientation=Z
				# else:
				# 	orientation=orientation[0]
				# locs=[]
				# if orientation==Z:
				# 	locs.append(block[A,(X,Y)])

				# print(locs)


				# Check if dz or dxy
				# print(orientation)


				# return


	# print(field)

	# block=blocks[0]
	# print(blocks[:,:,X])
	# lx=np.min(blocks[:,:,X],axis=1)
	# print(lo)
	# print(blocks[:,A,:])
	# print(blocks[:1])

	# blocks[:,:,X]-=13
	# blocks[:,:,Y]+=15
	# print(blocks)


	# blocks[:,:,X]-=minimum[X]
	# blocks[:,:,Y]-=minimum[Y]
	# print(blocks[:,:,[X,Y]])
	# print(minimum)
	# print(minimum[[X,Y]])



	# minimum=np.min(blocks[:,:,:],axis=(0,1))

	# maximum[X]-=minimum[X]
	# maximum[Y]-=minimum[Y]
	# np.max(blocks[:,:,:],axis=(0,1))


	# print(blocks)

	# print(minimum)
	# print(maximum)


	# xmin=np.min(blocks[:,:,X])



	# blocks_z=blocks[:,:,:-1]
	# is_equal=(blocks_z[:,A,:]-blocks_z[:,B,:])==0
	# # al=
	# is_equal[np.all(is_equal,axis=1),Y]=False
	# block_axis=1-np.nonzero(is_equal)[1]

	# # print(al)
	# # return
	# print(blocks_z[0]-blocks_z[1])

	# return

	# arr=[]
	# for line in inp:
	# 	pass

	# result=0
	# print(f"ANSWER: {result}")

# def collidesXY(blocks):




main()
