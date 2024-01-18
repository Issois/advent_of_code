import matplotlib.pyplot as plt
import numpy as np
import scipy
import sys
def main():
	with open("example1.input" if "e" in sys.argv else "data.input") as f:
		inp=np.array([list(x) for x in f.read().split("\n")])
	# pl=inp[inp=="."]
	rk=inp=="#"
	st=np.nonzero(inp=="S")
	# print(st)
	# print(inp.shape)
	arr=np.zeros(inp.shape)
	rocks=np.zeros(inp.shape)
	rocks[rk]=1
	rocks=1-rocks
	arr[st]=1

	steps=6

	ch=np.zeros(inp.shape)


	print(arr)
	arr=convolve(arr,1,1,0)*rocks
	print(arr)


	# plt.imshow(arr)
	# plt.show()


	# print(inp)


	result=0

	print(f"ANSWER: {result}")



def convolve(arr,a,b,c):
	# print("  [CONVOLVE]")
	kernel=np.array([[c,b,c],[b,a,b],[c,b,c]])
	return scipy.signal.convolve2d(arr,kernel,mode="same")



main()
