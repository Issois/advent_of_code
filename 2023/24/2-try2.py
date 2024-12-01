import numpy as np
import sys
import matplotlib.pyplot as plt

X=0
Y=1
Z=2

POS=0
VEL=1
RNG=np.random.default_rng()

def main():

	with open(sys.argv[1]) as f:
		inp=f.read().split("\n")

	# beam_arrs=np.zeros((len(inp),2,3))

	# arr=np.zeros((len(inp),3,2),dtype=np.longlong)
	beams=[]
	for idx,line in enumerate(inp):
		beam_arr=np.array([[int(num) for num in subline.split(",")] for subline in line.split("@")])
		# beam_arrs[idx,POS,:]=beam_arr[0]
		# beam_arrs[idx,VEL,:]=beam_arr[1]
		beams.append(Beam(beam_arr[0],beam_arr[1]))
	# beams=[Beam(beam[:3],beam[3:]) for beam in beam_arrs]
	beams=beams[:3]
	vtime_start=np.array([400,401,402])
	vtime=vtime_start
	# ts=t_start
	finished=False
	trace=[vtime_start]
	vals=[]
	# while not finished:
	for itera in range(1500):
		print(itera)
		# result=zero(beams[:3],ts)
		vtime_envs=env(vtime,10)
		idx_min=None
		val_min=None
		for idx,vtime_env in enumerate(vtime_envs):
			res=zero(beams,vtime_env)
			if not (np.isinf(res) or np.isnan(res)):
				if val_min is None or res<val_min:
					val_min=res
					idx_min=idx
		if idx_min is None:
			break

		vtime=vtime_envs[idx_min]
		vals.append(val_min)
		trace.append(vtime.copy())

	AX1=0
	AX2=1
	AX3=2

	x=[vtime[AX1] for vtime in trace]
	y=[vtime[AX2] for vtime in trace]
	z=[vtime[AX3] for vtime in trace]
	ax = plt.figure().add_subplot(111, projection='3d')
	plt.plot(vtime_start[AX1],vtime_start[AX2],vtime_start[AX3],marker="x")
	plt.plot([0,vtime_start[AX1]],[0,vtime_start[AX2]],[0,0],marker="o")
	plt.plot(x,y,z)
	plt.show()
	# plt.plot(vals)
	# plt.show()
	# plt.plot(vtime_start[AX1],vtime_start[AX2],marker="x")
	# plt.plot(x,y)
	# plt.show()
	# plt.plot(vals)
	# plt.show()


	# NX,NY=500,500
	# result=np.zeros((NX,NY))
	# for nx in range(NX):
		# print(nx)
		# for ny in range(NY):
			# res=zero(beams[:3],[nx,ny,0])
			# print(res)
			# result[nx,ny]=np.linalg.norm(res)

	# plt.imshow(result)
	# plt.show()


	# for i in range(beam_arrs.shape[0]):
	# 	for j in range(i+1,beam_arrs.shape[0]):
	# 		if are_parallel(beam_arrs[i],beam_arrs[j],[X,Y]):
	# 			print(f"PARA {i} {j}")

			# return

def env(ts,radius):
	cnt=10
	values=RNG.standard_normal(3*cnt)*radius
	results=[]
	for idx in range(cnt):
		res=np.zeros((3))
		for i in range(3):
			res[i]=ts[i]+values[(3*idx)+i]
		if np.all(res>0):
			results.append(res)
	return results


def zero(beams,times):
	return np.linalg.norm(
		((beams[1].point(times[1])-beams[0].point(times[0]))
		/(times[1]-times[0]))
		-
		((beams[2].point(times[2])-beams[1].point(times[1]))
		/(times[2]-times[1]))
	)


class Beam:
	def __init__(self,pos,vel):
		self.pos=pos
		self.vel=vel

	def point(self,time):
		return self.pos+(time*self.vel)

	def __str__(self):
		return f"{self.pos}+{self.vel}"

def are_parallel(arr1,arr2,axes):
	arr1=np.array(list(arr1[VEL][axes])+[0])
	arr2=np.array(list(arr2[VEL][axes])+[0])
	return np.linalg.norm(np.cross(arr1,arr2))==0





main()

