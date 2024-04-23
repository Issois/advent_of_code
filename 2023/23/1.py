
import numpy as np
import sys
# import matplotlib.pyplot as plt

FO=0
WA=1
NO=2
EA=3
SO=4
WE=5



def main():
	with open(sys.argv[1]) as f:
		inp=f.read().split("\n")

	arr=np.array([list(line) for line in inp])

	arrx=np.zeros(arr.shape,dtype=int)

	arrx[arr=="."]=WA
	arrx[arr=="^"]=NO
	arrx[arr==">"]=EA
	arrx[arr=="v"]=SO
	arrx[arr=="<"]=WE

	arr=arrx
	# plt.imshow(arr)
	# plt.show()
	# print(arr)

	start_col=np.nonzero(arr[0])[0][0]

	print(start_col)
	
	out={}


	answer=0
	# print(f"ANSWER: {answer}")
main()
