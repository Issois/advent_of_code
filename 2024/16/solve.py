
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(field,pos_start,pos_end):

	graph=make_graph(field)

	answer=0
	return answer

def solve_2(field,pos_start,pos_end):
	answer=0
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")
	inp=np.array([list(row) for row in inp])
	field=np.zeros(inp.shape,dtype=bool)
	field[inp!="#"]=True
	pos_start=np.array(np.nonzero(inp=="S"))[:,0]
	pos_end=np.array(np.nonzero(inp=="E"))[:,0]
	# print(pos_start)
	return field,pos_start,pos_end

def get_free_dires(field,pos):
	free_dires=[]
	for dire in range(0,8,2):
		if field[tuple(pos+DIREV[dire])]:
			free_dires.append(dire)
	return free_dires

def make_graph(field,add_poss):
	pos_start=add_poss[0]
	node_start=(tuple(pos_start),2)
	add_postups=set([tuple(pos) for pos in add_poss])
	graph={}
	nodes_checked=set()
	nodes_to_check=[node_start]
	while len(nodes_to_check)>0:
		node_to_check=nodes_to_check.pop()
		# node_to_check_postup,node_to_check_dire=node_to_check
		# find next node in current direction.
		cost=1
		pos_path=np.array(node_to_check[POSTUP])+DIREV[node_to_check[DIRE]]
		search_finshed=False
		while not search_finshed:

		# - walk to next tile
		# - if in add nodes: make new node
		# - count neigbours
		# - if 1: discard path
		# - elif 2: update direction
		# - else: make new node





	pass

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

POSTUP=0
DIRE=1

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
