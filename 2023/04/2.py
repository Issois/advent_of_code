
def main():

	with open("input") as f:
		inp=f.read()

	lines=inp.splitlines()
	total_cards=len(lines)
	card_wins=[]
	card_cnts=[0]*total_cards
	result=0
	for idx,line in enumerate(lines):
		# lidx=idx+1
		card_cnts[idx]+=1
		win,have=[set([int(y) for y in x.split()]) for x in line.replace("|",":").split(":")[1:]]
		wins=len(win&have)
		# count=
		card_wins.append(wins)
		for offset in range(1,wins+1):
			if idx+offset>=total_cards:
				break
			card_cnts[idx+offset]+=card_cnts[idx]
	for i in range(total_cards):
		print(f"{card_wins[i]=},{card_cnts[i]=}")

	print(sum(card_cnts))

	# print(result)

main()
