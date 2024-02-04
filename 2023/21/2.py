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

	# vals=np.array(vals,dtype=float)
	# vals[:,1]=vals[:,0]/vals[:,1]
	# # print(vals[:,1])

	# plt.plot(vals[:,0],vals[:,1])
	# plt.show()
	# return
	# if "e" in sys.argv:
	# 	io=[
	# 	]
	# else:
	# 	io=[
	# 		50,
	# 		500,
	# 		1000,
	# 		26501365,
	# 	]

	testcases={
		# 6:16,
		10:50,
		50:1594,
		100:6536,
		500:167004,
		1000:668697,
		5000:16733044,
	}



	data_step_count=26501365


	# file_name=argv[1]+".input"
	# calc=gp_ext_sim if argv[2]=="s" else gp_ext_fast
	# step_count=int(argv[3])

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
	test_sim=False
	test_sim_vs_fast=True
	if test_sim_vs_fast:
		# for step_count in [50,51,52,53,500,501,502,503,1000,1001,1002,1003]:
		# for step_count in range(4,176,2):
		for step_count in range(151,176,1):
			rs,plots_s,dim_s=gp("custom","sim",step_count,inputs)
			rf,plots_f,dim_f=gp("custom","fast",step_count,inputs)
			plot_plots([plots_s,plots_f[NE][2]],[dim_s,dim_f])
			return

			# print(f"Tested custom with {step_count} steps. Sim: {rs}, fast: {rf}. Diff: {(rf-rs)/13}.")
			# x.append()
		return
		infos={}
		for step_count in range(451,551,2):
		# for step_count in [500,501,502,503]:
		# for step_count in [500,501,502,503]:
			rs=gp("data","sim",step_count,inputs)
			rf,info=gp("data","fast",step_count,inputs)
			infos[step_count]=info
			print(f"Tested data with {step_count} steps. Sim: {rs}, fast: {rf}. Diff: {rf-rs}.")
		# print(infos)

		# for i in range(len(infos[500])):
		# 	print(f"{infos[500][i]['dire']}@{infos[500][i]['lvl']}: sc {infos[500][i]['sc']} vs {infos[501][i]['sc']}; pc {infos[500][i]['pc']} vs {infos[501][i]['pc']}; fc {infos[500][i]['fc']} vs {infos[501][i]['fc']}; val {infos[500][i]['val']} vs {infos[501][i]['val']}")
		# for key in infos[500]:
			# print(key,infos[500][key],infos[501][key])

	if test_sim:
		for step_count,true_result in testcases.items():
			if step_count<2000:
				result=gp("example1","sim",step_count,inputs)
				print(f"Tested example1 with {step_count} steps. sim: {result}, true: {true_result}. Success: {result==true_result}")


	# 75
	# 9
	# 4
	# 28

