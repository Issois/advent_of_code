
import numpy as np
import sys
def main():
	with open(sys.argv[2]) as f:
		inp=f.read().split("\n")

	order={}
	lists=False
	updates=[]
	for line in inp:
		if len(line)==0:
			lists=True
		elif lists:
			updates.append(line.split(","))
		else:
			a,b=line.split("|")
			if a not in order:
				order[a]=set()
			order[a].add(b)

	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]

	print(f"ANSWER: {solve(order,updates)}")

def solve_1(order,updates):
	result=0

	# print(order,updates)
	for update in updates:
		wrong=False
		# for idx in range(len(update)-1,-1,-1):
		for idx_a in range(len(update)):
			for idx_b in range(idx_a,len(update)):
				num_a=update[idx_a]
				num_b=update[idx_b]
				if num_b in order:
					# print(num_a,order[num_b])
					if num_a in order[num_b]:
						wrong=True
						break
			if wrong:
				break
		if not wrong:
			print(update)
			result+=int(update[len(update)//2])

	# 5509
	return result

def solve_2(order,updates):
	result=0
	return result

main()
