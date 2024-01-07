import numpy as np
BROKEN=0
UNKNOWN=1
FUNCTIONAL=2

import time

# DIVIDE AND CONQUER



def main():
	# orig="0022202022000022022222020"
	# arr=np.array([int(x) for x in orig])

	# # arr=arr!=0
	# # arr=arr*1
	# # print(arr+1)
	# print(grps_from_arr(arr))
	# print(orig)
	# print(arr)

	# for a in arr:
		# print(orig[a],orig[a+1])
	# return

	# with open("input-small") as f:
	with open("data.input") as f:
		inp=f.read().split("\n")

	print("START TIMING")
	t0=time.process_time()

	result=0
	target=2
	# for idx,row in enumerate(inp[target:target+1]):
	for idx,row in enumerate(inp):
		# if idx<target:
		# 	continue
		# if idx>target:
		# 	break
		# print(f"Checking {idx+1}/{len(inp)}")
		springs,gcnt_broken=row.split(" ")

		# folded result: 7163
		# UNFOLD
		folded=True
		folded=False
		if not folded:
			springs="?".join([springs]*5)
			gcnt_broken=",".join([gcnt_broken]*5)

		# CONVERT TO NUMERIC
		gcnt_broken=np.array([int(x) for x in gcnt_broken.split(",")])
		springs=springs.replace("#",str(BROKEN)).replace("?",str(UNKNOWN)).replace(".",str(FUNCTIONAL))
		springs=np.array([int(x) for x in springs],dtype=int)

		# GET POSSIBLE SPACES
		# print(gcnt_broken,springs)
		idx_posps=np.nonzero(springs<FUNCTIONAL)[0]
		# print(idx_posps)
		idx_posps_from_gcnt={}
		spring_count=springs.shape[0]
		for gcnt in np.unique(gcnt_broken):
			# print(gcnt)
			idx_posps_from_gcnt[gcnt]=[]
			# grp=np.zeros((gcnt),dtype=int)# +BROKEN #(==0)
			for idx_posp in idx_posps:
				if idx_posp>(spring_count-gcnt):
					break
				not_intersect_func=np.all(springs[idx_posp:idx_posp+gcnt]<FUNCTIONAL)
				not_touch_brok_start=idx_posp==0 or springs[idx_posp-1]>BROKEN
				not_touch_brok_end=idx_posp==spring_count-gcnt or springs[idx_posp+gcnt]>BROKEN
				is_posp=not_intersect_func and not_touch_brok_start and not_touch_brok_end
				# print(f"{gcnt=},{idx_posp=},{not_intersect_func=},{not_touch_brok_start=},{not_touch_brok_end=}")
				# print(is_posp)
				if is_posp:
					idx_posps_from_gcnt[gcnt].append(idx_posp)
			idx_posps_from_gcnt[gcnt]=np.array(idx_posps_from_gcnt[gcnt])



# [0 0 0 2 2 2 0 0 0 2 0 2 0 0 0 0 0 0 0]
# [0 0 0 2 2 0 0 0 2 2 0 2 0 0 0 0 0 0 0]

		# print(springs,gcnt_broken)
		# if PRINT:
			# print(idx_posps_from_gcnt)
		# print("INSIDE REC")
		sub_res=get_possibilities(
			0,
			gcnt_broken,
			0,
			gcnt_broken.shape[0]-1,
			0,
			springs.shape[0]-1,
			idx_posps_from_gcnt,
			springs)
		# if sub_res!=PREV_RESULTS[idx]:
			# print(f"WRONG @{idx}. IS: {sub_res}, SHOULD BE: {PREV_RESULTS[idx]}")
			# if PREV_RESULTS[idx]<6:
			# return
		print(f"################### {idx+1}/{len(inp)}:  {sub_res}")
		result+=sub_res

	t1=time.process_time()
	print(f"ELLAPSED: {(t1-t0)*1000}ms")


	print(f"RESULT: {result}")
		# print(f" xx {idx_posp}")

 #  1
 #  4
 #  1
 #  1
 #  4
 # 10

