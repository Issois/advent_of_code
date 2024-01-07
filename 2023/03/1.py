
import numpy as np
import matplotlib.pyplot as plt
import scipy


def main():

	with open("data.input") as f:
		inp=f.read()

	lines=inp.splitlines()


	matrix=[list(line) for line in lines]

	arr_str=np.array(matrix,dtype=str)
	arr=arr_str.copy()
	for s in "0123456789":
		arr[arr==s]=1
	dot_mask=arr=="."
	arr[arr!="1"]=2
	arr[dot_mask]=0
	arr=arr.astype(int)
	empties=arr==0
	numbers=arr==1
	symbols=arr==2


	convolved=convolve(symbols,1,1,1)
	convolved[convolved>0]=1
	convolved=convolved-symbols
	convolved=convolved&numbers

	convolved=convolve(convolved,1,1,1)
	convolved[convolved>0]=1
	convolved=convolved&numbers

	convolved=convolve(convolved,1,1,1)
	convolved[convolved>0]=1
	convolved=convolved&numbers

	rows,cols=np.nonzero(convolved)
	chars=arr_str[rows,cols]

	result=0
	num=str(chars[0])

	for i in range(1,chars.shape[0]):
		ch=chars[i]
		row=rows[i]
		col=cols[i]
		print(ch)
		if row==rows[i-1] and col==cols[i-1]+1:
			print(f" {num}+{ch}")
			num+=str(ch)
		else:
			print(f" ! add {num}")
			result+=int(num)
			num=str(ch)
			print(f" +{ch}")

	print(f" ! add {num}")
	result+=int(num)

	print(result)

def convolve(arr,a,b,c):
	print("  [CONVOLVE]")
	kernel=np.array([[c,b,c],[b,a,b],[c,b,c]])
	return scipy.signal.convolve2d(arr,kernel,mode="same")



main()
