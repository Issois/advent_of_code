import numpy as np


EMPTY=0
WALL=1
ROCK=3
MAP={".":EMPTY,"#":WALL,"O":ROCK}
IMAP={v:k for k,v in MAP.items()}
def main():
	# with open("example1_136") as f:
	with open("data.input") as f:
		inp=f.read().split("\n")


	arr=np.array([[MAP[y] for y in x] for x in inp],dtype=int)
	inp2=np.array([[y for y in x] for x in inp])

	# MOVE NORTH
	while move_up(arr)>0:
		pass

	# CALC:
	arr=(arr==ROCK).astype(int)
	weights=(np.arange(arr.shape[0])+1)[::-1]
	weights=(weights*np.ones(arr.shape,dtype=int)).T
	print(np.sum(weights*arr))


def move_up(arr):
	diff=arr[1:,]-arr[:-1,]
	switch_to_rock=np.nonzero(diff==ROCK)
	switch_to_empty=(switch_to_rock[0]+1,switch_to_rock[1])
	arr[switch_to_rock]=ROCK
	arr[switch_to_empty]=EMPTY

	switches=switch_to_rock[0].shape[0]
	return switches

main()