PRINT=True
PRINT=False



# lo and hi are inclusive



# lo and hi are inclusive
def get_possibilities(
		depth,
		gcnt_broken,
		gcnt_idx_lo,
		gcnt_idx_hi,
		posp_idx_lo,
		posp_idx_hi,
		idx_posps_from_gcnt,
		springs):
	# if PRINT:
		# print(f"{('-'*depth).ljust(5)}RECURSE {marked_range(springs,posp_idx_lo,posp_idx_hi)} {marked_range(gcnt_broken,gcnt_idx_lo,gcnt_idx_hi)}")
	if gcnt_idx_lo==gcnt_idx_hi:
		gcnt=gcnt_broken[gcnt_idx_lo]
		idx_posps=idx_posps_from_gcnt[gcnt]
		over_lo=idx_posps>=posp_idx_lo
		under_hi=idx_posps<=posp_idx_hi-(gcnt-1)
		filter_remaining_posps=np.logical_and(over_lo,under_hi)

		idx_broken_springs=np.nonzero(springs==BROKEN)[0]
		idx_broken_springs=idx_broken_springs[idx_broken_springs>=posp_idx_lo]
		idx_broken_springs=idx_broken_springs[idx_broken_springs<=posp_idx_hi]

		cnt=np.nonzero(filter_remaining_posps)[0].shape[0]

		if cnt>0 and idx_broken_springs.shape[0]>0:
			idx_remaining_posps=idx_posps[filter_remaining_posps]
			cnt=np.nonzero(np.logical_and(
				idx_remaining_posps<=idx_broken_springs[0],
				idx_remaining_posps+gcnt-1>=idx_broken_springs[-1]
			))[0].shape[0]
			# cnt=0
			# for idx_remaining_posps in idx_posps[filter_remaining_posps]:
				# if idx_remaining_posps<=idx_broken_springs[0] and idx_remaining_posps+gcnt-1>=idx_broken_springs[-1]:
					# cnt+=1
		return cnt


	gcnt_idx_center=(gcnt_idx_hi+gcnt_idx_lo)//2
	gcnt=gcnt_broken[gcnt_idx_center]
	idx_posps=idx_posps_from_gcnt[gcnt]
	possibilities=0
	for idx_posp in idx_posps:
		if posp_idx_lo<=idx_posp<=posp_idx_hi-1-gcnt:
			# if PRINT:
				# print(f"{('-'*depth).ljust(5)}LOOP    {marked_range(springs,idx_posp)} {marked_range(gcnt_broken,gcnt_idx_center)}")
			poss_lo=1
			poss_hi=1
			if gcnt_idx_center>gcnt_idx_lo:
				# recurse
				poss_lo=get_possibilities(
					depth+1,
					gcnt_broken,
					gcnt_idx_lo,
					gcnt_idx_center-1,
					posp_idx_lo,
					# remember groups shall not touch!
					idx_posp-2,
					idx_posps_from_gcnt,
					springs)
			else:
				# make sure there are no broken springs to the left
				if np.nonzero(springs[posp_idx_lo:idx_posp]==BROKEN)[0].shape[0]>0:
					poss_lo=0

			if poss_lo>0 and gcnt_idx_center<gcnt_idx_hi:
				# recurse
				poss_hi=get_possibilities(
					depth+1,
					gcnt_broken,
					gcnt_idx_center+1,
					gcnt_idx_hi,
					# remember groups shall not touch!
					idx_posp+gcnt+1,
					posp_idx_hi,
					idx_posps_from_gcnt,
					springs)
			else:
				# make sure there are no broken springs to the left
				if np.nonzero(springs[idx_posp+gcnt-1:posp_idx_lo]==BROKEN)[0].shape[0]>0:
					poss_hi=0

			# if PRINT:
				# print(f"{('-'*depth).ljust(5)} R: {poss_lo}*{poss_hi}={poss_lo*poss_hi}")
			possibilities+=(poss_lo*poss_hi)
	return possibilities


