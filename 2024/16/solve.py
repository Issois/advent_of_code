
import numpy as np
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from pprint import pprint


COST_STEP=1
COST_TURN=1000

# CONDITION: Works only for COST_TURN>>COST_STEP such that for any path between two nodes: step_count=cost%COST_TURN.
def solve_2(field,pos__start,pos__end):


	graph=make_graph(field,[pos__start,pos__end])

	node__start=tuple(pos__start),2
	postup__end=tuple(pos__end)


	heads=[(node__start,0,"0")]
	analyzed=set([node__start])
	min_cost_at_node={node__start:0}
	path_from_head={heads[0]:[heads[0]]}
	# alternate_path_heads={}
	min_cost=None

	next_head_id=1

	animate=True
	animate=False
	if animate:
		fig,ax=plt.subplots()
		artists=[]

	end_found=False
	while len(heads)>0:
	# while not end_found:
		# print("     ",heads[-3:])

		head__cur=heads.pop()

		if animate:
			img=field.astype(int)
			for node in analyzed:
				img[node[POSTUP]]=2
			img[head__cur[NODE][POSTUP]]=3
			artists.append([plt.imshow(img,animated=True)])

		if head__cur[NODE][POSTUP]==postup__end:
			if min_cost is None:
				min_cost=head__cur[COST]
		else:
			for edge__next in graph[head__cur[NODE]].values():
				node__next=edge__next[NODE]
				cost__next=head__cur[COST]+edge__next[COST]
				head__next=node__next,cost__next,str(next_head_id)
				next_head_id+=1
				if node__next not in analyzed or cost__next<=min_cost_at_node[node__next]:
					analyzed.add(node__next)
					min_cost_at_node[node__next]=cost__next
					path_from_head[head__next]=path_from_head[head__cur]+[head__next]
					insert_sorted(heads,head__next)

	if animate:
		ani=animation.ArtistAnimation(fig=fig,artists=artists,interval=60,blit=True)
		plt.show()

	edges__counted=set()
	postups__visited=set([postup__end])

	answer=0

	print(f"{min_cost=}")
	for head__end,heads__path in path_from_head.items():
		if head__end[NODE][POSTUP]==tuple(pos__end) and head__end[COST]==min_cost:
			# print("shortest path: ",heads__path)

			for index__path in range(len(heads__path)-1):
				pos__a=heads__path[index__path  ][NODE][POSTUP]
				pos__b=heads__path[index__path+1][NODE][POSTUP]
				postups__visited.add(pos__a)
				postups__visited.add(pos__b)
				if pos__a!=pos__b:
					if pos__a<pos__b:
						edge=pos__a,pos__b
					else:
						edge=pos__b,pos__a
					if edge not in edges__counted:
						edges__counted.add(edge)
						# count only tiles between nodes. add nodes separately.
						answer+=(graph[heads__path[index__path][NODE]][FORWARD][COST]%COST_TURN)-1

	answer+=len(postups__visited)

	# 494 is correct.

	return answer


def solve_1(field,pos__start,pos__end):

	graph=make_graph(field,[pos__start,pos__end])

	node__start=tuple(pos__start),2
	postup__end=tuple(pos__end)

	heads=[(node__start,0)]
	analyzed=set([node__start])
	min_cost_at_node={node__start:0}

	animate=True
	if animate:
		fig,ax=plt.subplots()
		artists=[]

	end_found=False
	while not end_found:

		head__cur=heads.pop()

		if animate:
			img=field.astype(int)
			for node in analyzed:
				img[node[POSTUP]]=2
			img[head__cur[NODE][POSTUP]]=3
			artists.append([plt.imshow(img,animated=True)])

		if head__cur[NODE][POSTUP]==postup__end:
			answer=head__cur[COST]
			end_found=True
		else:
			for edge__next in graph[head__cur[NODE]].values():
				node__next=edge__next[NODE]
				cost__next=head__cur[COST]+edge__next[COST]
				if node__next not in analyzed or cost__next<min_cost_at_node[node__next]:
					analyzed.add(node__next)
					min_cost_at_node[node__next]=cost__next
					insert_sorted(heads,(node__next,cost__next))

	if animate:
		ani=animation.ArtistAnimation(fig=fig,artists=artists,interval=60,blit=True)
		plt.show()
	# 95468 is too high.
	# 91468 is too high.
	# 91464 is correct.
	return answer

