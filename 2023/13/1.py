import numpy as np
import matplotlib.pyplot as plt
def main():

	with open("input") as f:
	# with open("example1_405") as f:
		matrices=f.read().split("\n\n")

	result=0

	for idx,matrix in enumerate(matrices):
		arr=(np.array([list(x) for x in matrix.split("\n")])=="#").astype(dtype=int)
		print()
		exp_rows=2**np.arange(arr.shape[1],0,-1)-1
		exp_cols=2**np.arange(arr.shape[0],0,-1)-1
		nums_rows=np.sum( arr  *exp_rows   ,axis=1)
		nums_cols=np.sum((arr.T*exp_cols).T,axis=0)

		for x,rc in [(nums_rows,"r"),(nums_cols,"c")]:
			y=x[None,:]-x[:,None]
			np.fill_diagonal(y,1)
			y=1-(np.fliplr(y)==0)
			mirror=None
			offsets=np.arange(x.shape[0]-1)*2
			offsets-=offsets[-1]//2
			print(f" matrix {idx} check {rc}, shape: {x.shape[0]}.")
			for idx_offs,offs in enumerate(offsets):
				trace=np.trace(y,offset=-offs)
				if trace==0:
					mirror=idx_offs+1

			if mirror is not None:
				result+=mirror*(1 if rc=="c" else 100)
				print(f" matrix {idx} is mirror on {rc} with {mirror}.")
	print(result)

main()