def get_possibilities_nonrec(
		depth,
		gcnt_broken,
		gcnt_idx_lo,
		gcnt_idx_hi,
		posp_idx_lo,
		posp_idx_hi,
		idx_posps_from_gcnt,
		springs):
	# if PRINT:
		# print(f"{('-'*depth).ljust(5)}RECURSE {marked_range(springs,posp_idx_lo,posp_idx_hi)} {marked_range(gcnt_broken,gcnt_idx_lo,gcnt_idx_hi)}")
	# if gcnt_idx_lo
	if gcnt_idx_lo==gcnt_idx_hi:
		gcnt=gcnt_broken[gcnt_idx_lo]
		idx_posps=idx_posps_from_gcnt[gcnt]
		over_lo=idx_posps>=posp_idx_lo
		under_hi=idx_posps<=posp_idx_hi-(gcnt-1)
		filter_remaining_posps=np.logical_and(over_lo,under_hi)
		# springs_on_spaces=springs[filter_remaining_posps[posps]]
		# broken_spring_count=np.nonzero(springs_on_spaces==BROKEN)[0].shape[0]


		idx_broken_springs=np.nonzero(springs==BROKEN)[0]
		idx_broken_springs=idx_broken_springs[idx_broken_springs>=posp_idx_lo]
		idx_broken_springs=idx_broken_springs[idx_broken_springs<=posp_idx_hi]

		# print(f"{('-'*depth).ljust(5)}  F: BSRPINGS {idx_broken_springs}")
		# if False:
			# pass
		cnt=np.nonzero(filter_remaining_posps)[0].shape[0]

		if cnt>0 and idx_broken_springs.shape[0]>0:
			cnt=0

			for idx_remaining_posps in idx_posps[filter_remaining_posps]:
				if idx_remaining_posps<=idx_broken_springs[0] and idx_remaining_posps+gcnt-1>=idx_broken_springs[-1]:
					cnt+=1

			# cnt=0
			# cover_idx=np.searchsorted(idx_remaining_posps,idx_broken_springs[0],side="right")-1
			# info=f"{idx_remaining_posps} {gcnt} {idx_broken_springs} {cover_idx}"
			# if GROUP can cover all BROKEN:
			# if idx_remaining_posps[cover_idx]+gcnt-1>=idx_broken_springs[-1]:
				# if PRINT:
					# print(f"{('-'*depth).ljust(5)}  SUCC/COVER: {info}")
				# cnt=1
			# else:
				# if PRINT:
					# print(f"{('-'*depth).ljust(5)}  FAIL/NOCOV: {info}")
				# cnt=0
		# else:
		# if PRINT:
			# print(f"{('-'*depth).ljust(5)}  COUNT: {cnt}")

		return cnt
	gcnt_idx_center=(gcnt_idx_hi+gcnt_idx_lo)//2
	gcnt=gcnt_broken[gcnt_idx_center]
	idx_posps=idx_posps_from_gcnt[gcnt]
	possibilities=0
	for idx_posp in idx_posps:
		if posp_idx_lo<=idx_posp<=posp_idx_hi-1-gcnt:
			# if PRINT:
				# print(f"{('-'*depth).ljust(5)}LOOP    {marked_range(springs,idx_posp)} {marked_range(gcnt_broken,gcnt_idx_center)}")
			poss_lo=1
			poss_hi=1
			if gcnt_idx_center>gcnt_idx_lo:
				# recurse
				poss_lo=get_possibilities(
					depth+1,
					gcnt_broken,
					gcnt_idx_lo,
					gcnt_idx_center-1,
					posp_idx_lo,
					# remember groups shall not touch!
					idx_posp-2,
					idx_posps_from_gcnt,
					springs)
			else:
				# make sure there are no broken springs to the left
				if np.nonzero(springs[posp_idx_lo:idx_posp]==BROKEN)[0].shape[0]>0:
					poss_lo=0

			if poss_lo>0 and gcnt_idx_center<gcnt_idx_hi:
				# recurse
				poss_hi=get_possibilities(
					depth+1,
					gcnt_broken,
					gcnt_idx_center+1,
					gcnt_idx_hi,
					# remember groups shall not touch!
					idx_posp+gcnt+1,
					posp_idx_hi,
					idx_posps_from_gcnt,
					springs)
			else:
				# make sure there are no broken springs to the left
				if np.nonzero(springs[idx_posp+gcnt-1:posp_idx_lo]==BROKEN)[0].shape[0]>0:
					poss_hi=0

			# if PRINT:
				# print(f"{('-'*depth).ljust(5)} R: {poss_lo}*{poss_hi}={poss_lo*poss_hi}")
			possibilities+=(poss_lo*poss_hi)
	return possibilities


