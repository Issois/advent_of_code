import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.signal import convolve2d
import sys

ROW=0
COL=1

def main():
	with open("example1" if "e" in sys.argv else "input") as f:
		cost=np.array([[int(y) for y in x] for x in f.read().split("\n")])
	result=0

	total=np.zeros(cost.shape,dtype=np.int32)+np.iinfo(np.int32).max

	total[0,0]=0

	checks=np.nonzero(total)
	checks=[(r,c) for r,c in zip(*checks)][::-1]

	while len(checks)>0:
		check=checks.pop()
		print(f"Checking {check}")
		# get neighbors
		#

		# checlk

	# print(checks)

	# for row in range(total.shape[ROW]):
		# for col in range(total.shape[COL]):
		# 	# if
	# print(total)






	# img=np.zeros((50,50))
	# img[20,25]=1

	# fig,ax=plt.subplots()
	# kernel=np.array([0,1,1,1,0,1,0,1,0]).reshape((3,3))
	# # kernel=1-kernel
	# # kernel[1,1]=10
	# kernel=1.1*kernel/np.sum(kernel)

	# i=0

	# aximg=ax.imshow(img)


	# def update(frame):
	# 	nonlocal img,kernel,aximg,i
	# 	i+=1
	# 	if i>50:
	# 		kernel=1-kernel
	# 		i=0
	# 	img=convolve2d(img,kernel,mode="same",boundary="fill",fillvalue=0)
	# 	img[img>1]=1
	# 	aximg.set_data(img)
	# 	# print(img)
	# 	return None

	# ani=animation.FuncAnimation(fig=fig,func=update,frames=40,interval=20)

	# plt.show()


	# plt.imshow(img)
	# plt.show()






	# print(f"ANSWER: {result}")
main()
