
import matplotlib.pyplot as plt
import numpy as np
import sys
import bisect


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

VE_COL=0
VE_FIR=1
VE_LAS=2

RA_INS=0
RA_FIR=1
RA_LAS=2


OFFS=0
NAME=1

OFFS_FROM_DIRE={
	NO:array(-1, 0),
	EA:array( 0, 1),
	SO:array( 1, 0),
	WE:array( 0,-1),
}



def main():
	with open("example1.input" if "e" in sys.argv else "data.input") as f:
		if False:
			inp=[line.split("#")[1][:-1] for line in f.read().split("\n")]
			arr=np.array([[int(line[:-1],base=16),(int(line[-1])+1)%4] for line in inp],dtype=np.int64)
			arr=arr[:,::-1]
		else:
			inp=(f.read()
				.replace("U","0")
				.replace("R","1")
				.replace("D","2")
				.replace("L","3")
				.split("\n"))
			arr=np.array([[int(x) for x in line.split(" ")[:2]] for line in inp],dtype=np.int64)


	# print(inp)

	# print(arr)

	result=np.int64(0)

	# col, first row, last row
	vedges=[]


	current_pos=array(0,0)
	for dire,dist in arr:
		next_pos=current_pos+OFFS_FROM_DIRE[dire]*dist
		# NO or SO
		if dire%2==0:
			first=current_pos[ROW]
			last=next_pos[ROW]
			if first<last:
				vedges.append((current_pos[COL],first,last))
			else:
				vedges.append((current_pos[COL],last,first))
		current_pos=next_pos
		# min_col=min(min_col,current_pos[COL])
		# max_col=max(max_col,current_pos[COL])

	# vedges=sorted(vedges,key=lambda elem:elem[0])
	vedges=sorted(vedges)
	# for vedge in vedges:
		# print(vedge)

	# group vedges:
	vegde_groups=[[vedges[0]]]
	for vedge in vedges[1:]:
		if vedge[VE_COL]==vegde_groups[-1][-1][VE_COL]:
			vegde_groups[-1].append(vedge)
		else:
			vegde_groups.append([vedge])

	# print(vegde_groups)

	DEB=False
	DEB=True
	# return
	ranges=[]
	prev_size=0
	# prev_col=None
	for vedge_group in vegde_groups:
		curr_col=vedge_group[0][VE_COL]
		curr_size=0
		if len(ranges)==0:
			# add vedges.
			for vedge in vedge_group:
				ranges.extend([vedge[VE_FIR],vedge[VE_LAS]])
				curr_size+=np.int64(vedge[VE_LAS]-vedge[VE_FIR]+1)
			if DEB: print(f" ADD first vedges, size {curr_size}")
			result+=curr_size
		else:
			# add inbetween columns:
			if curr_col-prev_col>1:
				if DEB: print(f" RE ADD {curr_col-prev_col-1} cols inbetween with size {prev_size}")
				result+=(curr_col-prev_col-1)*prev_size


			if DEB: print(f"  UPD ranges with vedges {vedge_group} from {ranges}",end="")
			# update ranges:
			for vedge in vedge_group:
				bisect.insort(ranges,vedge[VE_FIR])
				bisect.insort(ranges,vedge[VE_LAS])
			# remove number pairs in ranges.
			i=0
			while i<len(ranges)-1:
				if ranges[i]==ranges[i+1]:
					del ranges[i]
					del ranges[i]
				else:
					i+=1
			if DEB: print(f" to {ranges}")

			# add bigger one between prev and new column:
			for rng_idx in range(0,len(ranges)-1,2):
				curr_size+=np.int64(ranges[rng_idx+1]-ranges[rng_idx]+1)

			if DEB: print(f" ADD size max({curr_size},{prev_size})")
			result+=max(curr_size,prev_size)
		prev_size=curr_size
		prev_col=curr_col

	print(f"ANSWER: {result}")

main()
