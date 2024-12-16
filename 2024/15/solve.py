
import numpy as np
import sys
import matplotlib.pyplot as plt


def solve_1(inp):
	
	imap=np.array([list(row) for row in inp[0].split("\n")])
	# print(field)
	field=np.zeros(imap.shape,dtype=int)
	field[imap=="#"]=WAL
	field[imap=="O"]=BOX
	start_pos=np.array(np.nonzero(imap=="@"))
	start_pos=np.array([start_pos[X][0],start_pos[Y][0]])
	conv={"<":6,">":2,"v":4,"^":0}
	cmds=[conv[elem] for elem in inp[1] if elem in conv]
	inp=field,start_pos,cmds
	field,cur_pos,cmds=inp

	answer=0

	for idx,cmd in enumerate(cmds):
		nex_pos=cur_pos+DIREV[cmd]
		nex_pos_tup=tuple(nex_pos)
		elem=field[nex_pos_tup]
		if elem==NON:
			cur_pos=nex_pos
		elif elem==WAL:
			pass
		else:
			dist_no_box=1

			while field[(after_box_pos:=look_in_dire(cur_pos,cmd,dist_no_box))]==BOX:
				dist_no_box+=1
			if field[after_box_pos]==NON:
				field[after_box_pos]=BOX
				field[nex_pos_tup]=NON
				cur_pos=nex_pos


	box_positions=np.array(np.nonzero(field==BOX)).T
	for box_pos in box_positions:
		answer+=(box_pos[X]*100)+box_pos[Y]

	return answer

def look_in_dire(pos,dire,dist,field=None):
	pos_tup=tuple(pos+(dist*DIREV[dire]))
	# print(f"{pos=},{dire=},{dist=} => {pos_tup=}")
	if field is None:
		return pos_tup
	else:
		return field[pos_tup]

def solve_2(inp):
	field_str=inp[0]
	field_str=field_str.replace("#","##")
	field_str=field_str.replace("O","[]")
	field_str=field_str.replace(".","..")
	field_str=field_str.replace("@","@.")

	imap=np.array([list(row) for row in field_str.split("\n")])
	

	field=np.zeros(imap.shape,dtype=int)
	field[imap=="#"]=WAL
	field[imap=="["]=BOL
	field[imap=="]"]=BOR
	start_pos=np.array(np.nonzero(imap=="@"))
	start_pos=np.array([start_pos[X][0],start_pos[Y][0]])
	conv={"<":6,">":2,"v":4,"^":0}
	cmds=[conv[elem] for elem in inp[1] if elem in conv]
	inp=field,start_pos,cmds
	field,cur_pos,cmds=inp

	for idx,cmd in enumerate(cmds):
		nex_pos=cur_pos+DIREV[cmd]
		nex_pos_tup=tuple(nex_pos)
		elem=field[nex_pos_tup]
		if elem==NON:
			cur_pos=nex_pos
		elif elem==WAL:
			pass
		else:
			if cmd%4==2:
				# Check for wall/empty behind boxes like in 1.
				dist_no_box=3

				while field[(after_box_pos:=look_in_dire(cur_pos,cmd,dist_no_box))]>BOX:
					dist_no_box+=2
				if field[after_box_pos]==NON:
					while dist_no_box>=1:
						field[look_in_dire(cur_pos,cmd,dist_no_box)]=field[look_in_dire(cur_pos,cmd,dist_no_box-1)]
						dist_no_box-=1
						
					cur_pos=nex_pos
				pass
			else:
				# Build tree of affected boxes. If any has wall behind nothing happens. Else all get moved.
				blocked=False
				check_list=[cur_pos]
				tree={}
				while len(check_list)>0 and not blocked:
					# Check depth first.
					check_pos=check_list.pop()
					check_pos_tup=tuple(check_pos)
					tree[check_pos_tup]=[]
					check_nex_pos=check_pos+DIREV[cmd]
					check_nex_pos_tup=tuple(check_nex_pos)
					next_elem=field[check_nex_pos_tup]
					if next_elem>BOX:
						for pos in [other_box_half(field,check_nex_pos),check_nex_pos]:
							# THIS WORKS ONLY ON DEPTH FIRST!
							if tuple(pos) not in tree:
								tree[check_pos_tup].append(pos)
								check_list.append(pos)
					elif next_elem==WAL:
						blocked=True
				if not blocked:

					stack=[cur_pos]
					
					while len(stack)>0:
						tree_pos=stack[-1]
						tree_pos_tup=tuple(tree_pos)
						if len(tree[tree_pos_tup])>0:
							next_tree_pos=tree[tree_pos_tup].pop()
							stack.append(next_tree_pos)
						else:
							field[tuple(tree_pos+DIREV[cmd])]=field[tree_pos_tup]
							field[tree_pos_tup]=NON
							stack.pop()
					cur_pos=nex_pos

		# fieldx=field.copy()
		# fieldx=fieldx.astype(str)
		# fieldx[fieldx=="0"]=" "
		# fieldx[fieldx=="1"]="#"
		# fieldx[fieldx=="3"]="["
		# fieldx[fieldx=="4"]="]"
		# fieldx[tuple(cur_pos)]="@"
		# field_str="\n".join(["".join(row) for row in fieldx])
		# print(field_str)
		# print(f"[{idx}]  curr: {cur_pos}, next: {cmds[idx+1] if idx+1<len(cmds) else '...'}")
		# input()

		box_positions=np.array(np.nonzero(field==BOL)).T

	answer=0
	# print(box_positions)
	for box_position in box_positions:
		answer+=(100*box_position[X])+box_position[Y]

	# 1397393 is correct.
	return answer

def other_box_half(arr,box_pos):
	box=arr[tuple(box_pos)]
	if box==BOR:
		return box_pos+DIREV[6]
	elif box==BOL:
		return box_pos+DIREV[2]
	else:
		raise ValueError(f"Element {box} in pos {box_pos} not valid for call of other_box_half.")

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n\n")
	return inp


def main():
	inp=get_input(FILE_PATH)
	answer=solve(inp)
	print(f"ANSWER: {answer}")



def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)


RIDDLE_NUMBER=sys.argv[1]
FILE_PATH=sys.argv[2]

NON=0
WAL=1
BOX=2
BOL=3
BOR=4

X=0
Y=1
Z=2

ROW=0
COL=1

DIREV=np.array([
	[-1, 0],
	[-1, 1],
	[ 0, 1],
	[ 1, 1],
	[ 1, 0],
	[ 1,-1],
	[ 0,-1],
	[-1,-1],
])

solve=getattr(sys.modules[__name__],"solve_"+RIDDLE_NUMBER)
main()
