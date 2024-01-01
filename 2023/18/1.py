
import matplotlib.pyplot as plt
import numpy as np
import sys

def array(*vals):
	return np.array(vals)

ROW=0
COL=1

MIN=0
MAX=1

NO=0
EA=1
SO=2
WE=3

OFFS=0
NAME=1

OFFS_FROM_DIRE={
	NO:array(-1, 0),
	EA:array( 0, 1),
	SO:array( 1, 0),
	WE:array( 0,-1),
}



def main():
	with open("example1" if "e" in sys.argv else "input") as f:
		inp=(f.read()
			.replace("U","0")
			.replace("R","1")
			.replace("D","2")
			.replace("L","3")
			.split("\n"))
		arr=np.array([[int(x) for x in line.split(" ")[:2]] for line in inp],dtype=int)
	result=0
	turns=((((arr[1:,0]-arr[:-1,0])+4)%4)-2)*-1
	# inside_is_to_the_right=np.sum(turns)>0
	inside_turn=np.sum(turns)
	inside_turn=inside_turn/abs(inside_turn)


	current_pos=array(0,0)
	inside=set([tuple(current_pos)])
	to_check=[]
	mima=np.zeros((2,2),dtype=np.int32)
	border=set()
	# mima[MIN,:]=np.iinfo(np.int32).max
	# mima[MAX,:]=np.iinfo(np.int32).min
	for dire,dist in arr:
		new_positions=current_pos+np.outer((np.arange(dist)+1),OFFS_FROM_DIRE[dire])
		current_pos=new_positions[-1,:]
		inner_positions=new_positions+OFFS_FROM_DIRE[(dire+inside_turn)%4]
		# print(new_positions)
		# print(inner_positions)
		# return
		for pos in new_positions:
			inside.add(tuple(pos))
			border.add(tuple(pos))
		for pos in inner_positions:
			inside.add(tuple(pos))
			to_check.append(pos)

		mima[MIN]=np.minimum(mima[MIN],current_pos)
		mima[MAX]=np.maximum(mima[MAX],current_pos)


	loop_cnt=0
	while len(to_check)>0:
		loop_cnt+=1
		if loop_cnt%1000==0:
			print(f"{len(to_check)}")

		check=to_check.pop()
		if not tuple(check) in border:
			for dire,offs in OFFS_FROM_DIRE.items():
				new_pos=check+offs
				new_pos_tup=tuple(new_pos)
				if new_pos_tup not in inside:
					inside.add(new_pos_tup)
					if new_pos_tup not in border:
						to_check.append(new_pos)


	if True:
		row_count=mima[MAX,ROW]-mima[MIN,ROW]+1
		col_count=mima[MAX,COL]-mima[MIN,COL]+1
		img=np.zeros((row_count,col_count))
		for elem in inside:
			img[elem[ROW]-mima[MIN,ROW],elem[COL]-mima[MIN,COL]]=1

		plt.imshow(img)
		plt.show()

	result=len(inside)

	print(f"ANSWER: {result}")
main()
