

def main():

	with open("input") as f:
		inp=f.read().replace(" ","").splitlines()


	# inp=inp[:2]

	rgb={"r":12,"g":13,"b":14}
	lfc={"d": 3,"n": 5,"e": 4}
	result=0
	for lidx,line in enumerate(inp):
		gidx=lidx+1
		pulls=line.split(":")[1].split(";")
		invalid=False
		min_rgb={"r":0,"g":0,"b":0}
		for pidx,pull in enumerate(pulls):
			draws=pull.split(",")
			for didx,draw in enumerate(draws):
				splt_idx=len(draw)-lfc[draw[-1]]
				num=int(draw[:splt_idx])
				col=draw[splt_idx]
				min_rgb[col]=max(num,min_rgb[col])
				# if int(num)>rgb[col]:
				# 	print(f"invalid: {gidx:3} {pidx+1:2} {didx+1:2}: {num}{col}")
				# 	invalid=True
		power=1
		for val in min_rgb.values():
			power*=val
		print(f"game {gidx}: {min_rgb} {power}")

		result+=power
		# if not invalid:
			# print(gidx)
			# result+=gidx
	print(result)



main()