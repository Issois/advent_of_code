

def main():

	with open("input") as f:
		inp=f.readlines()

	times,distances=[[int(x) for x in inp[i].split()[1:]] for i in [0,1]]
	# print(inp[0].split())
	print(f"{times=},{distances=}")
	prod=1

	for t,d in zip(times,distances):
		target=1
		while get_distance(target,t)<=d:
			target+=1
		# print(target)
		if t%2==0:
			result=(((t//2)-target)*2)+1
		else:
			result=(((t//2)-target)*2)+2
		print(f"{target=},{result=}")
		prod*=result

	print(prod)


def get_distance(time,total_time):
	return time*(total_time-time)



main()
