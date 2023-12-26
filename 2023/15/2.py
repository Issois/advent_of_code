import sys
def main():

	with open("example1" if "e" in sys.argv else "input") as f:
		inp=f.read().split(",")

	boxes=[[] for _ in range(2**8)]

	for instr_idx,instruction in enumerate(inp):

		print(f"{instr_idx+1}/{len(inp)}: {instruction}")

		if instruction[-1]=="-":
			# REMOVE
			label=instruction[:-1]
			box_idx=hash_str(label)
			box=boxes[box_idx]
			for inside_box_idx in range(len(box)):
				# print(box[inside_box_idx])
				if box[inside_box_idx][:-1]==label:
					print(f"  REMOVE {label} from box {box_idx} {box}")
					box.pop(inside_box_idx)
					break
		else:
			# APPEND or REPLACE
			lens="".join(instruction.split("="))
			# lens=instruction.remove("=")
			box_idx=hash_str(lens[:-1])
			box=boxes[box_idx]
			found=False
			for inside_box_idx in range(len(box)):
				if box[inside_box_idx][:-1]==lens[:-1]:
					print(f"  REPLACE {box[inside_box_idx]} with {lens} from box {box_idx} {box}")
					box[inside_box_idx]=lens
					found=True
			if not found:
				print(f"  ADD {lens} to box {box_idx} {box}")
				box.append(lens)
	result=0

	for bidx,box in enumerate(boxes):
		if len(box)>0:
			print(bidx,box)

		for lidx,lens in enumerate(box):
			result+=((bidx+1)*(lidx+1)*int(lens[-1]))
	print(f"ANSWER: {result}")
	# 263211


def hash_str(s):
	return hash_arr([ord(c) for c in s])

def hash_arr(nums):
	s=0
	for num in nums:
		s=hash(num+s)
	return s
def hash(num):
	return (17*num)%256

main()