def insert_sorted(prio_queue,head):
	cost=head[COST]

	start=0
	end=len(prio_queue)
	# print(start,end)
	while end-start>0:
		index__search=(start+end)//2

		if cost>prio_queue[index__search][COST]:
			end=index__search
		else:
			start=index__search+1
		# print(start,end,index__search)
	prio_queue.insert(start,head)

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
	print_building=True
	print_building=False
	ncid=0

	while len(nodes__to_check)>0:
		# print(f"---  {nodes__to_check=}\n")
		# print(f"---  {len(nodes__to_check)=}\n")
		ncid+=1
		node__source=nodes__to_check.pop()

		if node__source in nodes__checked:
			if print_building:
				print(f"<{ncid:3.0f}|{node__source}> Node duplicate check.")
			continue

		if node__source not in graph:
			graph[node__source]={}

		# searched_dires={node[DIRE] for node,_ in graph[node__source]}

		if print_building:
			print(f"<{ncid:3.0f}|{node__source}> {graph[node__source].keys()}")

		if FORWARD not in graph[node__source]:
			# find next node in current direction.
			cost__path=COST_STEP
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
					add_node(graph,node__source,node__target,cost__path,nodes__to_check,print_building)
					search_finshed=True
					if print_building:
						print(f"<{ncid:3.0f}|{node__source}> SEARCH: special node: {node__target}")
				else:
			# - count neigbours
					free_dires=get_free_dires(field,pos__path)
					free_dires_count=len(free_dires)
			# - if 1: discard path
					if free_dires_count==1:
						if print_building:
							print(f"<{ncid:3.0f}|{node__source}> SEARCH: discard @ {pos__path}")
						search_finshed=True
			# - elif 2: update direction
					elif free_dires_count==2:
						if print_building:
							print(f"<{ncid:3.0f}|{node__source}> SEARCH: move @ {pos__path}, dire: {dire__path} [{free_dires}]")
						free_dires=set(free_dires)
						free_dires.remove((dire__path+4)%8)
						dire__path_new=free_dires.pop()
						if dire__path_new==dire__path:
							cost__path+=COST_STEP
							pos__path=pos__path+DIREV[dire__path]
						else:
							cost__path+=COST_STEP+COST_TURN
							dire__path=dire__path_new
							pos__path=pos__path+DIREV[dire__path]
			# - else: make new node
					else:
						node__target=tuple(pos__path),dire__path
						if print_building:
							print(f"<{ncid:3.0f}|{node__source}> SEARCH: new node (trg)     : {node__target}")
						add_node(graph,node__source,node__target,cost__path,nodes__to_check,print_building)
						search_finshed=True

		for turn in [LEFT,RIGHT]:
			dire_offset=(turn*2)-2
			dire__search=(node__source[DIRE]+dire_offset)%8
			if turn not in graph[node__source] and field[tuple(np.array(node__source[POSTUP])+DIREV[dire__search])]:
				node__target=node__source[POSTUP],dire__search
				graph[node__source][turn]=node__target,COST_TURN
				if node__target not in graph:
					graph[node__target]={}
				graph[node__target][2-turn]=node__source,COST_TURN
				nodes__to_check.append(node__target)
				if print_building:
					print(f"<{ncid:3.0f}|{node__source}> TURN: new node: {node__target}")

		nodes__checked.add(node__source)
		if print_building:
			print(f"<{ncid:3.0f}|{node__source}> CHECKED!\n")

	return graph





def add_node(graph,node__source,node__target,cost__path,nodes__to_check,print_building):
	# if (node__target,cost__path) in graph[node__source]:
		# print("????")
	graph[node__source][FORWARD]=node__target,cost__path
	node__source_reverse=node__source[POSTUP],(node__source[DIRE]+4)%8
	node__target_reverse=node__target[POSTUP],(node__target[DIRE]+4)%8
	if node__target_reverse not in graph:
		graph[node__target_reverse]={}
	if print_building:
		print(f"<   |{node__source}> SEARCH: new node (trg rev) : {node__target_reverse}")
	if print_building:
		print(f"<   |{node__source}> SEARCH: new node (src rev) : {node__source_reverse}")
	# if (node__source_reverse,cost__path) in graph[node__target_reverse]:
		# print("????")
	graph[node__target_reverse][FORWARD]=node__source_reverse,cost__path
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

LEFT=0
FORWARD=1
RIGHT=2


POSTUP=0
DIRE=1

NODE=0
COST=1
HID=2

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
