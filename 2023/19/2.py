
import sys
import hjson


TARGET=0
RULE_IDX=1
DICT=2

def main():

	with open("example1.input" if "e" in sys.argv else "data.input") as f:
		inp=f.read().split("\n")
	result=0
	workflows={}

	items=[["in",0,{
		"x":(1,4000),
		"m":(1,4000),
		"a":(1,4000),
		"s":(1,4000),
	}]]


	for line in inp:
		if len(line)==0:
			break
		wf_name,rules=line.split("{")
		rules=rules[:-1].split(",")
		final_target=rules[-1]
		workflows[wf_name]=[]
		for rule in rules[:-1]:
			prop=rule[0]
			comp=rule[1]
			num,target=rule[2:].split(":")
			num=int(num)

			workflows[wf_name].append((rule,make_rule(prop,comp==">",num,target)))
		workflows[wf_name].append((f"final {final_target}",make_final_rule(final_target)))


	while len(items)>0:
		item=items.pop()
		rule_name,rule_fun=workflows[item[TARGET]][item[RULE_IDX]]
		print(item)
		new_items=rule_fun(item)
		while len(new_items)>0:
			new_item=new_items.pop()
			# print(new_item)
			if new_item[TARGET]=="A":
				count=1
				for prop,rng in new_item[DICT].items():
					count*=(rng[1]-rng[0]+1)
				result+=count
			elif new_item[TARGET]=="R":
				pass
			else:
				items.append(new_item)


	print(f"ANSWER: {result}")


def make_final_rule(target):
	return lambda item:[[target,0,item[DICT].copy()]]

def make_rule(prop,comp_is_greater,num,target):
	if comp_is_greater:
		def calc(item):
			results=[]
			target_range=item[DICT][prop]
			if num<target_range[0]:
				results.append([target      ,0               ,item[DICT].copy()])
				pass
			elif num<target_range[1]:
				lower=item[DICT].copy()
				upper=item[DICT].copy()
				lower[prop]=item[DICT][prop][0],num
				upper[prop]=num+1,item[DICT][prop][1]
				results.append([item[TARGET],item[RULE_IDX]+1,lower])
				results.append([target      ,0               ,upper])
			else:
				results.append((item[TARGET].item[RULE_IDX]+1,item[DICT].copy()))
			return results
	else:
		def calc(item):
			results=[]
			target_range=item[DICT][prop]
			if num>target_range[1]:
				results.append([target      ,0               ,item[DICT].copy()])
				pass
			elif num>target_range[0]:
				lower=item[DICT].copy()
				upper=item[DICT].copy()
				lower[prop]=item[DICT][prop][0],num-1
				upper[prop]=num,item[DICT][prop][1]
				results.append([target      ,0               ,lower])
				results.append([item[TARGET],item[RULE_IDX]+1,upper])
			else:
				results.append((item[TARGET].item[RULE_IDX]+1,item[DICT].copy()))
			return results
	return calc

main()
