import sys
def main():

	with open("example1" if "e" in sys.argv else "input") as f:
		inp=f.read().split(",")

	# print(inp)
	# hashs=[[ord(y) for y in x] for x in inp]
	# print(hashs)
	# hashs=[hash_arr([ord(y) for y in x]) for x in inp]
	# print(hashs)
	# return
	# print(asc)

	boxes=[[] for _ in range(2**8)]

	for instr_idx,instruction in enumerate(inp):

		if instruction[-1]=="-":
			# REMOVE
			label=instruction[:-1]
			box_idx=hash_str(label)
			box=boxes[box_idx]
			print(f"REMOVE {label} from box {box_idx} {box}")
			for inside_box_idx in range(len(box)):
				# print(box[inside_box_idx])
				if box[inside_box_idx][0]==label:
					box.pop(inside_box_idx)
					break
		else:
			# APPEND or REPLACE
			lens=instruction.split("=")
			box_idx=hash_str(lens[0])
			box=boxes[box_idx]
			found=False
			for inside_box_idx in range(len(box)):
				if box[inside_box_idx][0]==lens[0]:
					print(f"REPLACE {label[0]} from box {box_idx} {box}")
					box[inside_box_idx]=lens
					found=True
			if not found:
				print(f"ADD {lens[0]} to box {box_idx} {box}")
				box.append(lens)
	result=0
	# return

	for bidx,box in enumerate(boxes):
		if len(box)>0:
			print(bidx,box)

		for lidx,lens in enumerate(box):
			result+=((bidx+1)*(lidx+1)*int(lens[1]))
	print(f"ANSWER: {result}")
	# 263221





	# boxes[0].append(1)
	# print(boxes)

	# result=0
	# for ords in asc:
		# sub_result=hash_arr(ords)
		# print(sub_result)
		# result+=sub_result
	# print(f"ANSWER: {result}")

def hash_str(s):
	return hash_arr([ord(c) for c in s])

def hash_arr(nums):
	# print(nums)
	s=0
	for num in nums:
		s=hash(num+s)
	return s
def hash(num):
	return (17*num)%256

main()