
import numpy as np
import sys



def array(*vals):
	return np.array(vals)

ROW=0
COL=1

EM=0
HO=1
VE=2
SL=3
BA=4

NO=0
EA=1
SO=2
WE=3

SYMBOL=0
OUTPUT_FROM_INPUT=1

INFO={
	EM:("." ,None),
	HO:("-" ,{NO:[EA,WE],EA:[EA   ],SO:[EA,WE],WE:[WE   ]}),
	VE:("|" ,{NO:[NO   ],EA:[NO,SO],SO:[SO   ],WE:[NO,SO]}),
	SL:("/" ,{NO:[EA   ],EA:[NO   ],SO:[WE   ],WE:[SO   ]}),
	BA:("\\",{NO:[WE   ],EA:[SO   ],SO:[EA   ],WE:[NO   ]}),
}

VECTOR=0
NAME=1

DIRE={
	NO:(array(-1, 0),"NO"),
	EA:(array( 0, 1),"EA"),
	SO:(array( 1, 0),"SO"),
	WE:(array( 0,-1),"WE"),
}

LO_ENER=" "
HI_ENER="#"

START=array(0,-1)

def main():
	with open("example1" if "e" in sys.argv else "input") as f:
		inp=np.array([list(x) for x in f.read().split("\n")])

	FILT={k:inp==v[SYMBOL] for k,v in INFO.items() if k!=EM}

	arr=np.zeros(inp.shape,dtype=int)

	for key,filt in FILT.items():
		arr[filt]=key

	energized=inp.copy()
	energized[:,:]=LO_ENER

	targets=[]

	beam=fire_beam(arr,array(0,-1),EA,is_start_beam=True)
	energized[beam]=arr[beam]
	print(energized)
	targets.append(((beam[ROW][-1],beam[COL][-1]),EA))

	while len(targets)>0:
		target_pos,input_dire=targets.pop()
		print(f"-- Popped new target ({len(targets)} remaining): {target_pos} beamed from {DIRE[input_dire][NAME]}")
		for output_dire in INFO[arr[target_pos]][OUTPUT_FROM_INPUT][input_dire]:
			# print(f"  ????  {target_pos=}")
			# print(f"  ????  {INFO[arr[target_pos]][SYMBOL]=}")
			# print(f"  ????  {INFO[arr[target_pos]][OUTPUT_FROM_INPUT]=}")
			# print(f"  ????  {input_dire=}")
			# print(f"  ????  {INFO[arr[target_pos]][OUTPUT_FROM_INPUT][input_dire]=}")
			print(f"~~ Target {target_pos} {INFO[arr[target_pos]][SYMBOL]} beams towards {DIRE[output_dire][NAME]}")
			beam=fire_beam(arr,array(*target_pos),output_dire)
			if len(beam[0])>0:
				new_target_pos=(beam[ROW][-1],beam[COL][-1])
				is_diagonal=arr[new_target_pos] in [SL,BA]
				is_not_energized=energized[new_target_pos]==LO_ENER
				is_not_empty=arr[new_target_pos]!=EM
				print(f"~~ new target_pos {new_target_pos} is {'' if is_diagonal else 'not '}diagonal, is {'not ' if is_not_energized else ''}energized and is {'not ' if is_not_empty else ''}empty")
				if is_diagonal or (is_not_energized and is_not_empty):
					targets.append((new_target_pos,output_dire))
					print(f"++ Pushed new target ({len(targets)} remaining): {new_target_pos} beamed from {DIRE[output_dire][NAME]}")
				energized[beam]=arr[beam]
				print(energized)

	result=np.nonzero(energized)[0].shape[0]
	print(f"ANSWER: {result}")


def fire_beam(arr,start_position,dire,is_start_beam=False):
	# print(f"*** FIRING BEAM from {start_position} towards {DIRE[dire][NAME]}")
	hits=([],[])
	dire_vec=DIRE[dire][VECTOR]
	position=start_position+dire_vec
	# print(f"*** POS: {position}, value: {arr[tuple(position)]}")

	while 0<=position[ROW]<arr.shape[ROW] and 0<=position[COL]<arr.shape[COL]:
		hits[ROW].append(position[ROW])
		hits[COL].append(position[COL])
		if arr[tuple(position)]!=EM:
			break
		else:
			position=position+dire_vec
			# print(f"*** POS: {position}, value: {arr[tuple(position)]}")

	# print(f"*** resulting hits: {hits}")
	return hits






main()