# def marked_arr(arr,tidx):
	# return "["+(" ".join([("(" if idx==tidx else "")+str(i)+(")" if idx==tidx else "") for idx,i in enumerate(arr)]))+"]"

def marked_range(arr,lo,hi=None):
	l="{"
	r="}"
	if hi is None:
		l="<"
		r=">"
		hi=lo
	lst=[]
	for idx,elem in enumerate(arr):
		if idx==lo:
			lst.append(l)
		lst.append(str(elem))

		if idx==hi:
			lst.append(r)
	j=" "+(" ".join(lst))+" "
	j=j.replace(f" {l} ",l).replace(f" {r} ",r)
	return f"[{j}]"






































PREV_RESULTS=[3,6,2,9,34,3,1,5,29,8,2,2,1,6,3,2,1,3,7,7,6,3,13,6,4,2,4,7,15,4,2,2,6,20,4,2,3,6,4,20,5,5,7,2,10,3,3,10,3,1,4,3,4,6,9,1,7,1,2,5,3,2,2,18,2,6,8,2,7,13,3,2,3,2,2,6,3,12,7,14,15,2,2,1,2,2,5,4,7,2,5,6,9,1,141,2,2,3,1,1,3,2,4,6,4,2,9,1,1,4,55,1,10,6,2,9,2,12,2,2,12,15,3,3,6,12,2,2,4,75,10,21,6,1,33,1,4,3,2,1,1,23,10,6,4,6,2,4,7,12,21,36,4,3,17,7,2,3,2,1,1,2,4,2,49,9,16,1,2,10,10,6,4,3,13,2,20,1,2,2,1,2,3,2,10,11,11,4,2,10,2,1,1,7,1,4,2,1,4,9,5,2,26,4,5,4,3,2,5,2,5,4,5,2,2,25,2,21,5,4,1,2,2,26,17,24,7,10,2,22,3,1,3,12,3,1,22,13,1,2,2,5,2,2,13,1,9,6,1,8,10,5,6,15,12,41,4,8,4,3,9,14,16,3,1,39,11,10,1,5,19,2,2,3,16,4,1,3,8,2,5,4,2,4,1,1,3,48,2,1,2,9,9,3,56,8,5,7,4,4,4,2,3,11,4,4,6,1,2,4,3,1,1,6,3,9,1,5,23,8,3,4,43,5,3,1,1,2,1,3,2,6,6,18,13,6,5,6,2,11,10,4,21,2,8,2,3,1,1,2,10,2,25,4,1,1,2,4,1,3,2,7,18,2,2,4,21,1,8,2,1,1,2,5,6,6,28,3,6,37,6,35,1,3,4,4,2,2,3,1,13,3,3,3,4,3,3,4,2,2,3,40,4,3,2,1,2,4,6,3,50,15,2,3,6,2,3,1,5,5,5,10,6,3,1,1,36,2,1,7,2,6,3,4,3,4,3,5,3,11,6,9,2,10,6,6,1,1,8,7,2,2,2,2,3,9,4,4,2,4,20,3,3,2,6,2,2,7,9,26,18,4,9,8,6,6,4,7,3,5,1,3,2,2,6,6,1,4,5,1,19,3,30,15,4,6,1,8,7,2,1,2,17,14,4,11,8,2,3,1,6,1,7,8,1,8,12,43,9,1,1,1,2,3,5,3,6,4,3,3,3,4,3,2,3,4,6,1,29,2,13,47,1,1,1,5,6,2,2,3,2,3,7,19,6,2,3,5,5,2,2,2,2,158,10,10,24,1,10,3,1,3,4,3,31,24,4,4,3,40,5,5,9,2,4,6,34,3,18,2,2,1,3,10,3,5,1,4,7,4,1,10,12,35,6,8,2,18,2,2,2,3,10,1,32,5,1,2,3,4,96,1,3,6,10,2,7,10,3,6,6,3,10,5,21,2,20,7,3,14,2,6,18,7,6,2,2,4,4,15,3,22,3,4,2,2,3,6,3,2,2,4,55,13,12,18,13,2,1,14,4,2,5,8,3,8,4,3,13,2,3,3,3,1,4,16,5,9,11,6,15,1,5,4,6,2,2,2,8,4,10,2,17,14,4,2,6,1,6,3,1,4,3,3,10,12,14,3,24,18,6,3,4,6,2,2,25,2,2,1,7,6,9,1,12,2,2,13,3,4,6,4,4,3,4,2,6,1,9,2,2,4,3,3,4,1,4,6,35,6,6,3,4,6,2,1,27,1,3,35,3,1,1,7,45,14,2,1,6,8,1,1,3,3,4,20,10,3,6,4,13,2,2,2,27,4,2,4,2,1,5,10,1,9,1,6,4,1,2,19,18,4,3,3,40,2,2,2,2,3,4,2,7,4,20,1,5,1,6,3,3,7,7,2,41,9,6,10,4,4,1,2,1,2,37,37,48,7,10,14,6,6,26,6,4,4,20,2,2,4,4,7,1,6,30,10,1,4,35,4,6,3,29,3,2,3,2,14,3,13,6,1,3,3,1,4,6,10,3,3,1,6,6,1,3,5,4,1,1,18,5,5,1,9,11,4,3,3,3,3,11,1,1,1,11,5,6,1,2,2,3,4,1,2,2,4,6,3,1,28,3,3,2,2,2,4,2,3,1,1,2,6,2,6,1,3,1,2,2,2,2,2,8,1,3,21,3,1,12,2,5,43,15,5,2,3,20,12,18,7,2,2,4,2,4,1,4,10,2,2,2,3,6,1,3,6,10,23,10,8,4,1,4,1,18,6,5,3,2,2]

