# import matplotlib.pyplot as plt
import numpy as np
# import scipy
import sys

X=0
Y=1

I=0
O=1

EVEN=0
ODD=1

OUTSIDE=0
ON_EDGE=1
INSIDE=2

	# STATE==OUTSIDE
	#
	#  B
	#  AB
	#  FAB
	#  FFAB
	#  FFFAB
	#  FFFFAB
	#  FFFFFAB
	# SFFFFFFE

	# STATE==ON_EDGE
	#
	#
	#  A
	#  FA
	#  FFA
	#  FFFA
	#  FFFFA
	#  FFFFFA
	# SFFFFFFE

	# STATE==INSIDE
	#
	#
	#  A
	#  BA
	#  FBA
	#  FFBA
	#  FFFBA
	#  FFFFBA
	# SFFFFFIE

def main():

	# for i in range(1,10):
	# 	print(csum_even(i),csum_odd(i))
	# return

	if "e" in sys.argv:
		io=[
			# (6,16),
			# (10,50),
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
	# ASSUME: Field is a square with odd length (DIM%2==1).
	# ASSUME: No big labyrinths, can find full field in 2*DIM steps.
	# ASSUME: Step count big enough to cover at least ~3 fields.

	DIM=inp.shape[X]

	IDX=0

	total_steps=io[IDX][0]
	plot_count =io[IDX][1]

	center_index=DIM//2
	steps_to_reach_next_field_from_center=DIM-center_index
	steps_inside={}
	count_non_center_fields=((total_steps-steps_to_reach_next_field_from_center)//DIM)+1



	# Start field. Factor 2 because of labyrinths etc.
	steps_inside["S"]=DIM*2
	# steps_inside["S"]=DIM-1
	# Corner field.
	steps_inside["C"]=(total_steps-steps_to_reach_next_field_from_center)%DIM
	# Full field.
	steps_inside["F"]=steps_inside["S"]
	# INSIDE extra field.
	steps_inside["I"]=steps_inside["C"]+DIM

	parity={"S":EVEN}
	parity["C"]=(parity["S"]+count_non_center_fields)%2
	parity["I"]=inv(parity["C"])
	# A edge field.
	parity["A"]=parity["C"]
	# B edge field.
	parity["B"]=parity["I"]

	count_per_quadrant={
		"E":1,
		"I":0,
		"A":count_non_center_fields-1,
		"B":count_non_center_fields,
		"Feven":csum_even(count_non_center_fields-1),
		"Fodd":csum_odd(count_non_center_fields-1),
	}

	if steps_inside["C"]>center_index:
		STATE=OUTSIDE
		steps_inside["B"]=steps_inside["C"]-steps_to_reach_next_field_from_center
		steps_inside["A"]=steps_inside["B"]+DIM
		F_radius=count_non_center_fields-1
	elif steps_inside["C"]==center_index:
		STATE=ON_EDGE
		steps_inside["A"]=DIM-1
		steps_inside["B"]=0
		F_radius=count_non_center_fields-1
		count_per_quadrant["B"]=0
	else:
		STATE=INSIDE
		steps_inside["A"]=steps_inside["C"]+DIM-steps_to_reach_next_field_from_center
		steps_inside["B"]=steps_inside["A"]+DIM
		F_radius=count_non_center_fields-2
		count_per_quadrant["B"]=count_non_center_fields-2
		count_per_quadrant["I"]=1
		count_per_quadrant["Feven"]=csum_even(count_non_center_fields-2)
		count_per_quadrant["Fodd"]=csum_odd(count_non_center_fields-2)


	result=0

	PARITY=total_steps%2

	plots={}

	# Last index.
	CI=center_index
	# Last index.
	LI=DIM-1

	center_start_pos=(CI,CI)

	# EtoN: East corner and everything north above.
	start_pos_from_quadrant={
		"EtoN":((LI, 0),(CI, 0)),
		"NtoW":((LI,LI),(LI,CI)),
		"WtoS":((0 ,LI),(CI,LI)),
		"StoE":((0 , 0),(0 ,CI)),
	}

	full_plots=get_plots(center_start_pos,steps_inside["S"],rocks,(DIM,DIM))
	# for i in range(40):
	# 	full_plots=get_plots(center_start_pos,i,rocks,(DIM,DIM))
	# 	print(i,full_plots)

	# return

	for quadrant,(start_pos_diag,start_pos_cardinal) in start_pos_from_quadrant.items():
		plots[quadrant]={}
		plots[quadrant]["C"]=get_plots(start_pos_cardinal,steps_inside["C"],rocks,(DIM,DIM))

		plots[quadrant]["A"]=get_plots(start_pos_diag,steps_inside["A"],rocks,(DIM,DIM))

		if STATE!=ON_EDGE:
			plots[quadrant]["B"]=get_plots(start_pos_diag,steps_inside["B"],rocks,(DIM,DIM))
		else:
			plots[quadrant]["B"]=(0,0)

		if STATE==INSIDE:
			plots[quadrant]["I"]=get_plots(start_pos_cardinal,steps_inside["I"],rocks,(DIM,DIM))
		else:
			plots[quadrant]["I"]=(0,0)

	QUADCNT=4

	# Start field.
	result=full_plots[pcomb(parity["S"],PARITY)]

	result+=QUADCNT*count_per_quadrant["Feven"]*full_plots[EVEN]
	result+=QUADCNT*count_per_quadrant["Fodd"]*full_plots[ODD]

	for quadrant in start_pos_from_quadrant:
		result+=plots[quadrant]["C"][pcomb(parity["C"],PARITY)]
		for field in "ABI":
			result+=plots[quadrant][field][pcomb(parity[field],PARITY)]*count_per_quadrant[field]

	print(f"{DIM=},{total_steps=}")
	print(f"{steps_inside=}")
	print(f"{count_non_center_fields=}")
	print(f"{count_per_quadrant=}")
	print(f"{PARITY=},{parity=}")
	print(f"{full_plots=}")
	print(f"{plot_count=}")
	for card,plot in plots.items():
		print(card,plot)

	print(f"ANSWER: {result}, state: {STATE}")
	# 632421646069917 is too low

def csum_odd(n):
	n-=1-(n%2)
	term_count=((n+1)//2)
	return term_count**2
	# return csum(term_count)+csum(term_count-1)

def csum_even(n):
	n=(n//2)*2
	term_count=n//2
	return term_count*(term_count+1)
	# return csum(term_count+1)-1+csum(term_count-1)

def csum(n):
	return (n*(n+1))/2

def inv(parity):
	return 1-parity

def pcomb(*parities):
	res=0
	for parity in parities:
		res+=parity
	return res%2

def get_plots(start_pos,steps,rocks,shape):
	old_poss={start_pos}
	rest_poss=set()
	new_poss=set()

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
