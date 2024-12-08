
import numpy as np
import sys
import matplotlib.pyplot as plt

X=0
Y=1
Z=2
XY=slice(X,Y+1)

DIREV=np.array([
	[-1, 0, 0],
	[-1, 1, 0],
	[ 0, 1, 0],
	[ 1, 1, 0],
	[ 1, 0, 0],
	[ 1,-1, 0],
	[ 0,-1, 0],
	[-1,-1, 0],
])


def main():



	# print(np.heaviside(4,1)*2-1)
	# # print(np.arange(-4,6))
	# return
	# arr=np.array([[a+b for b in range(10)] for a in range(0,100,10)])
	# # print(arr[3:7,4:5])

	# # print(arr[5:100:1,:])

	# start_pos=np.array((0,0,0))
	# size=5,0
	# for dire in range(0,8,2):
	# 	selection=select(arr,start_pos,dire,size)
	# 	print(selection.shape,selection)

	# return

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
	# inp[tuple(start)]=3
	# print(dire)
	# plt.imshow(inp)
	# plt.show()



def select(arr,start_pos,dire,size):
	direvs=[
		DIREV[dire],
		DIREV[(dire+2)%8]
	]

	end_pos=start_pos.copy()
	for idx in range(2):
		end_pos+=size[idx]*direvs[idx]
	# print(start_pos,end_pos)
	selection=select_internal(arr,start_pos,end_pos)
	if dire%4==2:
		selection=selection.T
	return selection

def select_internal(arr,p1,p2):
	# print(p1,p2)
	diff=p2-p1
	xstep=int(2*np.heaviside(diff[X],1))-1
	p2[X]+=xstep
	ystep=int(2*np.heaviside(diff[Y],1))-1
	p2[Y]+=ystep

	# print(p1,p2,xstep,ystep)

	return arr[p1[X]:p2[X]:xstep,p1[Y]:p2[Y]:ystep]

def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
		and
		arr[tuple(pos[[X,Y]])]==0
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

# N_DATA=0
N_POS=0
N_DIRE=1
# N_VISIT=1


def add_next_node(arr,cur_pos,cur_dire,graph,add_end_node=True):
	# cur_pos,cur_dire=cur_node_data
	# beam=get_beam(arr,cur_pos,cur_dire)
	beam=select(arr,cur_pos,cur_dire,(np.sum(arr.shape),0))
	# print(beam.shape,beam)
	if beam.shape[0]==0:
		occ=[]
		# beam=beam
	else:
		beam=beam[:,0]
		occ=np.nonzero(beam)[0]
	# exit()
	# [:,0]
	# print(f"ann: cur pos: {cur_pos}")
	cur_node=tuple(cur_pos),cur_dire
	# return
	if len(occ)==0:
		if len(beam)==0 or not add_end_node:
			next_node=None
		else:
			next_node_pos=cur_pos+(len(beam)*DIREV[cur_dire])
			next_node=tuple(next_node_pos),None
			graph[next_node]=None
	else:
		next_node_pos=tuple(cur_pos+((occ[0]-1)*DIREV[cur_dire]))
		next_node_dire=(cur_dire+2)%8
		next_node=tuple(next_node_pos),next_node_dire
		# print(pos,dire,cur_dire,next_node_pos)

	graph[cur_node]=next_node

def to_3d(vec2):
	return np.array(list(vec2)+[0])

def build_base_graph(arr):
	positions=np.array(np.nonzero(arr==2)).T
	graph={}
	for pos2d in positions:
		pos=to_3d(pos2d)
		for dire in range(0,8,2):
			# print(f"xx {pos}")
			cur_pos=pos+DIREV[dire]
			cur_dire=(dire+6)%8
			if is_in_range(cur_pos,arr):
				# print(f"bbg cur pos {cur_pos}")
				add_next_node(arr,cur_pos,cur_dire,graph)
				# graph[cur_node_data]=find_next_node(arr,cur_pos,cur_dire)
	return graph

COLORS=[
	[255,  0,  0],
	[155,  0,  0],
	[255,255,255],
	[ 50, 50, 50],
	[  0,255,  0],
	[  0,  0,100],
	[  0,  0,255],
	[ 50, 50, 50],
]

C_START=0
C_NEXT=1
C_CORR=2
C_WRONG_DIRE=3
C_WRONG_SIDE=4
C_NO_DIRE=5
C_NO_RANGE=6
C_BLOCK=7