def plot_plots(plotss,dims):
	_,axs=plt.subplots(ncols=len(plotss),figsize=(20,10))
	for plots,ax,dim in zip(plotss,axs,dims):
		arr=np.zeros((dim,dim))
		# print(dim)
		plotarr=np.array(list(plots))
		if dim>100:
			arr[arr.shape[X]//2,arr.shape[Y]//2]=3
			arr[:,0::13]=-1
			arr[:,12::13]=-1
			arr[0::13,:]=-1
			arr[12::13,:]=-1
		if plotarr.shape[0]>0:
			arr[plotarr[:,0],plotarr[:,1]]+=2
		if dim>100:
			arr=arr[arr.shape[X]//2-50:arr.shape[X]//2+13,-50:]
		ax.imshow(arr)
	plt.show()

	# 632421646069917 to low (from try 1)
	# 632421658207872 to hi  (from this try)

def gp(name,mode,total_stepcount,inputs):
	calc=gp_ext_sim if mode=="sim" else gp_ext_fast
	return calc(inputs[name],total_stepcount)


def gp_ext_sim(inp,total_stepcount):
	DIM=inp.shape[0]
	rk=np.nonzero(inp=="#")
	rocks={x for x in zip(*rk)}
	radius=(total_stepcount-(DIM//2))//DIM
	# print(f"{total_stepcount=}")
	# print(f"{radius=}")
	big_size=((radius+1)*2)+1
	# print(f"{big_size=}")
	arr=np.zeros((DIM,DIM))
	arr[rk]=1
	big_arr=np.tile(arr,(big_size,big_size))
	start_pos_big=big_arr.shape[X]//2,big_arr.shape[Y]//2
	big_arr_rk=np.nonzero(big_arr)
	big_arr_rocks={x for x in zip(*big_arr_rk)}
	plots=get_plots(start_pos_big,total_stepcount,big_arr_rocks,big_arr.shape[X])[total_stepcount%2]
	# print()
	# for p in plots:
	# pll=np.array(list(plots))
	# big_arr[pll[:,0],pll[:,1]]=2
	# plt.imshow(big_arr)
	# plt.show()
	# exit()
	return len(plots),plots,big_arr.shape[X]


def gp_ext_fast(inp,total_stepcount):
	DIM=inp.shape[0]
	start=DIM//2,DIM//2

	rk=np.nonzero(inp=="#")
	rocks={x for x in zip(*rk)}

	stepcount_middle_to_next={}
	stepcount_middle_to_next["card"]=DIM-(DIM//2)
	stepcount_middle_to_next["diag"]=2*stepcount_middle_to_next["card"]

	levels_from_dtype={
		"card":[1,2],
		"diag":[0,1,2],
	}
	PARITY=total_stepcount%2

	# print(f"{DIM=}")
	# print(f"{total_stepcount=}")

	# print(f"{PARITY=}")
	# print(f"{plot_count=}")
	# print(f"{stepcount_middle_to_next_card=}")
	# print(f"{stepcount_middle_to_next_diag=}")

	fieldstepcount={}
	fieldstepcount["card"]={lvl:((total_stepcount-stepcount_middle_to_next["card"])//DIM)-(lvl-1) for lvl in levels_from_dtype["card"]}
	fieldstepcount["diag"]={lvl:fieldstepcount["card"][1]-lvl for lvl in levels_from_dtype["diag"]}

	stepcount_into={
		dtype:{
			lvl:total_stepcount-stepcount_middle_to_next[dtype]-(fieldstepcount[dtype][lvl]*DIM) for lvl in lvls
		} for dtype,lvls in levels_from_dtype.items()
	}
	#
	# stepcoun t_into_diag_LVL={lvl:total_stepcount-stepcount_middle_to_next_diag-(fieldstepcount_to_diag_LVL[lvl]*DIM) for lvl in LVLS_DIAG}

	# print(f"{fieldstepcount['card'][1]=}")
	# print(f"{stepcount_into['card'][1]=}")
	# print(f"{stepcount_into['card'][2]=}")
	# print(f"{stepcount_into['diag'][0]=}")
	# print(f"{stepcount_into['diag'][1]=}")
	# print(f"{stepcount_into['diag'][2]=}")

	parity_field_lvl1=(fieldstepcount["card"][1]+1)%2
	# print(f"{parity_field_lvl1=}")

	parity_from_level={lvl:(parity_field_lvl1+lvl+1)%2 for lvl in levels_from_dtype["diag"]}

	# print(f"{parity_from_level=}")

	# ASSUME: No big labyrinths, can find full field in 2*DIM steps.
	plots_full=[len(p) for p in get_plots(start,2*DIM,rocks,DIM)]

	full_radius=fieldstepcount["card"][2]

	full_count_from_parity={
		EVEN:(csum_even(full_radius)*4)+1,
		ODD :(csum_odd (full_radius)*4),
	}
	# print(f"{full_radius=}")
	print(f"{full_count_from_parity=}")
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

		# print(f"With parity {par} there are {full_count_from_parity[par]} full fields with {plots_full[par]} plots each.")
		result+=plots_full[par]*full_count_from_parity[par]

	# info=[]
	plots={}
	for dire,start_pos in start_pos_from_dire.items():
		# print()

		dtype="card" if dire in CARD_DIRES else "diag"

		plots_from_level={
			lvl:[
				plots for plots in get_plots(start_pos,stepcount_into[dtype][lvl],rocks,DIM)
			] for lvl in levels_from_dtype[dtype]
		}
		plotcount_from_level={
			lvl:[len(p) for p in plots_from_level[lvl]]
			for lvl in levels_from_dtype[dtype]
		}


		# print(plotcount_from_level)
		for lvl,plotcount in plotcount_from_level.items():
			par=pcomb(parity_from_level[lvl],PARITY)
			sc=stepcount_into[dtype][lvl]
			pc=plotcount[par]
			fc=fieldcount[dtype][lvl]
			val=pc*fc
			plots_from_level[lvl]=plots_from_level[lvl][par]
			# if lvl==1:
			# info.append({
			# 	"dire":dire,
			# 	"start_pos":start_pos,
			# 	"sc":sc,
			# 	"lvl":lvl,
			# 	"dtype":dtype,
			# 	"par":par,
			# 	"pc":pc,
			# 	"fc":fc,
			# 	"val":val,
			# })

			# print(f"{dire=},{str(start_pos):10},{sc=:3},{lvl=},{dtype=},{par=},{pc=:5},{fc=:5},{val=:6}")
			# print(f"{par=}")
			result+=val

		plots[dire]=plots_from_level
	return result,plots,DIM


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

main()


# vals=[[51,-20],[53,-20],[55,-20],[57,-20],[59,28],[61,28],[63,28],[65,28],[67,28],[69,28],[71,28],[73,-36],[75,-36],[77,-36],[79,-36],[81,-36],[83,-36],[85,44],[87,44],[89,44],[91,44],[93,44],[95,44],[97,44],[99,-52],[101,-52],[103,-52],[105,-52],[107,-52],[109,-52],[111,60],[113,60],[115,60],[117,60],[119,60],[121,60],[123,60],[125,-68],[127,-68],[129,-68],[131,-68],[133,-68],[135,-68],[137,76],[139,76],[141,76],[143,76],[145,76],[147,76],[149,76],[151,-84],[153,-84],[155,-84],[157,-84],[159,-84],[161,-84],[163,92],[165,92],[167,92],[169,92],[171,92],[173,92],[175,92],[177,-100],[179,-100],[181,-100],[183,-100],[185,-100],[187,-100],[189,108],[191,108],[193,108],[195,108],[197,108],[199,108],[201,108],[203,-116],[205,-116],[207,-116],[209,-116],[211,-116],[213,-116],[215,124],[217,124],[219,124],[221,124],[223,124],[225,124],[227,124],[229,-132],[231,-132],[233,-132],[235,-132],[237,-132],[239,-132],[241,140],[243,140],[245,140],[247,140],[249,140],[251,140],[253,140],[255,-148],[257,-148],[259,-148],[261,-148],[263,-148],[265,-148],[267,156],[269,156],[271,156],[273,156],[275,156],[277,156],[279,156],[281,-164],[283,-164],[285,-164],[287,-164],[289,-164],[291,-164],[293,172],[295,172],[297,172],[299,172],[301,172],[303,172],[305,172],[307,-180],[309,-180],[311,-180],[313,-180],[315,-180],[317,-180],[319,188],[321,188],[323,188],[325,188],[327,188],[329,188],[331,188],[333,-196],[335,-196],[337,-196],[339,-196],[341,-196],[343,-196],[345,204],[347,204],[349,204],[351,204],[353,204],[355,204],[357,204],[359,-212],[361,-212],[363,-212],[365,-212],[367,-212],[369,-212],[371,220],[373,220],[375,220],[377,220],[379,220],[381,220],[383,220],[385,-228],[387,-228],[389,-228],[391,-228],[393,-228],[395,-228],[397,236],[399,236],[401,236],[403,236],[405,236],[407,236],[409,236],[411,-244],[413,-244],[415,-244],[417,-244],[419,-244],[421,-244],[423,252],[425,252],[427,252],[429,252],[431,252],[433,252],[435,252],[437,-260],[439,-260],[441,-260],[443,-260],[445,-260],[447,-260],[449,268],[451,268],[453,268],[455,268],[457,268],[459,268],[461,268],[463,-276],[465,-276],[467,-276],[469,-276],[471,-276],[473,-276],[475,284],[477,284],[479,284],[481,284],[483,284],[485,284],[487,284],[489,-292],[491,-292],[493,-292],[495,-292],[497,-292],[499,-292],[501,300],[503,300],[505,300],[507,300],[509,300],[511,300],[513,300],[515,-308],[517,-308],[519,-308],[521,-308],[523,-308],[525,-308],[527,316],[529,316],[531,316],[533,316],[535,316],[537,316],[539,316],[541,-324],[543,-324],[545,-324],[547,-324],[549,-324],]