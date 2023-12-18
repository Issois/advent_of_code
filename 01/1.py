
def main():
	with open("1.inp") as f:
		inp=f.readlines()


	res=0
	for line in inp:
		first=None
		last=None
		for ch in line:
			if ch in "123456789":
				if first is None:
					first=ch
					last=ch
				else:
					last=ch
		num=int(first+last)
		print(f"{num=},{line=}")
		res+=num
	print(f"{res=}")

main()