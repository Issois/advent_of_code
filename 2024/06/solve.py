
import numpy as np
import sys
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection

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

DIREV2=np.array([
	[-1, 0],
	[-1, 1],
	[ 0, 1],
	[ 1, 1],
	[ 1, 0],
	[ 1,-1],
	[ 0,-1],
	[-1,-1],
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

def is_in_range(pos,arr,check_empty=True):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
		and
		(arr[tuple(pos[[X,Y]])]==0 or not check_empty)
	)

def solve_1(inp,start,dire):
	return solve_1_internal(inp,start,dire)[0]

def solve_1_internal(inp,start,dire):
	answer=-1
	pos=start
	left_the_field=False
	max_steps=inp.shape[X]*inp.shape[Y]
	steps=0

	while(steps<max_steps):
		steps+=1
		inp[tuple(pos)]=1
		new_pos=pos+DIREV2[dire]

		if not is_in_range(new_pos,inp,check_empty=False):
			left_the_field=True
			# print("???")
			break

		if inp[tuple(new_pos)]==2:
			dire=(dire+2)%8
		else:
			pos=new_pos

	if left_the_field:
		answer=np.sum(inp==1)
	else:
		print("too much steps")

	# plt.imshow(inp)
	# plt.show()

	# 5242
	return answer,inp


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
			next_node_pos=cur_pos+((len(beam)-1)*DIREV[cur_dire])
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
	[150,150,150],
	[  0,255,  0],
	[  0,  0,100],
	[  0,150,  0],
	[255,255,  0],
	[255,  0,255],
	[  0,  0,  0],
]

C_START=0
C_NEXT=1
C_CORR=2
C_WRONG_DIRE=9
C_WRONG_SIDE=9
C_NO_DIRE=5
C_NO_RANGE=9
C_BLOCK=3
C_TRG=7
C_SRC=8
C_BLACK=9
C_GREEN=4
C_VISI=6


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
		elif (search_node[N_DIRE]+4)%8!=cur_node[N_DIRE]:
			pass
			# print(f"search node {search_node} not correct dire.")
			if image is not None:image[search_node[N_POS][XY]]=COLORS[C_WRONG_DIRE]
		else:
			dpos_search=np.array(search_node[N_POS])-np.array(cur_node[N_POS])
			side=np.cross(dpos_path,dpos_search)[Z]
			if side>=0:
				pass
				# print(f"search node {search_node} on wrong side.")
				if image is not None:image[search_node[N_POS][XY]]=COLORS[C_WRONG_SIDE]
			else:
				pass
				if image is not None:image[search_node[N_POS][XY]]=COLORS[C_CORR]
				# continue
				project=np.dot(dpos_path,dpos_search)/np.dot(dpos_path,dpos_path)
				if not 0<=project<1:
					pass
					if image is not None:image[search_node[N_POS][XY]]=COLORS[C_NO_RANGE]
				else:
					# Check which are not blocked.
					dists.append(int(project*dist))
					if image is not None:image[search_node[N_POS][XY]]=COLORS[C_CORR]
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

def find_loop(graph,next_node,visited,image=None):
	# print(f"Go down path starting with {next_node}")
	# next_node=graph[cur_node]
	path=[]
	prev_node=next_node
	# dires=[]
	visited_temp=set()
	while True:
		path.append(next_node)
		if next_node in visited:
			# print(f"- found loop in visited  {len(visited_temp)}")
			return 1,path

		elif next_node in visited_temp:
			# print(f"- found loop in visited_temp {len(visited_temp)} {prev_node}->{next_node} {dires}")
			# if (prev_node[N_DIRE]+2)%8!=next_node[N_DIRE]:
			# print(f"- found loop in visited_temp {len(visited_temp)} {prev_node}->{next_node}")
			return 1,path
		elif next_node is None:
			# print("- found no loop")
			return 0,path
		else:
			visited_temp.add(next_node)
			# print(next_node)
			if image is not None:image[next_node[N_POS][XY]]=COLORS[C_GREEN]

			# dires.append(next_node[N_DIRE])
			prev_node=next_node
			next_node=graph[next_node]
			# print(f"move to next node {next_node}")

