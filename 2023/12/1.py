import numpy as np
def main():
	with open("input") as f:
		inp=f.read().split("\n")

	BROKEN=0
	UNKNOWN=1
	FUNCTIONAL=2

	result=0

	for idx,row in enumerate(inp):
		print(f"Checking {idx+1}/{len(inp)}")
		springs,grps=row.split(" ")
		grps=np.array([int(x) for x in grps.split(",")])
		springs=springs.replace("#",str(BROKEN)).replace("?",str(UNKNOWN)).replace(".",str(FUNCTIONAL))
		springs=np.array([int(x) for x in springs],dtype=int)

		missing=springs.shape[0]-sum(grps)

		grps2=np.zeros(((grps.shape[0]*2)+1),dtype=int)

		grps2[1::2]=grps

		sub_res=0

		test=np.ones(springs.shape,dtype=int)
		for arr in perms2(len(grps)+1,missing):
			grps2[::2]=arr
			insert_offset=0
			for i in range(grps2.shape[0]):
				if i%2==0:
					if grps2[i]>0:
						test[insert_offset:insert_offset+grps2[i]]=np.zeros((grps2[i]))+FUNCTIONAL
						insert_offset+=grps2[i]
				else:
					if grps2[i]>0:
						test[insert_offset:insert_offset+grps2[i]]=np.zeros((grps2[i]))+BROKEN
						insert_offset+=grps2[i]
			errs=np.abs(test-springs)
			errs=np.any(errs>1)
			if not errs:
				sub_res+=1

		print(sub_res)
		result+=sub_res


	print()
	print(result)

def spring_perms(spaces,elements):
	pass

def perms2(spaces,elements):
	arr=np.zeros((spaces),dtype=int)
	center_spaces=spaces-2
	const_elements=np.ones((center_spaces),dtype=int)
	moving_elements=elements-center_spaces
	for edge_elements in range(moving_elements+1):
		center_elements=moving_elements-edge_elements
		for p2 in perms(2,edge_elements):
			for pX in perms(spaces-2,center_elements):
				arr[0]=p2[0]
				arr[-1]=p2[-1]
				arr[1:-1]=pX+const_elements
				yield arr




def perms(spaces,elements):

	arr=np.zeros((spaces),dtype=int)
	arr[0]=elements
	yield arr
	while arr[-1]<elements:
		idx=np.nonzero(arr)[0][0]
		if idx==0:
			arr[0]-=1
			arr[1]+=1
		else:
			arr[0]=arr[idx]-1
			arr[idx]=0
			arr[idx+1]+=1
		yield arr






def dsum(n):
	s=0
	while n:
		s+=n% 10
		n//=10
	return s





main()