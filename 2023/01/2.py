
def main():
	with open("data.input") as f:
		inp=f.read().splitlines()

	digits=[
		# "zero",
		"one",
		"two",
		"three",
		"four",
		"five",
		"six",
		"seven",
		"eight",
		"nine",
	]

	dd={digits[i-1]:str(i) for i in range(1,10)}
	# inp=inp[78:80]

	tree={}
	for digit in digits:
		leaf_ref=tree
		for ch in digit:
			if ch not in leaf_ref:
				leaf_ref[ch]={}

			leaf_ref=leaf_ref[ch]
		leaf_ref["_"]=digit
	# print(tree)
	# return

	res=0
	for line in inp:
		print(f"{line=}")
		first=None
		last=None
		leaf_ref=tree
		depth=0
		ch_idx=0
		while ch_idx<len(line):
			ch=line[ch_idx]
			print(f"  {ch_idx:2} {ch} {depth} {''.join(leaf_ref.keys())}")
			num=None
			if ch in "123456789":
				num=ch
				leaf_ref=tree
				depth=0
			elif ch in leaf_ref:
				# print(f" ! {ch=}")
				leaf_ref=leaf_ref[ch]
				depth+=1
				if "_" in leaf_ref:
					num=dd[leaf_ref["_"]]
					ch_idx-=len(leaf_ref["_"])-1
					leaf_ref=tree
					depth=0
			else:
				# print("- MISSED")
				leaf_ref=tree
				if depth>0:
					ch_idx-=depth
					depth=0
			if num is not None:
				print(f"- found {num=}")
				if first is None:
					first=num
					last=num
				else:
					last=num
			ch_idx+=1

		comb_num=int(first+last)
		print(f"{comb_num=}")
		res+=comb_num
	print(f"{res=}")

main()