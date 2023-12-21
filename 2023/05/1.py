

def main():

	with open("input") as f:
		inp=f.read()

	paras=inp.split("\n\n")

	seeds=[int(x) for x in paras[0].split(": ")[1].split(" ")]

	order=[
		"seed",
		"soil",
		"fertilizer",
		"water",
		"light",
		"temperature",
		"humidity",
	]

	maps={}

	for para in paras[1:]:
		lines=para.split("\n")
		header=lines[0].split("-")[0]
		maps[header]=[]
		for line in lines[1:]:
			arr=[int(x) for x in line.split(" ")]
			maps[header].append({"s":arr[1],"d":arr[0],"l":arr[2]})

	locs=[]

	for seed in seeds:
		print(seed)
		value=seed
		for header in order:
			print(f"- {header} {value}")
			for mp in maps[header]:
				source=mp["s"]
				dest=mp["d"]
				length=mp["l"]
				if source<=value<source+length:
					value=dest+(value-source)
					# print(f"-- value maps to {value}")
					break
		locs.append(value)


	print(locs)
	print(min(locs))


main()
