
import numpy as np
import sys
import matplotlib.pyplot as plt
from pprint import pprint

def solve_1(inp):
	registers,program=inp

	answer=execute_program(registers,program)["output"]
	answer=",".join([str(elem) for elem in answer])

	return answer

def xor7(num):
	return num^7

def digits_to_int(digits,base):
	num=0
	cnt=len(digits)
	for idx in range(cnt):
		num+=digits[idx]*(base**(cnt-(idx+1)))

	return num

def solve_2_test_01(inp):
	registers,program=inp

	for i in range(10000):
		if str(i)[-3:]=="611":
			print(i,i//9)
	return

	input_from_num={}

	# b has n digits:
	# -> max n+1 digits of a have an influence
	#    on last digit of a/b.
	# for i in range(11):
		# print(digits_to_int([1,0,1,0],i))
	# return

	rng=np.random.default_rng()

	count__digits__a=5
	count__digits__b=1
	count__experiments__a=10
	count__digits_relevant=count__digits__b+1

	digits__a_low =list(rng.choice(8,                 count__digits_relevant))
	digits__b     =list(rng.choice(8,count__digits__b))
	for exp_index in range(count__experiments__a):
		digits__a_high=list(rng.choice(8,count__digits__a-count__digits_relevant))
		num__a=digits_to_int([1]+digits__a_high+digits__a_low,8)
		num__b=digits_to_int(digits__b,8)
		num__quot=num__a//num__b

		print(int_to_base(num__a,8),int_to_base(num__b,8),int_to_base(num__quot,8)[-1])


	# print(np.unique(rng.choice(8,200),return_counts=True))
	# return

	# for num_input in range(8**4):
	# 	num_input_8=int_to_base(num_input,8)

	# 	print(b8)

	# num=


def solve_2(inp):
	# registers,program=inp
	solve_2_test_01(inp)



	answer=0
	return answer


digits_str=[str(val) for val in range(10)]+[chr(val) for val in range(ord("a"),ord("z")+1)]
def int_to_base(num,base):
	if num==0:
		return "0"
	if base>36:
		raise ValueError("base<=36")
	digits=[]
	while num>0:
		digits.append(num%base)
		num=num//base
	return "".join([digits_str[digits[idx]] for idx in range(len(digits)-1,-1,-1)])

# def bin_search(target_value,start,end,get_val):
# 	while end-start>0:
# 		index__search=(start+end)//2

# 		if cost>prio_queue[index__search][COST]:
# 			end=index__search
# 		else:
# 			start=index__search+1
# 		# print(start,end,index__search)
# 	prio_queue.insert(start,head)


def execute_program(registers,program,pause=False):
	state={
		"instruction_pointer":0,
		"advance_instruction_pointer":True,
		"output":[],
	}

	while state["instruction_pointer"]<len(program):
		state["advance_instruction_pointer"]=True
		opcode=program[state["instruction_pointer"]]
		operand=program[state["instruction_pointer"]+1]
		instruction=instr_from_opcode[opcode]
		instruction(operand,registers,state)
		if state["advance_instruction_pointer"]:
			state["instruction_pointer"]+=2
		elif exit_on_jump:
			return state
		if pause:
			print(instruction.__name__,operand,registers,state)
			input()

	return state

def resolve_combo_operand(operand,registers):
	return operand if operand<4 else registers[operand-4]

def instr__adv(operand,registers,state):
	registers[A]=registers[A]//(2**resolve_combo_operand(operand,registers))

def instr__bxl(operand,registers,state):
	registers[B]=registers[B]^operand

def instr__bst(operand,registers,state):
	registers[B]=resolve_combo_operand(operand,registers)%8

def instr__jnz(operand,registers,state):
	if registers[A]!=0:
		state["instruction_pointer"]=operand
		state["advance_instruction_pointer"]=False

def instr__bxc(operand,registers,state):
	registers[B]=registers[B]^registers[C]

def instr__out(operand,registers,state):
	state["output"].append(resolve_combo_operand(operand,registers)%8)

def instr__bdv(operand,registers,state):
	registers[B]=registers[A]//(2**resolve_combo_operand(operand,registers))

def instr__cdv(operand,registers,state):
	registers[C]=registers[A]//(2**resolve_combo_operand(operand,registers))

instr_from_opcode=[
	instr__adv,
	instr__bxl,
	instr__bst,
	instr__jnz,
	instr__bxc,
	instr__out,
	instr__bdv,
	instr__cdv,
]

def get_input(file_path):
	with open(file_path) as f:
		inp=f.read().split("\n\n")

	regs=[]
	for line in inp[0].split("\n"):
		regs.append(int(line.split(" ")[-1]))

	prog=[int(val) for val in inp[1].split(" ")[1].split(",")]

	return regs,prog


def main():
	inp=get_input(FILE_PATH)
	answer=solve(inp)
	print(f"ANSWER: {answer}")



A=0
B=1
C=2

RIDDLE_NUMBER=sys.argv[1]
FILE_PATH=sys.argv[2]

X=0
Y=1
Z=2

ROW=0
COL=1

DIREV=np.array([
	[-1, 0],
	[-1, 1],
	[ 0, 1],
	[ 1, 1],
	[ 1, 0],
	[ 1,-1],
	[ 0,-1],
	[-1,-1],
])

def is_in_range(pos,arr):
	return (
		0<=pos[X]<arr.shape[X]
		and
		0<=pos[Y]<arr.shape[Y]
	)

solve=getattr(sys.modules[__name__],"solve_"+RIDDLE_NUMBER)
main()


	# for index_instr in range(0,len(program),2):
	# 	print(instr_from_opcode[program[index_instr]].__name__,program[index_instr+1])
	# def get_len(reg_a):
	# 	registers=[a,0,0]
	# 	return len(execute_program(registers,program)["output"])
	# print(ord("a"),ord("z"))

	# 2,4,1
	# 2,4,1,7,7,5,0,3,4,0,1,7,5,5,3,0
	# for output in program[::-1]:
	# 	val=output
	# 	print(val)
	# 	val=xor7(val)
	# 	print(val)

		# return


	# convert={}

	# return
	# a=1000
	# for a in range(8):
		# print(a,int_to_base(a,8))
		# continue
		# print(int_to_base(a,base=8))
		# answer=execute_program(registers,program,True)["output"]
	# 	result=execute_program([a,0,0],program,False)["output"]
	# 	convert[str(a)]=result[0]
	# # print(convert)
	# 	# result="".join([str(elem) for elem in result[::-1]])

	# 	# print(int_to_base(a,base=8),result)
	# # for a in range(101):
	# # 	print(a,int_to_base(a,base=8))
	# div=2
	# comb={}
	# le=2
	# for a in range(1_000_000,10_000_000):
	# 	# print(a,int_to_base(a,base=8),a//4,int_to_base(a//4,base=8))
	# 	# inpu=int_to_base(a,base=8)[-le:]
	# 	inpu=int_to_base((a*(8**5)+1),base=8)
	# 	# outp=int_to_base(a//div,base=8)[-1]
	# 	outp=int_to_base((a*(8**5)+1)//div,base=8)
	# 	print(outp)
		# if inpu not in comb:
			# comb[inpu]=[]
		# comb[inpu].append(outp)
		# print(,)
	# pprint(comb)
		# a=100
		# result=execute_program([a,0,0],program,True)["output"][::-1]
		# base8=list(int_to_base(a,base=8))
		# converted=[convert[_] for _ in base8]
		# print(converted,result)

	# len__target=len(program)
	# for a in range(1000):
	# a=100
	# while get_len(a)<len__target:
	# 	a*=10

	# print(a)
	# max_lower_bound=a/10
	# max_upper_bound=a*10

	# lower_bound=max_lower_bound
	# upper_bound=max_upper_bound




# 10000000000000
	# execute_program(registers,program,pause=True)