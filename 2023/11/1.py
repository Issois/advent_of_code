import numpy as np
import matplotlib.pyplot as plt
def main():
	with open("data.input") as f:
	# with open("input-small-1") as f:
		inp=f.read().split("\n")

	rowc=len(inp)
	colc=len(inp[0])
	arr=np.zeros((rowc,colc))+1

	for ridx in range(rowc):
		for cidx in range(colc):
			if inp[ridx][cidx]=="#":
				arr[ridx,cidx]=0

	arr=np.insert(arr,np.nonzero(np.all(arr,axis=0))[0],1,axis=1)
	arr=np.insert(arr,np.nonzero(np.all(arr,axis=1))[0],1,axis=0)
	# print(empty_cols)
	# arr[:,np.all(arr,axis=0)]+=2
	# arr[np.all(arr,axis=1),:]+=4

	galaxies=[x for x in zip(*np.nonzero(arr==0))]

	result=0

	for i in range(len(galaxies)):
		for j in range(i+1,len(galaxies)):
			if not i==j:
				gi=galaxies[i]
				gj=galaxies[j]
				dr=abs(gi[0]-gj[0])
				dc=abs(gi[1]-gj[1])
				# print(f"{gi=},{gj=},{dr=},{dc=}")
				result+=dr+dc

			# if result>50:
				# break

	print(result)
	# print(galaxies)

	# plt.imshow(arr)
	# plt.show()


main()