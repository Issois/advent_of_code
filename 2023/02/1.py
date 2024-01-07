

def main():

	with open("data.input") as f:
		inp=f.read().replace(" ","").splitlines()


	# inp=inp[:2]

	rgb={"r":12,"g":13,"b":14}
	lfc={"d": 3,"n": 5,"e": 4}
	result=0
	for lidx,line in enumerate(inp):
		gidx=lidx+1
		pulls=line.split(":")[1].split(";")
		invalid=False
		for pidx,pull in enumerate(pulls):
			if invalid:break
			draws=pull.split(",")
			for didx,draw in enumerate(draws):
				if invalid:break
				splt_idx=len(draw)-lfc[draw[-1]]
				num=draw[:splt_idx]
				col=draw[splt_idx]
				if int(num)>rgb[col]:
					print(f"invalid: {gidx:3} {pidx+1:2} {didx+1:2}: {num}{col}")
					invalid=True

		if not invalid:
			print(gidx)
			result+=gidx
	print(result)



main()