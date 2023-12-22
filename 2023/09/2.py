import pandas as pd
import numpy as np

def main():
	inp=pd.read_csv("input",sep=" ",header=None,index_col=False)
	inp=np.array(inp)

	# result=inp[:,0]
	first_cols=[inp[:,0]]

	while np.any(inp):
		inp=inp[:,1:]-inp[:,:-1]
		first_cols.append(inp[:,0])

	result=np.zeros(first_cols[0].shape)
	first_cols=first_cols[::-1]
	for first_col in first_cols:
		result=first_col-result

	print(np.sum(result))


main()