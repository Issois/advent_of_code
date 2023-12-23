import numpy as np
import matplotlib.pyplot as plt
def main():
	with open("input") as f:
	# with open("input-small-1") as f:
		inp=f.read().split("\n")

	rowc=len(inp)
	colc=len(inp[0])
	arr=np.zeros((rowc,colc))+1

	for ridx in range(rowc):
		for cidx in range(colc):
			if inp[ridx][cidx]=="#":
				arr[ridx,cidx]=0

	# arr=np.insert(arr,np.nonzero(np.all(arr,axis=0))[0],1,axis=1)
	# arr=np.insert(arr,np.nonzero(np.all(arr,axis=1))[0],1,axis=0)
	# print(empty_cols)
	empty_cols=np.all(arr,axis=0)
	empty_rows=np.all(arr,axis=1)
	arr[:,empty_cols]+=2
	arr[empty_rows,:]+=2

	empty_cols=np.nonzero(empty_cols)[0]
	empty_rows=np.nonzero(empty_rows)[0]

	galaxies=[{"l":x} for x in zip(*np.nonzero(arr==0))]
	for gidx in range(len(galaxies)):
		row,col=galaxies[gidx]["l"]
		galaxies[gidx]["q"]=(
			np.searchsorted(empty_rows,row),
			np.searchsorted(empty_cols,col)
		)


	result=0
	exp=999999

	for i in range(len(galaxies)):
		for j in range(i+1,len(galaxies)):
			if not i==j:
				gil=galaxies[i]["l"]
				gjl=galaxies[j]["l"]
				giq=galaxies[i]["q"]
				gjq=galaxies[j]["q"]
				drl=abs(gil[0]-gjl[0])
				dcl=abs(gil[1]-gjl[1])
				drq=abs(giq[0]-gjq[0])*exp
				dcq=abs(giq[1]-gjq[1])*exp
				# print(f"{gil=},{gjl=},{drl=},{dcl=},{drq=},{dcq=}")
				result+=drl+dcl+drq+dcq

			# if result>50:
				# break

	print(result)
	# for galaxy in galaxies:
	# 	print(galaxy)

	# plt.imshow(arr)
	# plt.show()


main()