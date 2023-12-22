
import numpy as np
import functools

values="AKQJT98765432"[::-1]

values={values[i]:i for i in range(len(values))}

def main():
	with open("input") as f:
		inp=f.read().split()

	inp=np.array(inp,dtype="str")
	hands=inp[0::2]
	scores=inp[1::2]


	indices=np.arange(hands.shape[0])
	handsx=np.vstack((hands,indices)).transpose().tolist()


	handsxs=sorted(handsx,key=functools.cmp_to_key(compare))
	result=0
	for idx,hand in enumerate(handsxs):
		rank=idx+1
		score=scores[int(hand[1])]
		result+=rank*int(score)
	print(result)


def cparr(a,b):
	print(a,b)
	return a[0]-b[0]

def compare(a,b):
	ta=get_type(a[0])
	tb=get_type(b[0])
	if ta==tb:
		for aa,bb in zip(a[0],b[0]):
			if not aa==bb:
				return values[aa]-values[bb]
		return 0
	else:
		return ta-tb

def get_type(hand):
	hand=sorted(hand)
	streaks=[]
	prev_card=hand[0]
	current_streak=1
	for card in hand[1:]:
		if card==prev_card:
			current_streak+=1
		else:
			prev_card=card
			streaks.append(current_streak)
			current_streak=1

	streaks.append(current_streak)


	streaks=sorted(streaks)[::-1]
	if streaks[0]>3:
		return streaks[0]+1
	elif streaks[0]==3:
		if streaks[1]==2:
			return 4
		else:
			return 3
	elif streaks[0]==2:
		if streaks[1]==2:
			return 2
		else:
			return 1
	else:
		return 0






main()