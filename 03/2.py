
import numpy as np
import matplotlib.pyplot as plt
import scipy


def main():

	with open("input") as f:
		inp=f.read()

	lines=inp.splitlines()


	matrix=[list(line) for line in lines]

	arr_str=np.array(matrix,dtype=str)
	ast_mask=arr_str=="*"

	result=0
	nrows=[-1,-1,-1, 0, 0, 1, 1, 1]
	ncols=[-1, 0, 1,-1, 1,-1, 0, 1]

	arows,acols=np.nonzero(ast_mask)

	def is_number(x):
		return x in "0123456789"

	def is_next_to(a,b):
		return a[0]==b[0] and abs(a[1]-b[1])==1

	for aidx in range(arows.shape[0]):
	# for aidx in range(3):
		print(aidx)
		ar=arows[aidx]
		ac=acols[aidx]
		# neighbor numbers
		nnums=[]
		for nidx in range(len(nrows)):
			nr=ar+nrows[nidx]
			nc=ac+ncols[nidx]
			neighbor=arr_str[nr,nc]
			if is_number(neighbor):
				nnums.append((nr,nc))
		grp_cnt=0

		grps=[]
		for nnum in nnums:
			grp_found=False
			for grp in grps:
				for elem in grp:
					if is_next_to(elem,nnum):
						grp_found=True
						break
				if grp_found:
					break
			if grp_found:
				grp.append(nnum)
			else:
				grps.append([nnum])

		if len(grps)==2:
			# print("- Gear found!")
			ratio=1
			for grp in grps:
				# print("- "+str(grp))
				num=[arr_str[x] for x in grp]
				first=grp[0]
				last=grp[-1]
				offset=-1
				if first[1]+offset>=0:
					other_num=arr_str[first[0],first[1]+offset]
					while is_number(other_num):
						num.insert(0,other_num)
						offset-=1
						if first[1]+offset<0:
							break
						other_num=arr_str[first[0],first[1]+offset]


				offset=1
				if first[1]+offset<arr_str.shape[1]:
					other_num=arr_str[last[0],last[1]+offset]
					while is_number(other_num):
						num.append(other_num)
						offset+=1
						if first[1]+offset>=arr_str.shape[1]:
							break
						other_num=arr_str[last[0],last[1]+offset]


				num="".join(num)
				print("- found "+num)
				ratio*=int(num)
			result+=ratio



	print(result)




def convolve(arr,a,b,c):
	print("  [CONVOLVE]")
	kernel=np.array([[c,b,c],[b,a,b],[c,b,c]])
	return scipy.signal.convolve2d(arr,kernel,mode="same")



main()
