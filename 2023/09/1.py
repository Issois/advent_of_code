import pandas as pd
import numpy as np

def main():
	inp=pd.read_csv("input",sep=" ",header=None,index_col=False)
	inp=np.array(inp)

	result=inp[:,-1]

	while np.any(inp):
		inp=inp[:,1:]-inp[:,:-1]
		result+=inp[:,-1]
	print(np.sum(result))


main()