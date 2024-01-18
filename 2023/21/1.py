import matplotlib.pyplot as plt
import numpy as np
import scipy
import sys

X=0
Y=1

def main():
	step_count=6 if "e" in sys.argv else 64
	with open("example1.input" if "e" in sys.argv else "data.input") as f:
		inp=np.array([list(x) for x in f.read().split("\n")])

	st=np.nonzero(inp=="S")
	rk=np.nonzero(inp=="#")

	start_pos=(st[0][0],st[1][0])

	old_poss={start_pos}
	# new_poss=set()
	rest_poss=set()
	rocks={x for x in zip(*rk)}

	# print(old_new)
	# print(rocks)
	dirs=[[-1,0],[1,0],[0,1],[0,-1]]

	# step_count=15

	for step in range(step_count):
		new_poss=set()
		for old_pos in old_poss:
			for dx,dy in dirs:
				new_pos=old_pos[X]+dx,old_pos[Y]+dy
				if (
						0<=new_pos[X]<inp.shape[X]
						and 0<=new_pos[Y]<inp.shape[Y]
						and new_pos not in rocks
						and new_pos not in rest_poss):
					new_poss.add(new_pos)
		rest_poss.update(old_poss)
		old_poss=new_poss
	rest_poss.update(new_poss)

	target_spaces=(start_pos[X]+start_pos[Y]+step_count)%2

	# print(target_spaces)

	result=0
	arr=np.zeros(inp.shape)
	arr[rk]=-1

	for rest_pos in rest_poss:
		arr[rest_pos]+=1
		if (rest_pos[X]+rest_pos[Y])%2==target_spaces:
			# arr[rest_pos]+=1
			result+=1
			# print(rest_pos)

	# start: odd, step: even -> all odd
	plt.imshow(arr)
	plt.show()

	# print(rk)
	# print(st)
	# print(inp.shape)



	print(f"ANSWER: {result}")


main()