def find_potential_target_nodes(graph,cur_node,next_node,image):
	dists=[]
	dpos_path=np.array(next_node[N_POS])-np.array(cur_node[N_POS])
	dist=np.linalg.norm(dpos_path)
	for search_node in graph:
		if search_node==cur_node or search_node==next_node:
			pass
		elif search_node[N_DIRE] is None:
			pass
			# print(f"search node {search_node} has no dire.")
			# image[search_node[N_POS][XY]]=COLORS[C_NO_DIRE]
		elif (search_node[N_DIRE]+4)%8!=cur_node[N_DIRE]:
			pass
			# print(f"search node {search_node} not correct dire.")
			# image[search_node[N_POS][XY]]=COLORS[C_WRONG_DIRE]
		else:
			dpos_search=np.array(search_node[N_POS])-np.array(cur_node[N_POS])
			side=np.cross(dpos_path,dpos_search)[Z]
			if side>=0:
				pass
				# print(f"search node {search_node} on wrong side.")
				# image[search_node[N_POS][XY]]=COLORS[C_WRONG_SIDE]
			else:
				pass
				# image[search_node[N_POS][XY]]=COLORS[C_CORR]
				# continue
				project=np.dot(dpos_path,dpos_search)/np.dot(dpos_path,dpos_path)
				if not 0<=project<1:
					pass
					# image[search_node[N_POS][XY]]=COLORS[C_NO_RANGE]
				else:
					# Check which are not blocked.
					dists.append(int(project*dist))
					# image[search_node[N_POS][XY]]=COLORS[C_CORR]
	return dists

def find_source_nodes(arr,node):
	# print(f"Find sources for node {node}")
	search_dire=(node[N_DIRE]+2)%8
	node_pos=np.array(node[N_POS])
	area=select(arr,node_pos,search_dire,(np.sum(arr.shape),1))
	nodes=[]
	if area.shape[0]==0 or area.shape[1]<2:
		return nodes

	# print(node,dire)
	# print(area)
	# beam=get_beam(arr,node[N_POS],dire)
	# print(f"araee shape: {area.shape} {area}")
	occ=np.nonzero(area[:,0])[0]
	# print(occ)
	if len(occ)>0:
		area=area[:occ[0],1]
	else:
		area=area[:,1]
	# print(area)
	for occ in np.nonzero(area)[0]:
		source_node_pos=node_pos+(occ*DIREV[search_dire])
		source_node_dire=(search_dire+4)%8
		source_node=tuple(source_node_pos),source_node_dire
		# print(source_node)
		nodes.append(source_node)

	return nodes

def find_loop(graph,next_node,visited):
	# print(f"Go down path starting with {next_node}")
	# next_node=graph[cur_node]
	prev_node=next_node
	# dires=[]
	visited_temp=set()
	while True:
		if next_node in visited:
			# print(f"- found loop in visited  {len(visited_temp)}")
			return 1

		elif next_node in visited_temp:
			# print(f"- found loop in visited_temp {len(visited_temp)} {prev_node}->{next_node} {dires}")
			# if (prev_node[N_DIRE]+2)%8!=next_node[N_DIRE]:
				# print(f"- found loop in visited_temp {len(visited_temp)} {prev_node}->{next_node}")
			return 1
		elif next_node is None:
			# print("- found no loop")
			return 0
		else:
			visited_temp.add(next_node)
			# dires.append(next_node[N_DIRE])
			prev_node=next_node
			next_node=graph[next_node]
			# print(f"move to next node {next_node}")


