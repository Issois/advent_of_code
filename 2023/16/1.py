
import numpy as np
import sys


def array(*vals):
	return np.array(vals)


EM=0
HO=1
VE=2
SL=3
BA=4

DICT={
	EM:".",
	HO:"-",
	VE:"|",
	SL:"/",
	BA:"\\"
}

NO=0
EA=1
SO=2
WE=3

DIRE={
	NO=array(-1, 0)
	EA=array( 0, 1)
	SO=array( 1, 0)
	WE=array( 0,-1)

}

def main():
	with open("example1" if "e" in sys.argv else "input") as f:
		inp=np.array([list(x) for x in f.read().split("\n")])

	FILT={k:inp==v for k,v in DICT.items() if k!=EM}

	arr=np.zeros(inp.shape,dtype=int)

	for key,filt in FILT.items():
		arr[filt]=key

	r=7
	c=4
	# NO
	print(arr[:r+1,c][::-1])
	# EA
	print(arr[r,c:])
	# SO
	print(arr[r:,c])
	# WE
	print(arr[r,:c+1][::-1])

	return

	hits=fire_beam(arr,array(0,-1),EA)

	print(hits)


	# print(inp)



	result=0
	print(f"ANSWER: {result}")

def fire_beam(arr,start_position,dire):
	hit_positions=[]
	start=start_position+dire
	print(start)

	return hit_positions






main()
