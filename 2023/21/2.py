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
	data_step_count=26501365

	inputs={
		"data":None,
		"example1":None,
		"custom":None,
	}

	for inp in inputs:
		with open(inp+".input") as f:
			lines=f.read().split("\n")
			inputs[inp]=np.array([list(x) for x in lines])

	# ASSUME: Field is a square with odd length (DIM%2==1).
	# ASSUME: Start pos is in center of field.
	# ASSUME (for fast calculation): first, middle and last row/col are without rocks.
	answer=gp("data","fast",data_step_count,inputs)


	print(f"ANSWER: {answer}")
	# 632421646069917 to low (from try 1)
	# 632421658207872 to hi  (from try 2)
	# 632421652138917 is correct

def gp(name,mode,total_stepcount,inputs):
	calc=gp_ext_sim if mode=="sim" else gp_ext_fast
	return calc(inputs[name],total_stepcount)


def gp_ext_sim(inp,total_stepcount):
	DIM=inp.shape[0]
	rk=np.nonzero(inp=="#")
	rocks={x for x in zip(*rk)}
	radius=(total_stepcount-(DIM//2))//DIM
	big_size=((radius+1)*2)+1
	arr=np.zeros((DIM,DIM))
	arr[rk]=1
	big_arr=np.tile(arr,(big_size,big_size))
	start_pos_big=big_arr.shape[X]//2,big_arr.shape[Y]//2
	big_arr_rk=np.nonzero(big_arr)
	big_arr_rocks={x for x in zip(*big_arr_rk)}
	plots=get_plots(start_pos_big,total_stepcount,big_arr_rocks,big_arr.shape[X])
	return len(plots[total_stepcount%2])


def gp_ext_fast(inp,total_stepcount):
	DIM=inp.shape[0]
	start=DIM//2,DIM//2

	rk=np.nonzero(inp=="#")
	rocks={x for x in zip(*rk)}


	levels_from_dtype={
		"card":[1,2],
		"diag":[0,1,2],
	}

	MAX_LEVEL=max(levels_from_dtype["diag"])

	PARITY=total_stepcount%2

	pathlength_max=total_stepcount+1
	pathlength_card_inside_center=(DIM//2)+1
	number_of_fields_between_center_and_corner=(pathlength_max-pathlength_card_inside_center)//DIM

	pathlength_inside={dtype:{lvl:None for lvl in lvls} for dtype,lvls in levels_from_dtype.items()}
	stepcount_to_reach_non_center_field=DIM-(DIM//2)


	pathlength_inside["card"][1]=(
		(pathlength_max-pathlength_card_inside_center)%DIM
	)
	pathlength_inside["card"][2]=(
		pathlength_inside["card"][1]
		+DIM
	)
	pathlength_inside["diag"][0]=(
		pathlength_inside["card"][1]
		-stepcount_to_reach_non_center_field
	)
	pathlength_inside["diag"][1]=(
		pathlength_inside["diag"][0]
		+DIM
	)
	pathlength_inside["diag"][2]=(
		pathlength_inside["diag"][1]
		+DIM
	)

	parity_field_lvl1=(number_of_fields_between_center_and_corner+1)%2

	parity_from_level={lvl:(parity_field_lvl1+lvl+1)%2 for lvl in levels_from_dtype["diag"]}

	# ASSUME: No big labyrinths, can find full field in 2*DIM steps.
	plots_full=[len(p) for p in get_plots(start,2*DIM,rocks,DIM)]


	full_fields_radius=number_of_fields_between_center_and_corner+1-MAX_LEVEL
	full_count_from_parity={
		EVEN:(csum_even(full_fields_radius)*4)+1,
		ODD :(csum_odd (full_fields_radius)*4),
	}

	CARD_DIRES={NO,EA,SO,WE}

	fieldcount={}
	fieldcount["card"]={lvl:1 for lvl in levels_from_dtype["card"]}
	fieldcount["diag"]={lvl:number_of_fields_between_center_and_corner+1-lvl for lvl in levels_from_dtype["diag"]}

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
		result+=plots_full[par]*full_count_from_parity[pcomb(par,PARITY)]

	for dire,start_pos in start_pos_from_dire.items():

		dtype="card" if dire in CARD_DIRES else "diag"


		plotcount_from_level={
			lvl:[len(p) for p in get_plots(start_pos,pathlength_inside[dtype][lvl],rocks,DIM)]
			for lvl in levels_from_dtype[dtype]
		}


		for lvl,plotcount in plotcount_from_level.items():
			par=pcomb(parity_from_level[lvl],PARITY)
			sc=pathlength_inside[dtype][lvl]
			pc=plotcount[par]
			fc=fieldcount[dtype][lvl]
			val=pc*fc
			result+=val

	return result


def get_plots(start_pos,steps,rocks,DIM):
	if steps<0:
		return set(),set()
	if steps==0:
		start_parity=(start_pos[X]+start_pos[Y])%2
		result=[set(),set()]
		result[start_parity]={start_pos}
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
						0<=new_pos[X]<DIM
						and 0<=new_pos[Y]<DIM
						and new_pos not in rocks
						and new_pos not in rest_poss):
					new_poss.add(new_pos)
		rest_poss.update(old_poss)
		old_poss=new_poss
	rest_poss.update(new_poss)

	# target_spaces=(start_pos[X]+start_pos[Y]+step_count)%2
	# even_count=0
	# odd_count=0

	evens=set()
	odds=set()

	for rest_pos in rest_poss:
		if (rest_pos[X]+rest_pos[Y])%2==0:
			evens.add(rest_pos)
		else:
			odds.add(rest_pos)

	# print(len(evens),len(odds))
	# print(f"{evens=},{odds=}")
	return evens,odds




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

def compare_via_plot(inputs):
	step_count=150
	rs,plots_s,dim_s=gp("custom","sim",step_count,inputs)
	rf,plots_f,dim_f=gp("custom","fast",step_count,inputs)
	plot_plots([plots_s,plots_f[EA][1]],[dim_s,dim_f])


def plot_plots(plotss,dims,subsize):
	_,axs=plt.subplots(ncols=len(plotss),figsize=(20,10))
	if len(plotss)==1:
		axs=[axs]

	for plots,ax,dim in zip(plotss,axs,dims):
		arr=np.zeros((dim,dim))
		plotarr=np.array(list(plots))
		if dim>100:
			arr[arr.shape[X]//2,arr.shape[Y]//2]=3
			arr[:,0::subsize]=-1
			arr[:,subsize-1::subsize]=-1
			arr[0::subsize,:]=-1
			arr[subsize-1::subsize,:]=-1
		if plotarr.shape[0]>0:
			arr[plotarr[:,0],plotarr[:,1]]+=2
		ax.imshow(arr)
	plt.show()

main()

