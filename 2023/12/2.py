import numpy as np
def main():
	with open("input-small") as f:
	# with open("input") as f:
		inp=f.read().split("\n")

	BROKEN=0
	UNKNOWN=1
	FUNCTIONAL=2

	result=0

	for idx,row in enumerate(inp):
		print(f"Checking {idx+1}/{len(inp)}")
		springs,grps=row.split(" ")

		folded=True
		if not folded:
			springs="?".join([springs]*5)
			grps=",".join([grps]*5)

		# print(grps)
		# print(grps)
		# return

		grps=np.array([int(x) for x in grps.split(",")])
		springs=springs.replace("#",str(BROKEN)).replace("?",str(UNKNOWN)).replace(".",str(FUNCTIONAL))
		springs=np.array([int(x) for x in springs],dtype=int)

		# missing=springs.shape[0]-sum(grps)

		inserts=np.nonzero(springs==1)[0]
		insert_idx=0
		insert_count=inserts.shape[0]
		sub_res=0
		# print(inserts)
		test=springs.copy()
		# while insert_idx<len(inserts):
		# 	# for state in [BROKEN,FUNCTIONAL]:
		# 	test[inserts[insert_idx]]=BROKEN
		# 	if is_correct(test,springs):
		# 		if insert_idx==insert_count-1:
		# 			sub_res+=1
		# 		else:
		# 			insert_idx+=1


		# print(test)

		break

		print(sub_res)
		result+=sub_res
		# return

	print()
	print(result)

def check(test,springs,inserts,insert_idx):


def is_correct(test,springs):
	errs=np.abs(test-springs)
	return not np.any(errs>1)


main()