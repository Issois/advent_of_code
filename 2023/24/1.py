
import numpy as np
import sys

IDX=0
AXS=1
DIM=2

X=0
Y=1
Z=2

POS=0
VEL=1

def main():
	with open(sys.argv[1]) as f:
		inp=f.read().split("\n")

	xymin,xymax=[int(num) for num in inp[0].split(",")]
	inp=inp[1:]

	arr=np.zeros((len(inp),3,2),dtype=np.longlong)

	for idx,line in enumerate(inp):
		line_arr=np.array([[int(num) for num in subline.split(",")] for subline in line.split("@")])
		arr[idx]=line_arr.T

	arr=arr[:,(X,Y),:]

	result=0

	# np.seterr(all="ignore")

	for i in range(arr.shape[0]):
		for j in range(i+1,arr.shape[0]):
			x,y=intersection(arr[i],arr[j])
			if y is None:
				pass
				# print(f". {x} {i} {j}")
			else:
				if xymin<=x<=xymax and xymin<=y<=xymax:
					result+=1
					print("+ intersect inside",i,j,x,y)
				else:
					pass
					# print(". intersect outside",i,j,x,y)


	print(f"ANSWER: {result}")
	# 25261 is correct!


def intersection(h1,h2):
	dp=h2[:,POS]-h1[:,POS]
	k2=(
		 (-dp[Y]+(h1[Y,VEL]*dp[X]/h1[X,VEL]))
		/(h2[Y,VEL]-(h1[Y,VEL]*h2[X,VEL]/h1[X,VEL]))
	)
	k1=(dp[X]+(k2*h2[X,VEL]))/h1[X,VEL]

	# print("--------",k1,k2)
	if not np.isfinite(k2):
		return "no intersection",None
	if k1<0 or k2<0:
		return "t<0",None
	else:
		return h2[:,POS]+k2*h2[:,VEL]

main()
