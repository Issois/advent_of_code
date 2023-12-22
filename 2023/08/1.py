import re
def main():
	with open("input") as f:
		inp=f.read().split("\n")

	instructions=[to_idx(rl) for rl in inp[0]]
	# print(instructions)
	mp={}
	word="([A-Z]{3})"
	rgx=re.compile(fr"{word} = \({word}, {word}\)")
	for line in inp[2:]:
		l1,l2,l3=rgx.match(line).groups()
		mp[l1]=(l2,l3)

	loc="AAA"
	step_count=0
	next_instruction=0
	instr_count=len(instructions)
	while loc!="ZZZ":
		loc=mp[loc][instructions[next_instruction]]
		step_count+=1
		print(instructions[next_instruction],loc)
		next_instruction=(next_instruction+1)%instr_count
		# if step_count>10:
			# break

	print(step_count)


def to_idx(rl):
	return ord(rl)//82

main()