
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

	def meet(self,other,axes=[0,1]):
		self.pos2=self.pos[axes]
		self.vel2=self.vel[axes]
		other.pos2=other.pos[axes]
		other.vel2=other.vel[axes]

		mat=np.array((self.vel2,-other.vel2)).T
		# print(mat)
		try:
			mat=np.linalg.inv(mat)
		except:
			return None
		t1,t2=mat@(other.pos2-self.pos2)
		# print(t1,t2)
		# return
		meet_pos=self.pos2+(t1*self.vel2)
		return meet_pos
		# print(other.pos2+(t2*other.vel2))
		# print(self.point(t1))
		# print(other.point(t2))





def equation(beams,times):
	result=(
		 ((beams[1].point(times[1])-beams[0].point(times[0]))/(times[1]-times[0]))
		-((beams[2].point(times[2])-beams[1].point(times[1]))/(times[2]-times[1]))
	)
	return np.linalg.norm(result)



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
		beams.append(Beam(*beam_arr))
		# axy,axz=Beam(*beam_arr).angles()
		# angles_xy[idx]=axy
		# angles_xz[idx]=axz

	# beams.insert(0,Beam(np.array((0,0,0)),np.array((0,1,1))))
	# beams.insert(1,Beam(np.array((4,1,0)),np.array((-1,1,-1))))

	x=[]
	y=[]
	for i in range(len(beams)):
		print(i)
		for j in range(i+1,len(beams)):
			meet_pos=beams[i].meet(beams[j],[0,2])
			if meet_pos is not None:
				if meet_pos[0]<1e20 and meet_pos[1]<1e20:
					x.append(meet_pos[0])
					y.append(meet_pos[1])


			# print(i,j,meet_pos)

	x=np.array(x)
	y=np.array(y)



	# plt.hist(x)
	# plt.show()

	plt.scatter(x,y)
	plt.show()

	# print()
	# print(equation(beams[:3],[1,2,4]))
	# xs=range(10000)
	# ys=[equation(beams[:3],[x,2000,5000]) for x in xs]
	# rang=range(1,10000,100)
	# val=9999999999999
	# mins=[]
	# for t1 in rang:
	# 	print(t1)
	# 	for t2 in rang:
	# 		for t3 in rang:
	# 			if t1!=t2 and t2!=t3 and t1!=t3:
	# 				new_val=equation(beams[:3],[t1,t2,t3])
	# 				if new_val<val:
	# 					val=new_val
	# 					mins.append((t1,t2,t3,val))

	# for mi in mins:
	# 	print(mi)



	# plt.plot(xs,ys)
	# plt.yscale("log")
	# plt.show()

	# beam_arrs[:,0:3]=0
	# para_grps=[[0]]
	# # print(beam_arrs)
	# for idx in range(1,beam_arrs.shape[0]):
	# 	print(f"{idx}/{beam_arrs.shape[0]}",end="")
	# 	is_para=False
	# 	for para_grp_idx in range(len(para_grps)):
	# 		curr=beam_arrs[idx,3:]
	# 		para=beam_arrs[para_grps[para_grp_idx][0],3:]
	# 		# print(curr,para)
	# 		if np.linalg.norm(np.cross(curr,para))==0:
	# 			para_grps[para_grp_idx].append(idx)
	# 			is_para=True
	# 	if not is_para:
	# 		para_grps.append([idx])
	# 		print("")
	# 	else:
	# 		print(" PARA")


	# print(para_grps)


	# _,ax=plt.subplots(subplot_kw={"projection": "3d"})
	# ax.quiver(
	# 	beam_arrs[:,0],
	# 	beam_arrs[:,1],
	# 	beam_arrs[:,2],
	# 	beam_arrs[:,3],
	# 	beam_arrs[:,4],
	# 	beam_arrs[:,5],
	# 	# length=0.4,
	# 	arrow_length_ratio=0,
	# 	# normalize=True
	# )
	# ax.quiver(1,0,0,.1,0,0,color="green")
	# ax.quiver(0,1,0,0,.1,0)
	# ax.quiver(0,0,1,0,0,.1,color="red")
	# ax.quiver(-1,0,0,-.1,0,0,color="green")
	# ax.quiver(0,-1,0,0,-.1,0)
	# ax.quiver(0,0,-1,0,0,-.1,color="red")
	# plt.show()

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
