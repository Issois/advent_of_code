
import numpy as np
import sys
import re
def main():
	with open(sys.argv[2]) as f:
		inp=f.read()
	solve=[solve_1,solve_2]
	solve=solve[int(sys.argv[1])-1]

	print(f"ANSWER: {solve(inp)}")

def solve_1(inp):
	result=0
	for mtc in re.finditer(r'mul\((\d\d?\d?),(\d\d?\d?)\)',inp):
		a,b=mtc.groups()
		result+=int(a)*int(b)



	return result

def solve_2(inp):
	result=0
	en=True
	for mtc in re.finditer(r'(mul\((\d\d?\d?),(\d\d?\d?)\))|(do\(\))|(don\'t\(\))',inp):
		grp=mtc.groups()
		if grp[0] is None:
			if grp[3] is not None:
				en=True
			if grp[4] is not None:
				en=False
		else:
			if en:
				a,b=grp[1:3]
				result+=int(a)*int(b)

		print(mtc.groups())
	return result
main()
