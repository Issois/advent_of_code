import numpy as np
import matplotlib.pyplot as plt
def main():

	with open("input") as f:
	# with open("example1_405") as f:
		matrices=f.read().split("\n\n")


	result=0
	mslen=str(len(matrices))
	target=3
	for idx,matrix in enumerate(matrices):
		# if idx+1<target:
			# continue
		# if idx+1>target:
			# break
		# print()
		# mlen=len(matrix)
		first_result,mlen=check(matrix,get_count=True)
		first_result=first_result[0]
		# print(res)
		success=None
		print(f" checked  {idx+1}/{mslen}")
		for i in range(mlen):
			# if i>2:break
			sec_result=check(matrix,bitflip_index=i)

			# print(f" checked  {idx+1}/{mslen}, {i}/{mlen}, {first_result} {sec_result}")
			# return
			if len(sec_result)>0:
				for sr in sec_result:
					if sr!=first_result:
						success=sr
						# print(success)
						break
		if success is not None:
			result+=success[0]*(1 if success[1]=="c" else 100)
		else:
			print("COULD NOT FIND SECOND")
			return
		# break
		# if res is not None:
	print(result)

def check(matrix,bitflip_index=None,get_count=False):
	arr=(np.array([list(x) for x in matrix.split("\n")])=="#").astype(dtype=int)
	if bitflip_index is not None:
		colcount=arr.shape[1]
		row=bitflip_index//colcount
		col=bitflip_index%colcount
		arr[row,col]=1-arr[row,col]
		# print(arr)
	# print(arr)
	# return
	# print()
	exp_rows=2**np.arange(arr.shape[1],0,-1)-1
	exp_cols=2**np.arange(arr.shape[0],0,-1)-1
	nums_rows=np.sum( arr  *exp_rows   ,axis=1)
	nums_cols=np.sum((arr.T*exp_cols).T,axis=0)

	mirrors=[]
	for x,rc in [(nums_rows,"r"),(nums_cols,"c")]:
		y=x[None,:]-x[:,None]
		np.fill_diagonal(y,1)
		y=1-(np.fliplr(y)==0)
		# plt.imshow(y)
		# plt.show()
		offsets=np.arange(x.shape[0]-1)*2
		offsets-=offsets[-1]//2
		# print(f" matrix {idx} check {rc}, shape: {x.shape[0]}.")
		for idx_offs,offs in enumerate(offsets):
			trace=np.trace(y,offset=-offs)
			if trace==0:
				mirrors.append((idx_offs+1,rc))

	if get_count:
		return mirrors,arr.shape[0]*arr.shape[1]
	else:
		return mirrors

			# print(f" matrix {idx} is mirror on {rc} with {mirror}.")

main()