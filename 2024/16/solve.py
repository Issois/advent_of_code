
import numpy as np
import sys
# import matplotlib.pyplot as plt

from pprint import pprint


def solve_1(field,pos__start,pos__end):

	graph=make_graph(field,[pos__start,pos__end])

	pprint(graph)

	answer=0
	return answer

def solve_2(field,pos__start,pos__end):
	answer=0
	return answer

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n")
	inp=np.array([list(row) for row in inp])
	field=np.zeros(inp.shape,dtype=bool)
	field[inp!="#"]=True
	pos__start=np.array(np.nonzero(inp=="S"))[:,0]
	pos__end=np.array(np.nonzero(inp=="E"))[:,0]
	# print(pos__start)
	return field,pos__start,pos__end

def get_free_dires(field,pos):
	free_dires=[]
	for dire in range(0,8,2):
		if field[tuple(pos+DIREV[dire])]:
			free_dires.append(dire)
	return free_dires

def make_graph(field,add_poss):
	pos__start=add_poss[0]
	node_start=tuple(pos__start),2
	add_postups=set([tuple(pos) for pos in add_poss])
	graph={}
	nodes__checked=set()
	nodes__to_check=[node_start]

	ncid=0

	while len(nodes__to_check)>0:
		# print(f"---  {nodes__to_check=}\n")
		# print(f"---  {len(nodes__to_check)=}\n")
		ncid+=1
		node__source=nodes__to_check.pop()

		if node__source in nodes__checked:
			# print(f"<{ncid:3.0f}|{node__source}> Node duplicate check.")
			continue

		if node__source not in graph:
			graph[node__source]=[]

		searched_dires={node[DIRE] for node,_ in graph[node__source]}

		# print(f"<{ncid:3.0f}|{node__source}> {searched_dires=}")

		if node__source[DIRE] not in searched_dires:
			# find next node in current direction.
			cost__path=1
			pos__path=np.array(node__source[POSTUP])+DIREV[node__source[DIRE]]
			dire__path=node__source[DIRE]
			search_finshed=False
			if not field[tuple(pos__path)]:
				search_finshed=True
			# - walk to next tile
			while not search_finshed:
			# - if in add nodes: make new node
				if tuple(pos__path) in add_postups:
					node__target=tuple(pos__path),dire__path
					add_node(graph,node__source,node__target,cost__path,nodes__to_check)
					search_finshed=True
					# print(f"<{ncid:3.0f}|{node__source}> SEARCH: special node: {node__target}")
				else:
			# - count neigbours
					free_dires=get_free_dires(field,pos__path)
					free_dires_count=len(free_dires)
			# - if 1: discard path
					if free_dires_count==1:
						# print(f"<{ncid:3.0f}|{node__source}> SEARCH: discard @ {pos__path}")
						search_finshed=True
			# - elif 2: update direction
					elif free_dires_count==2:
						# print(f"<{ncid:3.0f}|{node__source}> SEARCH: move @ {pos__path}, dire: {dire__path} [{free_dires}]")
						free_dires=set(free_dires)
						free_dires.remove((dire__path+4)%8)
						dire__path_new=free_dires.pop()
						if dire__path_new==dire__path:
							cost__path+=1
							pos__path=pos__path+DIREV[dire__path]
						else:
							cost__path+=1001
							dire__path=dire__path_new
							pos__path=pos__path+DIREV[dire__path]
			# - else: make new node
					else:
						node__target=tuple(pos__path),dire__path
						# print(f"<{ncid:3.0f}|{node__source}> SEARCH: new node (trg)     : {node__target}")
						add_node(graph,node__source,node__target,cost__path,nodes__to_check)
						search_finshed=True

		for dire_offset in [2,6]:
			dire__search=(node__source[DIRE]+dire_offset)%8
			if dire__search not in searched_dires and field[tuple(np.array(node__source[POSTUP])+DIREV[dire__search])]:
				node__target=node__source[POSTUP],dire__search
				graph[node__source].append((node__target,1000))
				if node__target not in graph:
					graph[node__target]=[]
				graph[node__target].append((node__source,1000))
				nodes__to_check.append(node__target)
				# print(f"<{ncid:3.0f}|{node__source}> TURN: new node: {node__target}")

		nodes__checked.add(node__source)
		# print(f"<{ncid:3.0f}|{node__source}> CHECKED!\n")

	return graph





def add_node(graph,node__source,node__target,cost__path,nodes__to_check):
	graph[node__source].append((node__target,cost__path))
	node__source_reverse=node__source[POSTUP],(node__source[DIRE]+4)%8
	node__target_reverse=node__target[POSTUP],(node__target[DIRE]+4)%8
	if node__target_reverse not in graph:
		graph[node__target_reverse]=[]
	# print(f"<   |{node__source}> SEARCH: new node (trg rev) : {node__target_reverse}")
	# print(f"<   |{node__source}> SEARCH: new node (src rev) : {node__source_reverse}")
	graph[node__target_reverse].append((node__source_reverse,cost__path))
	nodes__to_check.extend([
		node__target,
		node__source_reverse,
		node__target_reverse
	])


def main():
	inp=get_input(FILE_PATH)
	answer=solve(*inp)
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

NODE=0
COST=1

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
