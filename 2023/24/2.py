
import numpy as np
import sys
import matplotlib.pyplot as plt
import math

IDX=0
AXS=1
DIM=2

X=0
Y=1
Z=2

POS=0
VEL=1

class Beam:
	def __init__(self,pos,vel):
		self.pos=pos
		self.vel=vel

	def point(self,time):
		return self.pos+(time*self.vel)

	def __str__(self):
		return f"{self.pos}+{self.vel}"

	def angles(self):
		return math.atan2(self.vel[X],self.vel[Y]),math.atan2(self.vel[X],self.vel[Z])



def main():
	with open(sys.argv[1]) as f:
		inp=f.read().split("\n")

	# xymin,xymax=[int(num) for num in inp[0].split(",")]
	# inp=inp[1:]
	beams=[]
	angles_xy=np.zeros((len(inp)))
	angles_xz=np.zeros((len(inp)))

	beam_arrs=np.zeros((len(inp),6))

	# arr=np.zeros((len(inp),3,2),dtype=np.longlong)
	for idx,line in enumerate(inp):
		beam_arr=np.array([[int(num) for num in subline.split(",")] for subline in line.split("@")])
		beam_arrs[idx,0:3]=beam_arr[0]
		beam_arrs[idx,3:6]=beam_arr[1]
		# beams.append(Beam(*beam_arr))
		axy,axz=Beam(*beam_arr).angles()
		angles_xy[idx]=axy
		angles_xz[idx]=axz

	# beam_arrs[:,0:3]=0


	_,ax=plt.subplots(subplot_kw={"projection": "3d"})
	ax.quiver(
		beam_arrs[:,0],
		beam_arrs[:,1],
		beam_arrs[:,2],
		beam_arrs[:,3],
		beam_arrs[:,4],
		beam_arrs[:,5],
		# length=0.4,
		arrow_length_ratio=0,
		# normalize=True
	)
	# ax.quiver(1,0,0,.1,0,0,color="green")
	# ax.quiver(0,1,0,0,.1,0)
	# ax.quiver(0,0,1,0,0,.1,color="red")
	# ax.quiver(-1,0,0,-.1,0,0,color="green")
	# ax.quiver(0,-1,0,0,-.1,0)
	# ax.quiver(0,0,-1,0,0,-.1,color="red")
	plt.show()

	# plt.scatter(angles_xy,angles_xz)
	# plt.grid()
	# plt.show()


		# print(beam)


		# arr[idx]=line_arr.T

	# arr=arr[:,(X,Y),:]


	# fig=plt.figure()
	# ax=fig.add_subplot(111, projection='3d')

	# for i in range(arr.shape[0]):
	# 	ax.plot(arr[i,(X,Y),POS],arr[i,(X,Y),POS]+2*arr[i,(X,Y),VEL],zs=[arr[i,Z,POS],arr[i,Z,POS]+2*arr[i,Z,VEL]])
	# plt.show()


	# for i in range(arr.shape[0]):
	# 	for j in range(i+1,arr.shape[0]):
			# vec_p=arr[i,:,POS]-arr[j,:,POS]

			# mat=np.vstack([arr[i,:,POS],arr[i,:,VEL],-arr[j,:,VEL]]).T
			# mat_inv=np.linalg.inv(mat)
			# print(mat@mat_inv)
			# k=mat_inv@arr[j,:,POS]
			# print(k)

			# mat=np.vstack([arr[i,:,VEL],-arr[j,:,VEL]]).T
			# print(mat)
			# mat_inv=np.linalg.inv(mat)
			# print(mat@mat_inv)
			# k=mat_inv@(arr[j,:,POS]-arr[i,:,POS])
			# print(k)
			# print(mat)


			# print(k1,k2)

			# print(arr[i,:,POS]+(ki*arr[i,:,VEL]))
			# print(arr[j,:,POS]+(kj*arr[j,:,VEL]))

			# return
			# quot=arr[i,:,VEL]/arr[j,:,VEL]
			# if np.all(quot==1):
				# print(f"{i} and {j} are parallel.")


	result=0

	# np.seterr(all="ignore")

	# for i in range(arr.shape[0]):
	# 	for j in range(i+1,arr.shape[0]):
	# 		x,y=intersection(arr[i],arr[j])
	# 		if y is None:
	# 			pass
	# 			# print(f". {x} {i} {j}")
	# 		else:
	# 			if xymin<=x<=xymax and xymin<=y<=xymax:
	# 				result+=1
	# 				print("+ intersect inside",i,j,x,y)
	# 			else:
	# 				pass
	# 				# print(". intersect outside",i,j,x,y)


	print(f"ANSWER: {result}")
	# _ is _!


# def intersection(h1,h2):
# 	dp=h2[:,POS]-h1[:,POS]
# 	k2=(
# 		 (-dp[Y]+(h1[Y,VEL]*dp[X]/h1[X,VEL]))
# 		/(h2[Y,VEL]-(h1[Y,VEL]*h2[X,VEL]/h1[X,VEL]))
# 	)
# 	k1=(dp[X]+(k2*h2[X,VEL]))/h1[X,VEL]

# 	# print("--------",k1,k2)
# 	if not np.isfinite(k2):
# 		return "no intersection",None
# 	if k1<0 or k2<0:
# 		return "t<0",None
# 	else:
# 		return h2[:,POS]+k2*h2[:,VEL]

main()
