
import numpy as np
import sys
import matplotlib.pyplot as plt

X=0
Y=1
DIRE=np.array([
	[-1, 0],
	[-1, 1],
	[ 0, 1],
	[ 1, 1],
	[ 1, 0],
	[ 1,-1],
	[ 0,-1],
	[-1,-1],
])


def main():
	with open(sys.argv[2]) as f:
		inp=f.read().split("\n")
	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]
	
	inp=[list(line) for line in inp]
	inp=np.array(inp)
	hasht=inp=="#"
	point=inp=="."
	inp[point]=0
	inp[hasht]=2
	start=np.logical_not(np.logical_or(point,hasht))
	start=np.nonzero(start)
	start=np.array((start[X][0],start[Y][0]))
	dire=inp[tuple(start)]
	dire={"^":0,">":2,"v":4,"<":6}[dire]
	inp[tuple(start)]=0
	inp=inp.astype(int)

	print(f"ANSWER: {solve(inp,start,dire)}")

def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)

def solve_1(inp,start,dire):
	answer=-1
	pos=start
	left_the_field=False
	max_steps=inp.shape[X]*inp.shape[Y]
	steps=0

	while(steps<max_steps):
		steps+=1
		inp[tuple(pos)]=1
		new_pos=pos+DIRE[dire]

		if not is_in_range(new_pos,inp):
			left_the_field=True
			break

		if inp[tuple(new_pos)]==2:
			dire=(dire+2)%8
		else:
			pos=new_pos

	if left_the_field:
		answer=np.sum(inp==1)
	else:
		print("too much steps")

	plt.imshow(inp)
	plt.show()

	# 5242
	return answer

def solve_2(inp,start,dire):
	answer=None
	return answer

main()
