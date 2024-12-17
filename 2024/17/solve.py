
import numpy as np
import sys
# import matplotlib.pyplot as plt


def solve_1(inp):
	registers,program=inp

	answer=execute_program(registers,program)["output"]
	answer=",".join([str(elem) for elem in answer])

	return answer

def solve_2(inp):
	registers,program=inp

	for index_instr in range(0,len(program),2):
		print(instr_from_opcode[program[index_instr]].__name__,program[index_instr+1])


	answer=0
	return answer

def execute_program(registers,program):
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
		print(instruction.__name__,operand,registers,state)
		instruction(operand,registers,state)
		if state["advance_instruction_pointer"]:
			state["instruction_pointer"]+=2

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
