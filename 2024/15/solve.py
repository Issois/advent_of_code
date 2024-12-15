
import numpy as np
import sys
import matplotlib.pyplot as plt


def solve_1(inp):
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
	field,start_pos,cmds=inp
	answer=0
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n\n")
	imap=np.array([list(row) for row in inp[0].split("\n")])
	# print(field)
	field=np.zeros(imap.shape,dtype=int)
	field[imap=="#"]=WAL
	field[imap=="O"]=BOX
	start_pos=np.array(np.nonzero(imap=="@"))
	start_pos=np.array([start_pos[X][0],start_pos[Y][0]])
	conv={"<":6,">":2,"v":4,"^":0}
	cmds=[conv[elem] for elem in inp[1] if elem in conv]
	return field,start_pos,cmds


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
