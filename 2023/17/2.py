
import numpy as np
import sys
def main():
	with open("example1" if "e" in sys.argv else "input") as f:
		inp=f.read().split("\n")
	result=0

	print(f"ANSWER: {result}")
main()
