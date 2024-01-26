import matplotlib.pyplot as plt
import numpy as np
# import scipy
import sys

X=0
Y=1

EVEN=0
ODD=1

NO=0
NE=1
EA=2
SE=3
SO=4
SW=5
WE=6
NW=7




def main():


	if "e" in sys.argv:
		io=[
			# (6,16),
			# (10,50),
			# (50,1594),
			# (100,6536),
			50,
			100,
			500,
			1000,
			5000,
		]
	else:
		io=[
			50,
			500,
			1000,
			26501365,
		]


	with open("custom.input" if "e" in sys.argv else "data.input") as f:
		lines=f.read().split("\n")
		inp=np.array([list(x) for x in lines])

	IDX=0
	if "i" in sys.argv:
		IDX=int(sys.argv[-1])
	total_stepcount=io[IDX]
	plot_count     =None


	# ASSUME: Field is a square with odd length (DIM%2==1).
	DIM=inp.shape[0]
	# ASSUME: Start pos is in center of field.
	start=(DIM//2,DIM//2)
	# ASSUME: first, middle and last row/col are without rocks.

	# print(rk)

	if "x" in sys.argv:
		arr=inp.copy()
		arr[start[X],:]="."
		arr[:,start[Y]]="."
		rk=np.nonzero(arr=="#")
		rocks={x for x in zip(*rk)}
		radius=(total_stepcount-(DIM//2))//DIM
		big_size=((radius+1)*2)+1
		print(f"{big_size=}")
		arr=np.zeros(arr.shape)
		arr[rk]=1
		big_arr=np.tile(arr,(big_size,big_size))
		start_pos_big=big_arr.shape[X]//2,big_arr.shape[Y]//2
		big_arr_rk=np.nonzero(big_arr)
		big_arr_rocks={x for x in zip(*big_arr_rk)}
		plot_count=get_plots(start_pos_big,total_stepcount,big_arr_rocks,big_arr.shape)[total_stepcount%2]
		# plot_count=get_plots(start_pos_big,total_stepcount,big_arr_rocks,big_arr.shape)
		# plt.imshow(big_arr)
		# plt.imshow(arr)
		# plt.show()
		# return
	else:
		rk=np.nonzero(inp=="#")
		rocks={x for x in zip(*rk)}

	# print(f"{radius=}")
	# return



	# print(DIM*DIM*big_size*big_size*4/1000000)
	# print(inp.shape*big_size)

	# big_arr=np.zeros((DIM*big_size,DIM*big_size),dtype=np.int8)

	# for dx in range(DIM):
	# 	for dy in range(DIM):
	# 		big_arr[(DIM*dx):(DIM*(dx+1)),(DIM*dy):(DIM*(dy+1))]=arr

	# print(big_arr.shape)

	# big_arr[start_pos_big]=2

	# print(f"{plot_count=}")
	# return
	# plot_count

	# max_steps=big_arr.shape[X]//2



	# return

	# return
	# print(get_plots((0,0),5,rocks,inp.shape))
	# return
	# arr=np.zeros(inp.shape)
	# arr[rk]=1
	# arr[start]=2


	stepcount_middle_to_next={}
	stepcount_middle_to_next["card"]=DIM-start[X]
	stepcount_middle_to_next["diag"]=2*stepcount_middle_to_next["card"]

	levels_from_dtype={
		"card":[1,2],
		"diag":[0,1,2],
	}
	PARITY=total_stepcount%2

	print(f"{DIM=}")
	print(f"{total_stepcount=}")

	print(f"{PARITY=}")
	print(f"{plot_count=}")
	# print(f"{stepcount_middle_to_next_card=}")
	# print(f"{stepcount_middle_to_next_diag=}")

	fieldstepcount={}
	fieldstepcount["card"]={lvl:((total_stepcount-stepcount_middle_to_next["card"])//DIM)-(lvl-1) for lvl in levels_from_dtype["card"]}
	fieldstepcount["diag"]={lvl:fieldstepcount["card"][1]-lvl for lvl in levels_from_dtype["diag"]}

	a={1 for x in [1]}
	stepcount_into={
		dtype:{
			lvl:total_stepcount-stepcount_middle_to_next[dtype]-(fieldstepcount[dtype][lvl]*DIM) for lvl in lvls
		} for dtype,lvls in levels_from_dtype.items()
	}
	#
	# stepcoun t_into_diag_LVL={lvl:total_stepcount-stepcount_middle_to_next_diag-(fieldstepcount_to_diag_LVL[lvl]*DIM) for lvl in LVLS_DIAG}

	# print(f"{stepcount_into['card'][1]=}")
	# print(f"{stepcount_into['card'][2]=}")
	# print(f"{stepcount_into['diag'][0]=}")
	# print(f"{stepcount_into['diag'][1]=}")
	# print(f"{stepcount_into['diag'][2]=}")

	parity_field_lvl1=(fieldstepcount["card"][1]+1)%2
	print(f"{parity_field_lvl1=}")

	parity_from_level={lvl:(parity_field_lvl1+lvl+1)%2 for lvl in levels_from_dtype["diag"]}

	print(f"{parity_from_level=}")

	# ASSUME: No big labyrinths, can find full field in 2*DIM steps.
	plots_full=get_plots(start,2*DIM,rocks,inp.shape)

	full_radius=fieldstepcount["card"][2]

	full_count_from_parity={
		EVEN:(csum_even(full_radius)*4)+1,
		ODD :(csum_odd (full_radius)*4),
	}
	# print(f"{full_radius=}")
	# print(f"{full_count_from_parity=}")
	# return

	CARD_DIRES={NO,EA,SO,WE}

	fieldcount={}
	fieldcount["card"]={lvl:1 for lvl in levels_from_dtype["card"]}
	fieldcount["diag"]={lvl:fieldstepcount["card"][1]+1-lvl for lvl in levels_from_dtype["diag"]}

	print(f"{fieldcount=}")

	start_pos_from_dire={
		NO:(DIM-1 ,DIM//2),
		NE:(DIM-1 ,0     ),
		EA:(DIM//2,0     ),
		SE:(0     ,0     ),
		SO:(0     ,DIM//2),
		SW:(0     ,DIM-1 ),
		WE:(DIM//2,DIM-1 ),
		NW:(DIM-1 ,DIM-1 ),
	}

	result=0

	PARITIES=[EVEN,ODD]
	for par in PARITIES:

		print(f"With parity {par} there are {full_count_from_parity[par]} full fields with {plots_full[par]} plots each.")
		result+=plots_full[par]*full_count_from_parity[par]

	for dire,start_pos in start_pos_from_dire.items():
		# print()

		dtype="card" if dire in CARD_DIRES else "diag"
		# lvls=LVLS_CARD if dire in CARD_DIRES else LVLS_DIAG
		plotcount_from_level={lvl:get_plots(start_pos,stepcount_into[dtype][lvl],rocks,inp.shape) for lvl in levels_from_dtype[dtype]}
		# print(plotcount_from_level)
		for lvl,plotcount in plotcount_from_level.items():
			par=pcomb(parity_from_level[lvl],PARITY)
			sc=stepcount_into[dtype][lvl]
			pc=plotcount[par]
			fc=fieldcount[dtype][lvl]
			val=pc*fc
			# if lvl==1:
			# print(f"{dire=},{start_pos=},{sc=},{lvl=},{dtype=},{par=},{pc=},{fc=},{val=}")
			result+=val


	print(f"ANSWER: {result}")
	# 632421646069917 to low (from try 1)
	# 632421658207872 to hi  (from this try)



def pcomb(*parities):
	res=0
	for parity in parities:
		res+=parity
	return res%2

def csum_odd(n):
	n-=1-(n%2)
	term_count=((n+1)//2)
	return term_count**2

def csum_even(n):
	n=(n//2)*2
	term_count=n//2
	return term_count*(term_count+1)

def csum(n):
	return (n*(n+1))/2


def get_plots(start_pos,steps,rocks,shape):
	if steps<0:
		return (0,0)
	if steps==0:
		start_parity=(start_pos[X]+start_pos[Y])%2
		result=[0,0]
		result[start_parity]=1
		return result
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
			# print(f"ODD: {rest_pos}")
			odd_count+=1
	return even_count,odd_count

main()
