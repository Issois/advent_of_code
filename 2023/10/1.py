import numpy as np
def main():
	with open("input") as f:
		inp=np.array([list(x) for x in f.read().split("\n")])
	#  0
	# 3 1
	#  2
	pipes={
		"|":"02",
		"-":"13",
		"L":"01",
		"J":"03",
		"7":"23",
		"F":"12",
	}

	pipes={c:{int(a[0]):int(a[1]),int(a[1]):int(a[0])} for c,a in pipes.items()}

	print(pipes)
	# return

	offs_from_dire=np.array([
		[-1,0],
		[0,1],
		[1,0],
		[0,-1],
	])

	pos=np.array(np.nonzero(inp=="S"))[:,0]

	print(pos)

	for dire,offs in enumerate(offs_from_dire):
		# print()
		new_pos=pos+offs
		new_pipe=inp[tuple(new_pos)]
		if (dire+2)%4 in pipes[new_pipe]:
			print(f"Found next step in direction {dire}")
			pos=new_pos
			step_count=1
			break
	prev_dire=dire

	while not inp[tuple(pos)]=="S":
		pipe=inp[tuple(pos)]
		new_dire=pipes[pipe][(prev_dire+2)%4]
		pos+=offs_from_dire[new_dire]
		step_count+=1
		print(f"Found next step {step_count} from {pipe} in direction {new_dire}")
		prev_dire=new_dire

	print(step_count//2)


main()