def solve_2_part_brute_force(arr,start_pos,start_dire):

	start_pos=to_3d(start_pos)
	answer=0

	graph=build_base_graph(arr)
	# add_next_node(arr,start_pos,start_dire,graph)
	start_node=tuple(start_pos),start_dire

	positions=set()


	for x in range(arr.shape[X]):
		for y in range(arr.shape[Y]):
			print(x,y)
			if (x,y,0)!=start_node[N_POS] and arr[x,y]==0:
				changed_targets={}
				nodes_added=[]
				temp_block_pos=np.array((x,y,0))
				# arr_temp=arr.copy()
				# arr_temp[x,y]=2
				# graph=build_base_graph(arr_temp)
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

						# if (start_node[N_DIRE]+2)%8==new_node_dire:
						# 	changed_targets[start_node]=graph[start_node]
						# 	graph[start_node]=new_node

						# Find target for new node.
						add_next_node(arr,new_node_pos,new_node_dire,graph,add_end_node=False)
						nodes_added.append(new_node)


				add_next_node(arr,start_pos,start_dire,graph)
				visited=set()
				cur_node=start_node
				while cur_node is not None and cur_node not in visited:
					visited.add(cur_node)
					cur_node=graph[cur_node]
				if cur_node is not None:
					answer+=1
					positions.add(tuple(temp_block_pos))

				# Revert changes in graph.
				for node_added in nodes_added:
					# print(f"del {node_added}")
					del graph[node_added]
				for node_changed,old_target in changed_targets.items():
					graph[node_changed]=old_target
	# 1412 is wrong.
	return answer,positions


def solve_2_full_brute_force(arr,start_pos,start_dire):
	_,arr1=solve_1_internal(arr.copy(),start_pos,start_dire)
	start_pos=to_3d(start_pos)
	start_node=tuple(start_pos),start_dire



	answer=0
	positions=set()

	count=0

	for x in range(arr.shape[X]):
		for y in range(arr.shape[Y]):
			if (x,y,0)!=start_node[N_POS] and arr1[x,y]==1:
				count+=1
				print(x,y)
				# print("1")
				arr2=arr.copy()
				arr2[x,y]=2
				graph=build_base_graph(arr2)
				# print("2")
				add_next_node(arr2,start_pos,start_dire,graph)
				# start_node=tuple(start_pos),start_dire
				visited=set()
				cur_node=start_node
				# prev_node=cur_node
				while cur_node is not None and cur_node not in visited:
					visited.add(cur_node)
					# prev_node=cur_node
					cur_node=graph[cur_node]
				# print(prev_node)
				if cur_node is not None:
					answer+=1
					positions.add((x,y,0))
				# if count>50:
				# 	return answer,positions
	print(f"fbf answer: {answer}")
	# 1424 is correct.
	return answer,positions




def solve_2(arr,start_pos,start_dire):
	answer_fb,pos_fb=solve_2_full_brute_force(arr,start_pos,start_dire)
	# answer_bf,pos_bf=solve_2_part_brute_force(arr,start_pos,start_dire)
	# answer_sr,pos_sr=solve_2_search(arr,start_pos,start_dire)
	print(pos_fb)

	# for pos in pos_bf:
	# for pos in pos_sr:
		# if arr[pos[:2]]==2:
			# print("WRONG! ",pos)

	# plt.imshow(arr)
	# plt.scatter([p[Y] for p in pos_bf],[p[X] for p in pos_bf],marker="s",c="r")
	# plt.scatter([p[Y] for p in pos_sr],[p[X] for p in pos_sr],marker="o",c="b")
	# plt.show()

	# both=pos_bf&pos_sr
	# only_bf=pos_bf-pos_sr
	# only_sr=pos_sr-pos_bf

	# print(both)
	# print()
	# print()
	# print(only_bf)
	# print()
	# print()
	# print(only_sr)

	return answer_fb

