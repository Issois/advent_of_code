import matplotlib.pyplot as plt
import numpy as np
import scipy
import sys

X=0
Y=1

I=0
O=1

EVEN=0
ODD=1

def main():

	if "e" in sys.argv:
		io=[
			(6,16),
			(10,50),
			(50,1594),
			(100,6536),
			(500,167004),
			(1000,668697),
			(5000,16733044),
		]
	else:
		io=[(26501365,None)]


	with open("example1.input" if "e" in sys.argv else "data.input") as f:
		inp=np.array([list(x) for x in f.read().split("\n")])

	# st=np.nonzero(inp=="S")
	rk=np.nonzero(inp=="#")

	rocks={x for x in zip(*rk)}
	# start_pos=(st[0][0],st[1][0])

	# ASSUME: Start pos is in center of field.
	# ASSUME: Field is a square with odd length.

	fparity_start_field=EVEN

	DIM=inp.shape[X]

	total_steps=io[0]
	plot_count=io[1]

	center_index=DIM//2
	steps_to_reach_next_field_from_center=DIM-center_index

	count_inside_non_center_fields=(total_steps-steps_to_reach_next_field_from_center)//DIM
	steps_inside_last_field=(total_steps-steps_to_reach_next_field_from_center)%DIM

	if steps_inside_last_field>center_index:
		steps_inside_diagB=steps_inside_last_field-steps_to_reach_next_field_from_center
		steps_inside_diagA=steps_into_diagB+DIM
	elif steps_inside_last_field==center_index:
		steps_inside_diagA=DIM-1
		# only one diagonal.
		steps_inside_diagB=None
	else:
		steps_inside_diagB=steps_inside_last_field+DIM
		steps_inside_diagA=steps_into_diagB-steps_to_reach_next_field_from_center

	fparity_last_field=(fparity_start_field+count_inside_non_center_fields+1)%2
	fparity_diagA=fparity_last_field
	fparity_diagB=(fparity_diagA+1)%2

	print(f"{count_inside_non_center_fields=},{steps_inside_last_field=}")
	# print(f"{count_inside_non_center_fields=}")

	# field_span=total_steps//DIM

	# remaining=total_steps%inp.shape[X]

	# print((center_index+steps_to_reach_next_field)%DIM)


	return

	# steps_into_final_field=

	# print(field_span,remaining,130-66)

	# return


	print(get_counts(start_pos,step_count,rocks,inp.shape))
	print(get_counts((130,0),130-66,rocks,inp.shape))


	# start: odd, step: even -> all odd
	# plt.imshow(arr)
	# plt.show()

	# print(rk)
	# print(st)
	# print(inp.shape)



	# print(f"ANSWER: {result}")


def get_counts(start_pos,steps,rocks,shape):
	old_poss={start_pos}
	rest_poss=set()

	dirs=[[-1,0],[1,0],[0,1],[0,-1]]

	for step in range(steps):
		new_poss=set()
		for old_pos in old_poss:
			for dx,dy in dirs:
				new_pos=old_pos[X]+dx,old_pos[Y]+dy
				if (
						0<=new_pos[X]<shape[X]
						and 0<=new_pos[Y]<shape[Y]
						and new_pos not in rocks
						and new_pos not in rest_poss):
					new_poss.add(new_pos)
		rest_poss.update(old_poss)
		old_poss=new_poss
	rest_poss.update(new_poss)

	# target_spaces=(start_pos[X]+start_pos[Y]+step_count)%2
	even_count=0
	odd_count=0

	for rest_pos in rest_poss:
		if (rest_pos[X]+rest_pos[Y])%2==0:
			even_count+=1
		else:
			odd_count+=1
	return even_count,odd_count

main()
