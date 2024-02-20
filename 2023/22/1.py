
import numpy as np
import sys

X=0
Y=1
Z=2

A=0
B=1

# IDX=0


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
	# block=blocks[0]
	blocks_z=blocks[:,:,:-1]
	is_equal=(blocks_z[:,A,:]-blocks_z[:,B,:])==0
	# al=
	is_equal[np.all(is_equal,axis=1),Y]=False
	block_axis=1-np.nonzero(is_equal)[1]

	# print(al)
	# return
	print(blocks_z[0]-blocks_z[1])

	return

	result=0
	arr=[]
	for line in inp:
		pass

	print(f"ANSWER: {result}")

def collideXY(blocks):
	if blocks[1,A,X]<block[0,A,X]:
		if blocks[1,A,X]<block[0,B,X]:
			pass



main()
