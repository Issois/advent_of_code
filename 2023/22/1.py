
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

	loz_grp=[[] for _ in range(maximum[Z])]
	for bl_idx,loz in enumerate(lo[:,Z]):
		# if loz not in loz_grp:
			# loz_grp[loz]=[]
		loz_grp[loz].append(bl_idx)

	print(loz_grp)


	supports={}
	is_supported_by={}

	field=np.zeros((*maximum[XY],2),dtype=int)

	field[:,:,BLK_IDX]=-1


	for height,block_indices in enumerate(loz_grp):
		if len(block_indices)>0:
			for bidx in block_indices:
				print(height,blocks[bidx])


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
