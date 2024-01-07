import re
import math
def main():
	with open("data.input") as f:
		inp=f.read().split("\n")

	instructions=[to_idx(rl) for rl in inp[0]]
	mp={}
	word="([A-Z]{3})"
	locs=[]
	rgx=re.compile(fr"{word} = \({word}, {word}\)")
	for line in inp[2:]:
		l1,l2,l3=rgx.match(line).groups()
		mp[l1]=(l2,l3)
		if l1[2]=="A":
			locs.append(l1)


	result=math.lcm(*[get_steps(loc,mp,instructions) for loc in locs])
	print(result)

def get_steps(start,mp,instructions):
	step_count=0
	next_instruction=0
	loc=start
	instr_count=len(instructions)
	fin=False
	xlocs=[]
	while not fin:
		# print(loc)

		loc=mp[loc][instructions[next_instruction]]
		step_count+=1

		if loc[2]=="Z":
			xloc=(loc,next_instruction,step_count)
			# print(xloc)
			if not any([loc==l and next_instruction==ni for l,ni,_ in xlocs]):
				xlocs.append(xloc)
			else:
				xlocs.append(xloc)
				fin=True
				print(xlocs)
				print([l[2]/xlocs[0][2] for l in xlocs])
				# print(step_count)
				# return

		# print(instructions[next_instruction],loc)
		next_instruction=(next_instruction+1)%instr_count
	return xlocs[0][2]

def to_idx(rl):
	return ord(rl)//82

main()