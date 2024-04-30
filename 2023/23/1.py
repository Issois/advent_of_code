
import numpy as np
import sys
import matplotlib.pyplot as plt
import pprint

FOREST=0
PATH=1
NO=2
EA=3
SO=4
WE=5

TO=0
FROM=1

DIRE={
	NO:np.array([-1, 0]),
	EA:np.array([ 0, 1]),
	SO:np.array([ 1, 0]),
	WE:np.array([ 0,-1]),
}

DNAME={
	NO:"NO",
	EA:"EA",
	SO:"SO",
	WE:"WE",
	PATH:"..",
}

OPPO={
	EA:WE,
	WE:EA,
	NO:SO,
	SO:NO,
}

FORW=1
BAKW=-1
ANYW=0


def main():
	with open(sys.argv[1]) as f:
		inp=f.read().split("\n")

	arr=np.array([list(line) for line in inp])

	arrx=np.zeros(arr.shape,dtype=int)

	arrx[arr=="."]=PATH
	arrx[arr=="^"]=NO
	arrx[arr==">"]=EA
	arrx[arr=="v"]=SO
	arrx[arr=="<"]=WE

	arr=arrx
	not_visited=np.ones(arr.shape,dtype=bool)


	pos_start=np.array((0,np.nonzero(arr[0])[0][0]))
	pos_end=np.array((arr.shape[0]-1,np.nonzero(arr[-1])[0][0]))

	not_visited[tuple(pos_start)]=False

	pel_start=PathElement(pos_start)
	pel_from_tpos={tuple(pos_start):pel_start}

	pels_to_check=[pel_start]
	while len(pels_to_check)>0:
		pel_to_check=pels_to_check.pop(0)
		for dire,dire_vec in DIRE.items():
			pos_next=pel_to_check.pos+dire_vec
			tpos_next=tuple(pos_next)
			if is_in_bounds(pos_next,arr) and arr[tpos_next]>FOREST:
				if not_visited[tpos_next]:
					pel_neighbor=PathElement(pos_next)
					pel_from_tpos[tpos_next]=pel_neighbor
					not_visited[tpos_next]=False
					pels_to_check.append(pel_neighbor)
				else:
					pel_neighbor=pel_from_tpos[tpos_next]

				assert np.linalg.norm(pel_to_check.pos-pel_neighbor.pos)==1, f"Non neighbors declared as neigbors: old {pel_to_check.pos+1} new {pel_neighbor.pos+1} posnext {pos_next+1}"

				pel_to_check.neighbors[dire] =pel_neighbor
				pel_neighbor.neighbors[OPPO[dire]]=pel_to_check

	test=np.zeros(arr.shape,dtype=int)

	pel_end=pel_from_tpos[tuple(pos_end)]

	pel_from_pid={pel.id:pel for pel in pel_from_tpos.values()}

	graph={
		pel_start.id:[],
		pel_end.id:[],
	}

	for pel in pel_from_tpos.values():
		if len(pel.neighbors)>2:
			graph[pel.id]=[]


	npelids_to_check=[pel_start.id]
	pelids_checked=set(npelids_to_check)

	while len(npelids_to_check)>0:
		npelid_current=npelids_to_check.pop(0)
		npel_current=pel_from_pid[npelid_current]

		for dire_nstart,npel_current_neighbor in npel_current.neighbors.items():
			# print(f"Starting from node at {npel_current.pos+1} in direction {DNAME[dire_nstart]}.")
			if npel_current_neighbor.id not in pelids_checked:
				edge_new=GraphEdge()
				edge_new.distance=1

				dire_current=dire_nstart

				pel_current=npel_current_neighbor
				while pel_current.id not in graph:
					# print(f"In direction {DNAME[dire_current]} to pos {pel_current.pos+1}.")
					edge_new.distance+=1

					pelids_checked.add(pel_current.id)

					assert len(pel_current.neighbors)==2,"Not exactly two neighbors!"

					pel_neighbor_next,dire_next=[(neigh,dire_neigh) for dire_neigh,neigh in pel_current.neighbors.items() if dire_neigh!=OPPO[dire_current]][0]

					path_current=arr[tuple(pel_current.pos)]
					if path_current==dire_next:
						# This is a slope in walking direction.
						if edge_new.direction==ANYW:
							edge_new.direction=FORW
						assert edge_new.direction!=BAKW,f"pos: {pel_current.pos+1}, path: {DNAME[path_current]}, dire: {DNAME[dire_current]}  Edge contains backward and then forward. {pel_from_pid[npelid_current].pos+1} to {DNAME[dire_nstart]}"
					elif path_current==OPPO[dire_current]:
						# This is a slope against walking direction.
						if edge_new.direction==ANYW:
							edge_new.direction=BAKW
						assert edge_new.direction!=FORW,f"pos: {pel_current.pos+1}, path: {DNAME[path_current]}, dire: {DNAME[dire_current]}  Edge contains forward and then backward. {pel_from_pid[npelid_current].pos+1} to {DNAME[dire_nstart]}"
					dire_current=dire_next
					pel_current=pel_neighbor_next

				edge_new.pelid_target=pel_current.id
				edge_reverse=GraphEdge()
				edge_reverse.pelid_target=npelid_current
				edge_reverse.distance=edge_new.distance
				edge_reverse.direction=-edge_new.direction

				# Add edges to both nodes.
				graph[npelid_current].append(edge_new)
				graph[edge_new.pelid_target].append(edge_reverse)
				# Add target node to check if not already.
				if edge_new.pelid_target not in pelids_checked:
					pelids_checked.add(edge_new.pelid_target)
					npelids_to_check.append(edge_new.pelid_target)


	graph_mono={
		npelid:[
			edge for edge in edges if edge.direction>=0
		] for npelid,edges in graph.items()
	}


	pprint.pprint(graph_mono)
	print(f"start: {pel_start}, end: {pel_end}.")


	def rec_search(head,tail,distance):
		available_edges=[edge for edge in graph_mono[head] if edge.pelid_target not in tail]
		if len(available_edges)==0:
			# No more path left.
			if head==pel_end.id:
				print(head,tail,distance)
				return distance
		else:
			dists=[]
			for edge in available_edges:
				tail.append(head)
				dists.append(rec_search(edge.pelid_target,tail,distance+edge.distance))
				tail.pop(-1)
			return max(dists)

	answer=rec_search(pel_start.id,[],0)

	print(f"ANSWER: {answer}")
	# 2114 is correct!





class GraphEdge:
	def __init__(self):
		self.pelid_target=None
		self.distance=0
		self.direction=ANYW
	def __str__(self):
		return f"To pel {self.pelid_target} {self.distance}m {self.direction}"
	def __repr__(self):
		return str(self)


class PathElement:
	NEXT_ID=0
	def __init__(self,pos):
		self.id=PathElement.NEXT_ID
		PathElement.NEXT_ID+=1
		self.pos=pos
		self.neighbors={}
	def __str__(self):
		return f"pel{self.id}@{self.pos}"
	def __repr__(self):
		return str(self)



def is_in_bounds(pos,arr):
	return 0<=pos[0]<arr.shape[0] and 0<=pos[1]<arr.shape[1]


main()
