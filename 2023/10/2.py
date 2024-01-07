import matplotlib.pyplot as plt
import numpy as np
def main():

	with open("data.input") as f:
		inp=np.array([list(x) for x in f.read().split("\n")])

	UP=0
	LE=1
	DO=2
	RI=3

	UNKNOWN_DIRE=-1

	UNCHECKED=-1
	UNCHECKED_LOOP=0
	CHECKED=1
	INSIDE_LOOP=2

	CW=1
	CCW=2

	pipes={
		"|":"02",
		"-":"13",
		"L":"01",
		"J":"03",
		"7":"23",
		"F":"12",
	}

	arr_from_pipe={
		"|":np.array([0,1,0,0,1,0,0,1,0]).reshape((3,3)),
		"-":np.array([0,0,0,1,1,1,0,0,0]).reshape((3,3)),
		"L":np.array([0,1,0,0,1,1,0,0,0]).reshape((3,3)),
		"J":np.array([0,1,0,1,1,0,0,0,0]).reshape((3,3)),
		"7":np.array([0,0,0,1,1,0,0,1,0]).reshape((3,3)),
		"F":np.array([0,0,0,0,1,1,0,1,0]).reshape((3,3)),
	}


	pipes={c:{int(a[0]):int(a[1]),int(a[1]):int(a[0])} for c,a in pipes.items()}


	offs_from_dire=np.array([
		[-1,0],
		[0,1],
		[1,0],
		[0,-1],
	])

	pos=np.array(np.nonzero(inp=="S"))[:,0]
	start=pos

	img=np.zeros(np.array(inp.shape)*3,dtype=np.byte)
	img[3*pos[0]:3*pos[0]+3,3*pos[1]:3*pos[1]+3]=np.ones((3,3))

	mask=np.zeros(inp.shape,dtype=np.byte)+UNCHECKED
	dire_mask=np.zeros(inp.shape,dtype=np.byte)+UNKNOWN_DIRE
	curve_mask=np.zeros(inp.shape,dtype=np.byte)

	for dire,offs in enumerate(offs_from_dire):
		new_pos=pos+offs
		new_pipe=inp[tuple(new_pos)]
		if (dire+2)%4 in pipes[new_pipe]:
			pos=new_pos
			break
	prev_dire=dire

	current_angle=dire
	pipe=inp[tuple(pos)]

	while not inp[tuple(pos)]=="S":
		pipe=inp[tuple(pos)]
		mask[tuple(pos)]=UNCHECKED_LOOP
		new_dire=pipes[pipe][(prev_dire+2)%4]
		img[3*pos[0]:3*pos[0]+3,3*pos[1]:3*pos[1]+3]=arr_from_pipe[pipe]


		if (prev_dire+new_dire)%2==1:
			if prev_dire==0 and new_dire==3:
				cw=False
			elif prev_dire==3 and new_dire==0:
				cw=True
			else:
				cw=new_dire-prev_dire>0
			curve=1*(1 if cw else -1)
			current_angle+=curve
			curve_mask[tuple(pos)]=CW if cw else CCW
		dire_mask[tuple(pos)]=prev_dire
		pos+=offs_from_dire[new_dire]
		prev_dire=new_dire

	inside_dire_offset=1 if current_angle>0 else -1

	cw_is_outside_curve=current_angle>0

	to_check=np.nonzero(mask==UNCHECKED_LOOP)
	to_check=[np.array(x) for x in zip(*to_check)]
	while len(to_check)>0:
		current_pos=to_check.pop()
		current_val=mask[tuple(current_pos)]
		if current_val==UNCHECKED:
			mask[tuple(current_pos)]=INSIDE_LOOP
			for dire in range(4):
				to_check.append(current_pos+offs_from_dire[dire])
		elif current_val==UNCHECKED_LOOP:
			mask[tuple(current_pos)]=CHECKED
			curve=curve_mask[tuple(current_pos)]
			if curve>0:
				if cw_is_outside_curve==(curve==CCW):
					for dire in range(4):
						to_check.append(current_pos+offs_from_dire[dire])

			else:
				inside_dire=(dire_mask[tuple(current_pos)]+inside_dire_offset)%4
				to_check.append(current_pos+offs_from_dire[inside_dire])
		elif current_val==CHECKED:
			pass
		elif current_val==INSIDE_LOOP:
			pass
		else:
			print(f"??? {current_val}")


	# Start point gets counted as well (but that does not happen on all inputs)
	print(np.nonzero(mask==INSIDE_LOOP)[0].shape[0]-1)
	plt.imshow(mask,extent=(0,1,1,0))
	plt.imshow(img,alpha=0.1,extent=(0,1,1,0))
	plt.show()


main()
