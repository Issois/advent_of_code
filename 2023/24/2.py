import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd

X=0
Y=1
Z=2

POS=0
VEL=1
RNG=np.random.default_rng()

def main():

	with open(sys.argv[1]) as f:
		inp=f.read().split("\n")

	beams=np.zeros((len(inp),2,3))

	# arr=np.zeros((len(inp),3,2),dtype=np.longlong)
	# beams=[]
	for idx,line in enumerate(inp):
		beam_arr=np.array([[int(num) for num in subline.split(",")] for subline in line.split("@")])
		beams[idx,POS,:]=beam_arr[0]
		beams[idx,VEL,:]=beam_arr[1]
		# beams.append(Beam(beam_arr[0],beam_arr[1]))

	# AX=Y
	for AX in range(3):

		print(f"AX: {AX}")

		df=pd.DataFrame({"a":beams[:,VEL,AX]})

		grps=df.groupby(by=df.a).groups
		for grp in grps.values():
			if len(grp)==3:
				break
		grp=list(grp)

		print(beams[grp,:,AX])
			# print(len(grp))


		break

	# t_end=2e12
	# x_end=beams[:,POS,AX]+(t_end*beams[:,VEL,AX])



	# for idx in range(beams.shape[0]):
		# plt.plot([0,t_end],[beams[idx,POS,AX],x_end[idx]],color="b",alpha=0.1)

	plt.show()



main()

