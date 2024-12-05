
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
	for update in updates:
		if check_update(order,update) is None:
			result+=int(update[len(update)//2])

	# 5509
	return result

def check_update(order,update):

	for idx_a in range(len(update)):
		for idx_b in range(idx_a,len(update)):
			num_a=update[idx_a]
			num_b=update[idx_b]
			if num_b in order:
				# print(num_a,order[num_b])
				if num_a in order[num_b]:
					return idx_a,idx_b
	return None

def sort_update(order,update):
	new_update=[update[0]]
	for num in update[1:]:
		inserted=False
		insert_idx=0
		# while not inserted:
			# inserted_num=new_update[insert_idx]
		for idx,inserted_num in enumerate(new_update):
			if num in order and inserted_num in order[num]:
				new_update.insert(idx,num)
				inserted=True
				break
			# else:
		if not inserted:
			new_update.append(num)

	return new_update
	

def solve_2(order,updates):
	result=0
		
	for idx_upd,update in enumerate(updates):
		print(idx_upd,len(updates))
		# if idx_upd>10:return
		tup=check_update(order,update)
		if tup is not None:
			new_update=sort_update(order,update)
			result+=int(new_update[len(new_update)//2])

	return result

main()
