

def main():

	with open("data.input") as f:
		inp=f.readlines()

	time,distance=[int("".join([x for x in inp[i].split()[1:]])) for i in [0,1]]
	# times=
	# print(inp[0].split())
	# print(f"{times=},{distances=}")
	# print(distances+1)

	t1=1
	t2=time//2

	while t1!=t2:
		center=(t1+t2)//2
		print(f"{t1=},{t2=},{center=}")

		if get_distance(center,time)<distance:
			t1=center+1
		else:
			t2=center

	result=(((time//2)-t1)*2)+2

	print(result)



def get_distance(time,total_time):
	return time*(total_time-time)


main()
