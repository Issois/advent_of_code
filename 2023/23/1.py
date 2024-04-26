
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
		for dire in DIRE.values():
			pos_next=pel_to_check.pos+dire
			tpos_next=tuple(pos_next)
			if is_in_bounds(pos_next,arr) and arr[tpos_next]>FOREST:
				if not_visited[tpos_next]:
					pel_new=PathElement(pos_next)
					pel_from_tpos[tpos_next]=pel_new
					not_visited[tpos_next]=False
					pels_to_check.append(pel_new)
					are_neighbors_already=False
				else:
					pel_old=pel_from_tpos[tpos_next]
					are_neighbors_already=False
					for neigh in pel_old.neighbors:
						if neigh.id==pel_to_check.id:
							are_neighbors_already=True

				if not are_neighbors_already:
					pel_to_check.neighbors.append(pel_new)
					pel_new.neighbors.append(pel_to_check)
					# if len([neigh for neigh in pel_old.neighbors if tuple(neigh)])

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

	while len(npelids_to_check)>0:
		return


	# graph={}

	# for idx,pel in enumerate(pel_from_tpos.values()):
	# 	test[tuple(pel.pos)]=100

	# for npel in node_pels:
	# 	test[tuple(npel.pos)]=200
	# pe=pel_start
	# test[tuple(pe.pos)]=1
	# while len(pe.children)>0:
	# 	pe=pe.children[0]
	# 	test[tuple(pe.pos)]=1



	plt.imshow(test)
	plt.show()
	return


	# pos_current=np.array((0,np.nonzero(arr[0])[0][0]))
	# pos_from_node_id={
	# 	0:pos_current
	# }
	# node_id_from_tpos={tuple(pos):nid for nid,pos in enumerate(pos_from_node_id)}



	# context={
	# 	"arr":arr,
	# 	"not_visited":not_visited,
	# 	"pos_from_node_id":pos_from_node_id,
	# 	"node_id_from_tpos":node_id_from_tpos,
	# }
	# # print(not_visited.astype(int))
	# # print(arr)

	# # print(available.astype(int))
	# # print(start_col)
	
	# out={}
	# id_current=0
	# len_current=0

	# nodes_and_dires_to_check=[(pos_current,SO)]


	# pos_next=

	# while True:



	answer=0
	# print(f"ANSWER: {answer}")

class PathElement:
	NEXT_ID=0
	def __init__(self,pos):
		self.id=PathElement.NEXT_ID
		PathElement.NEXT_ID+=1
		self.pos=pos
		self.neighbors=[]
		# self.children=[]
		# self.parents=[]


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