def solve_2_search(arr,start_pos,start_dire):
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
	block_positions=[]
	path=[]
	while cur_node is not None and next_node is not None:
		print(plen)
		visited.add(cur_node)
		path.append(cur_node)
		# cur_node
		# print(f"Current node: {cur_node}.")
		# print(f"Next node: {next_node}.")

		image=np.zeros((arr.shape[X],arr.shape[Y],3),dtype=int)
		image=None
		image1=None
		if image is not None:
			for node in visited:
				image[node[N_POS][XY]]=COLORS[C_VISI]
			image[cur_node[N_POS][XY]]=COLORS[C_START]
			image[next_node[N_POS][XY]]=COLORS[C_NEXT]
			image[arr==2]=COLORS[C_BLOCK]

			# image[arr==2]=COLORS[C_BLOCK]

		# Find all nodes to the right between both nodes.
		dists=find_potential_target_nodes(graph,cur_node,next_node,image)
		# dists=find_potential_target_nodes(graph,cur_node,next_node,image)
		dists=set(dists)
		# dists=[]
		for dist_idx,dist in enumerate(dists):
			if image is not None:
				image1=image.copy()
			# Add stone at dist+1 and temp nodes.
			temp_block_pos=cur_node[N_POS]+((dist+1)*DIREV[cur_node[N_DIRE]])
			if image is not None:image1[tuple(temp_block_pos)[XY]]=COLORS[C_TRG]
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
							if image is not None: image1[source_node[N_POS][XY]]=COLORS[C_SRC]
							changed_targets[source_node]=graph[source_node]
							graph[source_node]=new_node

						if cur_node==start_node and (cur_node[N_DIRE]+2)%8==new_node_dire:
							changed_targets[start_node]=graph[start_node]
							graph[start_node]=new_node

						# Find target for new node.
						add_next_node(arr,new_node_pos,new_node_dire,graph,add_end_node=False)
						nodes_added.append(new_node)

				loop_count,temp_path=find_loop(graph,graph[cur_node],visited,image1)
				answer+=loop_count
				if loop_count==1:
					block_positions.append(tuple(temp_block_pos))

				# Revert changes in graph.
				for node_added in nodes_added:
					del graph[node_added]
				for node_changed,old_target in changed_targets.items():
					graph[node_changed]=old_target
			if image is not None and loop_count==1:
			# if image is not None and dist_idx==len(dists)-1 and plen%10==0:

				plt.imshow(image1)
				lines=[node[N_POS][1::-1] for node in path]
				if len(lines)>1:
					plt.gca().add_collection(LineCollection([lines],colors=["r"]))
				lines=[lines[-1]]+[node[N_POS][1::-1] for node in temp_path]
				if len(lines)>1:
					plt.gca().add_collection(LineCollection([lines],colors=["g"]))
				# plt.gca().add_collection(LineCollection([node[N_POS][XY] for node in temp_path]))
				fig=plt.gcf()
				fig.set_size_inches(9, 9)
				fig.tight_layout()
				# fig.canvas.manager.window.move(0,0)
				plt.show()
				if input()=="x":exit()

		cur_node=next_node
		next_node=graph[cur_node]
		plen+=1
		# if plen>4:return
		# return
	answer=len(block_positions)
	print(f"search total loops: {answer}")
	block_positions=set(block_positions)
	if start_node[N_POS] in block_positions:
		block_positions.remove(start_node[N_POS])
	answer=len(block_positions)
	print(f"search answer: {answer}")
 	# 1526 too high
	# 1583 even higher
	# 1564 still too high
	# 1562 still too high
	# 1563 still too high
	# 1497 is too high
	return answer,block_positions

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