# def legacy():
# 	while True:
# 		# print("xx1")
# 		# return
# 		# print(springs)
# 		# cnt=(2**(np.nonzero(springs==UNKNOWN)[0].shape[0]))//10
# 		# # print("xx2")
# 		# print(cnt)
# 		# perc=1
# 		# for i in range(cnt):
# 		# 	x=int((100*i/cnt))
# 		# 	if x>perc:
# 		# 		print(perc)
# 		# 		perc+=1
# 		# 	# if x%10==0:
# 		# 	# print(x)
# 		# 	# print(x%10)
# 		# 	# do_work(i)

# 		# continue


# 		# missing=springs.shape[0]-sum(grps)

# 		inserts=np.nonzero(springs==1)[0]
# 		# insert_idx=0
# 		# insert_count=inserts.shape[0]
# 		# sub_res=0
# 		# print(inserts)
# 		test=springs.copy()
# 		sub_res=check(test,springs,grps,inserts,0)
# 		# while insert_idx<len(inserts):
# 		# 	# for state in [BROKEN,FUNCTIONAL]:
# 		# 	test[inserts[insert_idx]]=BROKEN
# 		# 	if is_correct(test,springs):
# 		# 		if insert_idx==insert_count-1:
# 		# 			sub_res+=1
# 		# 		else:
# 		# 			insert_idx+=1