def solve_2(arr,start_pos,start_dire):
	start_pos=to_3d(start_pos)
	answer=0

	graph=build_base_graph(arr)
	add_next_node(arr,start_pos,start_dire,graph)
	start_node=tuple(start_pos),start_dire


	# node=start_node
	# while node is not None:
	# 	print(node)
	# 	node=graph[node]
	# return


	# for node,node_target in graph.items():
	# 	print(node,node_target)

	# return

	visited=set()


	cur_node=start_node
	next_node=graph[cur_node]
	plen=0
	while cur_node is not None and next_node is not None:
		print(plen)
		visited.add(cur_node)
		# cur_node
		# print(f"Current node: {cur_node}.")
		# print(f"Next node: {next_node}.")

		# image=np.zeros((arr.shape[X],arr.shape[Y],3),dtype=int)
		# image[cur_node[N_POS][XY]]=COLORS[C_START]
		# image[next_node[N_POS][XY]]=COLORS[C_NEXT]
		# image[arr==2]=COLORS[C_BLOCK]

		# Find all nodes to the right between both nodes.
		dists=find_potential_target_nodes(graph,cur_node,next_node,None)
		# dists=find_potential_target_nodes(graph,cur_node,next_node,image)
		dists=set(dists)
		# dists=[]
		for dist in dists:
			# Add stone at dist+1 and temp nodes.
			temp_block_pos=cur_node[N_POS]+((dist+1)*DIREV[cur_node[N_DIRE]])
			if is_in_range(temp_block_pos,arr):
				# print(f"temp block pos: {temp_block_pos}")
				changed_targets={}
				nodes_added=[]
				for new_node_dire in range(0,8,2):
					new_node_pos=temp_block_pos+DIREV[(new_node_dire+2)%8]
					if is_in_range(new_node_pos,arr):
						new_node=(tuple(new_node_pos),new_node_dire)
						# Search for nodes that could hit temp nodes.
						source_nodes=find_source_nodes(arr,new_node)
						# Safe their targets and write temp target.
						for source_node in source_nodes:
							changed_targets[source_node]=graph[source_node]
							graph[source_node]=new_node

						# if cur_node==start_node:
						# 	changed_targets[start_node]=graph[start_node]
						# 	graph[start_node]=new_node

						# Find target for new node.
						add_next_node(arr,new_node_pos,new_node_dire,graph,add_end_node=False)
						nodes_added.append(new_node)

				loop_count=find_loop(graph,graph[cur_node],visited)
				answer+=loop_count

				# Revert changes in graph.
				for node_added in nodes_added:
					del graph[node_added]
				for node_changed,old_target in changed_targets.items():
					graph[node_changed]=old_target
		# plt.imshow(image)
		# plt.show()

		cur_node=next_node
		next_node=graph[cur_node]
		plen+=1
		# if plen>4:return
		# return


	# 1526 too high
	# 1583 even higher
	# 1564 still to high
	return answer

# LOOPS=[]
#

main()


	# return

	# while start_node is not None:
	# 	print(f"PATH iter: {start_node}")
	# 	start_node=graph[start_node]
	# return

	# graph[start_node_data]=
	# positions=np.array(np.nonzero(arr==2)).T
	# plt.imshow(arr)
	# # plt.scatter(positions[:,Y],positions[:,X],color="r",marker="s")
	# for node_data_a,node_b in graph.items():
	# 	if node_b is not None:
	# 		color="r"
	# 		lw=0
	# 		ls="-"
	# 		if graph[node_b[N_DATA]] is None:
	# 			color="w"
	# 			ls=":"
	# 			lw=2
	# 		plt.plot([node_data_a[N_D_POS][Y],node_b[N_DATA][N_D_POS][Y]],[node_data_a[N_D_POS][X],node_b[N_DATA][N_D_POS][X]],linestyle=ls,linewidth=lw,color=color)

	# # plt.gca().invert_yaxis()

	# plt.show()

	# return


	# for start,end in graph.items():
	# 	print(start,end)
	# # print(graph)
	# while node is not None:

	# 	if len(pnodes)>3:
	# 		node_pos,node_dire=node
	# 		# look at all prev with dire+6 and to the right
	# 		target_node_dire=(node_dire+2)%8
	# 		dire_right =DIREV[(node_dire+6)%8]
	# 		dire_behind=DIREV[ node_dire     ]

	# 		delta=ar(path[-1])-ar(node[0])
	# 		# print(path[-1],node[0],delta)
	# 		# return
	# 		delta3=np.zeros((3),dtype=int)
	# 		delta3[:2]=delta

	# 		print(f"current node {node}, {delta}")
	# 		for pnode in pnodes[1:-2]:
	# 			pnode_pos,pnode_dire=pnode
	# 			print(path[-1],pnode)
	# 			deltap=ar(path[-1])-ar(pnode_pos)
	# 			deltap3=np.zeros((3),dtype=int)
	# 			deltap3[:2]=deltap

	# 			print(delta3,deltap3)
	# 			cross=np.cross(delta3,deltap3)
	# 			print(cross)

	# 			# if pnode_dire==target_node_dire:
	# 			# 	print(f"node correct {pnode}")
	# 			# else:
	# 			# 	print(f"node wrong   {pnode}")


	# 		break


	# 	if node=="start":
	# 		path=[start_pos]
	# 	else:
	# 		path.append(np.array(node[0])+DIREV[node[1]])
	# 	pnodes.append(node)
	# 	node=graph_base[node]
	# 	steps+=1
	# 	if steps>max_steps:raise ValueError("Too many steps!")

	# path=np.array(path)
	# print(path)

	# positions=np.array(np.nonzero(inp==2)).T
	# plt.scatter(positions[:,Y],positions[:,X],color="r",marker="s")

	# plt.gca().invert_yaxis()
	# plt.plot(path[:,Y],path[:,X])
	# plt.show()




