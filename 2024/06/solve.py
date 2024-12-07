
import numpy as np
import sys
import matplotlib.pyplot as plt

X=0
Y=1
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

ar=np.array

UNVISITED=0
VISITED=1


def main():
	with open(sys.argv[2]) as f:
		inp=f.read().split("\n")
	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]
	
	inp=[list(line) for line in inp]
	inp=np.array(inp)
	hasht=inp=="#"
	point=inp=="."
	inp[point]=0
	inp[hasht]=2
	start=np.logical_not(np.logical_or(point,hasht))
	start=np.nonzero(start)
	start=np.array((start[X][0],start[Y][0]))
	dire=inp[tuple(start)]
	dire={"^":0,">":2,"v":4,"<":6}[dire]
	inp[tuple(start)]=0
	inp=inp.astype(int)

	print(f"ANSWER: {solve(inp,start,dire)}")

def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)

def solve_1(inp,start,dire):
	answer=-1
	pos=start
	left_the_field=False
	max_steps=inp.shape[X]*inp.shape[Y]
	steps=0

	while(steps<max_steps):
		steps+=1
		inp[tuple(pos)]=1
		new_pos=pos+DIREV[dire]

		if not is_in_range(new_pos,inp):
			left_the_field=True
			break

		if inp[tuple(new_pos)]==2:
			dire=(dire+2)%8
		else:
			pos=new_pos

	if left_the_field:
		answer=np.sum(inp==1)
	else:
		print("too much steps")

	plt.imshow(inp)
	plt.show()

	# 5242
	return answer


def get_beam(arr,pos,dire):
	if False:pass
	elif dire==0:res=arr[:pos[X]   , pos[Y]   ]
	elif dire==2:res=arr[ pos[X]   , pos[Y]+1:]
	elif dire==4:res=arr[ pos[X]+1:, pos[Y]   ]
	elif dire==6:res=arr[ pos[X]   ,:pos[Y]   ]
	else:raise ValueError(f"Beam invalid direction: {dire}")
	if dire==0 or dire==6:
		res=res[::-1]
	return res

N_DATA=0
N_D_POS=0
N_D_DIRE=1
N_VISIT=1


def find_next_node(arr,cur_pos,cur_dire):
	# cur_pos,cur_dire=cur_node_data
	# cur_pos=ar(cur_pos)
	beam=get_beam(arr,cur_pos,cur_dire)
	# print(cur_node_data,beam)
	occ=np.nonzero(beam)[0]
	# return
	if len(occ)==0:
		# if len(beam)==0:
			# next_node_pos=
		next_node=None
		# nodes[cur_node_data]=None
	else:
		next_node_pos=tuple(cur_pos+((occ[0])*DIREV[cur_dire]))
		next_node_dire=(cur_dire+4)%8
		next_node=[(tuple(next_node_pos),next_node_dire),UNVISITED]
		# print(pos,dire,cur_dire,next_node_pos)
	return next_node
	# nodes[cur_node_data]=[(next_node_pos,next_node_dire),UNVISITED]

def build_base_graph(arr):
	positions=np.array(np.nonzero(arr==2)).T
	nodes={}
	for pos in positions:
		for dire in range(0,8,2):
			cur_pos=pos+DIREV[dire]
			cur_dire=(dire+6)%8
			cur_node_data=tuple(cur_pos),cur_dire
			if is_in_range(cur_pos,arr):
				nodes[cur_node_data]=find_next_node(arr,cur_pos,cur_dire)
	return nodes

def solve_2(arr,start_pos,start_dire):
	answer=0

	graph_base=build_base_graph(arr)
	start_node_data=tuple(start_pos),start_dire
	graph_base[start_node_data]=find_next_node(arr,start_pos,start_dire)
	for node_data_a,node_b in graph_base.items():
		if node_b is not None:
			plt.plot([node_data_a[N_D_POS][X],node_b[N_DATA][N_D_POS][X]],[node_data_a[N_D_POS][Y],node_b[N_DATA][N_D_POS][Y]],color="r")

	plt.show()

	return
	node="start"
	path=[]
	pnodes=[]
	max_steps=1000
	steps=0
	# for start,end in graph_base.items():
	# 	print(start,end)
	# # print(graph_base)
	while node is not None:
		if len(pnodes)>3:
			node_pos,node_dire=node
			# look at all prev with dire+6 and to the right
			target_node_dire=(node_dire+2)%8
			dire_right =DIREV[(node_dire+6)%8]
			dire_behind=DIREV[ node_dire     ]

			delta=ar(path[-1])-ar(node[0])
			# print(path[-1],node[0],delta)
			# return
			delta3=np.zeros((3),dtype=int)
			delta3[:2]=delta

			print(f"current node {node}, {delta}")
			for pnode in pnodes[1:-2]:
				pnode_pos,pnode_dire=pnode
				print(path[-1],pnode)
				deltap=ar(path[-1])-ar(pnode_pos)
				deltap3=np.zeros((3),dtype=int)
				deltap3[:2]=deltap

				print(delta3,deltap3)
				cross=np.cross(delta3,deltap3)
				print(cross)

				# if pnode_dire==target_node_dire:
				# 	print(f"node correct {pnode}")
				# else:
				# 	print(f"node wrong   {pnode}")


			break


		if node=="start":
			path=[start_pos]
		else:
			path.append(np.array(node[0])+DIREV[node[1]])
		pnodes.append(node)
		node=graph_base[node]
		steps+=1
		if steps>max_steps:raise ValueError("Too many steps!")

	path=np.array(path)
	# print(path)

	# positions=np.array(np.nonzero(inp==2)).T
	# plt.scatter(positions[:,Y],positions[:,X],color="r",marker="s")

	# plt.gca().invert_yaxis()
	# plt.plot(path[:,Y],path[:,X])
	# plt.show()









	return answer

main()