# 		# print(test)


# 		print(f"################### {idx+1}/{len(inp)}:  {sub_res}")
# 		result+=sub_res
# 		# break
# 		# return
# 	print()
# 	print(result)

# def grps_from_arr(arr):
# 	x=np.nonzero(arr[1:]-arr[:-1])[0]+1
# 	x=np.hstack((0,x,len(arr)))
# 	return x[1:]-x[:-1]

# def check(test,springs,grps,inserts,insert_idx,_correct_type=UNKNOWN):
# 	# print("-"*insert_idx+f" {insert_idx}")
# 	if insert_idx>=len(inserts):
# 		# print("RESULT: "+("SUCC" if _correct_type==EQUAL else "FAIL"))
# 		return 1 if _correct_type==EQUAL else 0

# 	corrects=0

# 	for state in [BROKEN,FUNCTIONAL]:
# 		test[inserts[insert_idx]]=state
# 		correct_type=is_correct(test,springs,grps)
# 		if correct_type>WRONG:
# 			corrects+=check(test,springs,grps,inserts,insert_idx+1,correct_type)

# 	test[inserts[insert_idx]]=UNKNOWN

# 	return corrects

# def is_sub(a,b):
# 	ib=0
# 	for aa in a:
# 		if ib>=b.shape[0]:
# 			return False
# 		while b[ib]<aa:
# 			ib+=1
# 			if ib>=b.shape[0]:
# 				return False
# 		ib+=1
# 	return True

# EQUAL=2
# SUB=1
# WRONG=0

# def is_correct(test,springs,grps):
# # def is_correct(test,springs):
# 	gtest=test.copy()
# 	gtest[gtest>BROKEN]=FUNCTIONAL
# 	tgrps=grps_from_arr(gtest)

# 	if gtest[0]==BROKEN:
# 		tgrps=tgrps[::2]
# 	else:
# 		tgrps=tgrps[1::2]

# 	if is_sub(tgrps,grps):
# 		if tgrps.shape==grps.shape and np.all(tgrps==grps):
# 			# print(f"EQU: {str(test)} {str(springs)} {str(grps)} {str(tgrps)}")
# 			return EQUAL
# 		else:
# 			# print(f"SUB: {str(test)} {str(springs)} {str(grps)} {str(tgrps)}")
# 			return SUB
# 	else:
# 		# print(f"WRO: {str(test)} {str(springs)} {str(grps)} {str(tgrps)}")
# 		# return WRONG
# 		errs=np.abs(test-springs)
# 		is_correct=not np.any(errs>1)
# 		return SUB if is_correct else WRONG
# 	# else:
# 		# print(f" {str(tgrps)} is sub of {str(tgrps)} {str(grps)}")



# 	# print(gtest)
# 	# print(tgrps)
# 	# print(grps)
# 	# print(is_sub(tgrps,grps))
# 	# # print(tgrps)
# 	# print(bgrps.shape==grps.shape)
# 	# # print(f"{bgrps=},{grps=}")
# 	# if bgrps.shape==grps.shape and np.all(bgrps==grps):
# 	# 	# print(f"{test} is valid!!!")
# 	# 	return 1
# 	# else:
# 	# 	# print(f"{test} is not valid...")
# 	# 	return 0


# 	# check grps:
# 	# 211100

# 	# print(test)
# 	# print(springs)
# 	# print(is_correct)
# 	# return is_correct

# # def b_grps_from_arr(arr):
# # 	0002022002220
# # 	00
# # 	=
# # 	3112231

main()