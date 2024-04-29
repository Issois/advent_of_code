
import numpy as np
import sys
import matplotlib.pyplot as plt

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
}

OPPO={
	EA:WE,
	WE:EA,
	NO:SO,
	SO:NO,
}


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
	# plt.imshow(arr)
	# plt.show()
	# print(arr)
	not_visited=np.ones(arr.shape,dtype=bool)


	pos_start=np.array((0,np.nonzero(arr[0])[0][0]))
	pos_end=np.array((arr.shape[0]-1,np.nonzero(arr[-1])[0][0]))
	# pos_start=np.nonzero(arr[0])

	# print(pos_end)
	# return
	# pos_end=np.array((0,np.nonzero(arr[-1,:])[0][0]))

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
					pel_new=PathElement(pos_next)
					pel_from_tpos[tpos_next]=pel_new
					not_visited[tpos_next]=False
					pels_to_check.append(pel_new)
					are_neighbors_already=False
				else:
					pel_prev_visited=pel_from_tpos[tpos_next]
					are_neighbors_already=False
					for neigh in pel_prev_visited.neighbors.values():
						if neigh.id==pel_to_check.id:
							are_neighbors_already=True

				if not are_neighbors_already:
					pel_to_check.neighbors[dire] =pel_new
					pel_new.neighbors[OPPO[dire]]=pel_to_check

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


	pelids_checked=set()
	# print(graph)
	# return

	npelids_to_check=set([pel_start.id])

	while len(npelids_to_check)>0:
		npelid_current=npelids_to_check.pop()
		npel_current=pel_from_pid[npelid_current]
		# npel_current_neighbors=npelid_current.neighbors

		for dire_nstart,npel_current_neighbor in npel_current.neighbors.items():
			print(f"Starting from node at {npel_current.pos} in direction {DNAME[dire_nstart]}.")
			if npel_current_neighbor.id not in pelids_checked:
				edge_new=GraphEdge()

				dire_current=dire_nstart

				pel_current=npel_current_neighbor
				while pel_current.id not in graph:
					print(f"In direction {DNAME[dire_current]} to pos {pel_current.pos}.")
					# increas dist
					edge_new.distance+=1
					# add to checked
					pelids_checked.add(pel_current.id)

					assert len(pel_current.neighbors)==2,"Not exactly two neighbors!"

					pel_neighbor_next,dire_next=[(neigh,dire_neigh) for dire_neigh,neigh in pel_current.neighbors.items() if dire_neigh!=OPPO[dire_current]][0]

					# print(neighbor_next,DNAME[dire_next])
					# return
					path_current=arr[tuple(pel_current.pos)]
					if path_current==dire_next:
						# This is a slope in walking direction.
						if edge_new.direction=="none":
							edge_new.direction="forward"
						assert edge_new.direction!="backward","Edge contains forward and backward."
					elif path_current==OPPO[dire_current]:
						# This is a slope against walking direction.
						if edge_new.direction=="none":
							edge_new.direction="backward"
						assert edge_new.direction!="forward","Edge contains forward and backward."
					dire_current=dire_next
					pel_current=pel_neighbor_next

				# assert pel_current.id in graph,"End of edge is not a node."
				# print(pel_current)
				edge_new.pelid_target=pel_current.id
				# print(edge_new)

				return
					# check dire


				pass

		pelids_checked.add(npelid_current)


	print(graph)




	answer=0
	# print(f"ANSWER: {answer}")

class GraphEdge:
	def __init__(self):
		self.pelid_target=None
		self.distance=0
		self.direction="none"
	def __str__(self):
		return f"To pel{self.pelid_target} {self.distance}m {self.direction}"
	def __repr__(self):
		return str(self)


class PathElement:
	NEXT_ID=0
	def __init__(self,pos):
		self.id=PathElement.NEXT_ID
		PathElement.NEXT_ID+=1
		self.pos=pos
		self.neighbors={}
		# self.children=[]
		# self.parents=[]
	def __str__(self):
		return f"pel{self.id}@{self.pos}"
	def __repr__(self):
		return str(self)



def is_in_bounds(pos,arr):
	return 0<=pos[0]<arr.shape[0] and 0<=pos[1]<arr.shape[1]

# def find_connection(context,nid,dire):
# 	distance=1
# 	pos_current=context["pos_from_node_id"][nid]
# 	pos_next=pos_current+DIRE[dire]
# 	available=(context["not_visited"]*context["arr"])>0

# 	if is_in_bounds(pos_next,context["arr"]) and available[tuple(pos_next)]:
# 		cell=context["arr"][tuple(pos_next)]
# 		if cell==PATH:
# 			pass
# 		else





main()
