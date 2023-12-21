
def main():

	with open("input") as f:
		inp=f.read()

	lines=inp.splitlines()
	# lines=lines[:2]
	result=0
	for idx,line in enumerate(lines):
		lidx=idx+1
		win,have=[set([int(y) for y in x.split()]) for x in line.replace("|",":").split(":")[1:]]
		count=len(win&have)
		if count>0:
			result+=2**(count-1)

	print(result)

main()
