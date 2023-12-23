import numpy as np
def main():
	# with open("input-small") as f:
	with open("input") as f:
		inp=f.read().split("\n")

	result=0

	for idx,row in enumerate(inp):
		print(f"Checking {idx+1}/{len(inp)}")
		springs,grps=row.split(" ")
		grps=np.array([int(x) for x in grps.split(",")])
		springs=springs.replace("#","0").replace("?","1").replace(".","2")
		springs=np.array([int(x) for x in springs],dtype=int)
		# springs=np.array(springs,dtype=int)
		# print(springs)
		# return

		missing=springs.shape[0]-sum(grps)
		# grps=[np.array([0]*grp) for grp in grps]

		grps2=np.zeros(((grps.shape[0]*2)+1),dtype=int)

		# print(grps2[::2])
		grps2[1::2]=grps

		sub_res=0

		test=np.ones(springs.shape,dtype=int)
		for arr in perms2(len(grps)+1,missing):
			# x=list(arr)
			grps2[::2]=arr
			insert_offset=0
			for i in range(grps2.shape[0]):
				if i%2==0:
					if grps2[i]>0:
						test[insert_offset:insert_offset+grps2[i]]=np.zeros((grps2[i]))+2
						insert_offset+=grps2[i]
				else:
					if grps2[i]>0:
						test[insert_offset:insert_offset+grps2[i]]=np.zeros((grps2[i]))
						insert_offset+=grps2[i]

			errs=np.abs(test-springs)
			errs=np.any(errs>1)
			# print()
			if not errs:
				sub_res+=1

			# print(arr)
		print(sub_res)
		result+=sub_res
		# print(missing)


		# print(springs)
		# if idx>0:
			# break
	print()
	print(result)

def spring_perms(spaces,elements):
	pass

def perms2(spaces,elements):
	arr=np.zeros((spaces),dtype=int)
	center_spaces=spaces-2
	const_elements=np.ones((center_spaces),dtype=int)
	moving_elements=elements-center_spaces
	# print(moving_elements)
	for edge_elements in range(moving_elements+1):
		center_elements=moving_elements-edge_elements
		for p2 in perms(2,edge_elements):
			# print(p2)
			for pX in perms(spaces-2,center_elements):
				arr[0]=p2[0]
				arr[-1]=p2[-1]
				arr[1:-1]=pX+const_elements
				yield arr




def perms(spaces,elements):

	# arr=[0]*spaces
	# arr[0]=elements
	# while arr[-1]<elements:
	# 	yield arr
	# 	if arr[0]==0:
	# 		arr[2]+=1
	# 		arr[0]=arr[1]-1
	# 		arr[1]=0
	# 	arr[0]-=1
	# 	arr[1]+=1
	# yield arr


	arr=np.zeros((spaces),dtype=int)
	i=elements
	mx=elements*(10**(spaces-1))
	while i<=mx:
		if dsum(i)==elements:
			temp=np.array([int(x) for x in str(i)])
			arr[-temp.shape[0]:]=temp
			yield arr
		i+=1

		# if i%10==0:
		# 	i+=54
		# else:
		# 	i+=9
		# yield i

		# print(i)

def dsum(n):
	s=0
	while n:
		s+=n% 10
		n//=10
	return s


# def check_valid(test,record,grps):



main()