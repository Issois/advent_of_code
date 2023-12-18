
import numpy as np
import matplotlib.pyplot as plt
import scipy


def main():

	with open("input") as f:
		inp=f.read()

	lines=inp.splitlines()

	matrix=[list(line) for line in lines]

	arr=np.array(matrix,dtype=str)
	for s in "0123456789":
		arr[arr==s]=1
	dot_mask=arr=="."
	arr[arr!="1"]=2
	arr[dot_mask]=0
	arr=arr.astype(int)
	empties=arr==0
	numbers=arr==1
	symbols=arr==2
	# arr=arr.view('S1').reshape((arr.size, -1))
	# lines=["".join(arr[i,:]) for i in range(arr.shape[0])]
	# print("\n".join(lines))
	# print(arr[1,:])
	# print(arr)
	# numbers1=np.zeros(numbers.shape+np.array([2,2]))
	print(numbers.shape)
	# print(numbers1.shape)
	# numbers1[1:-1,1:-1]=numbers

	kernel=[
		[1,1,1],
		[1,1,1],
		[1,1,1],
	]
	# kernel=[
	# 	[0,1,0],
	# 	[1,0,1],
	# 	[0,1,0],
	# ]
	kernel=np.array(kernel)
	# convolved=scipy.signal.convolve2d(numbers1,kernel)
	convolved=scipy.signal.convolve2d(numbers,kernel,mode="same")
	convolved[convolved>0]=1
	convolved=convolved-numbers
	_,axs=plt.subplots(1,2)

	axs[0].imshow(numbers)
	# plt.show()
	axs[1].imshow(convolved)
	plt.show()






main()