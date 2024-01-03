
import sys
import hjson
def main():

	with open("example1" if "e" in sys.argv else "input") as f:
		inp=f.read().replace("=",":").split("\n")
	result=0
	parsing_rules=True
	workflows={}
	items=[]
	for line in inp:
		if len(line)==0:
			parsing_rules=False
			continue
		if parsing_rules:
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
		else:
			items.append(hjson.loads(line))
			# print(items[-1])
	# return


	for item in items:
		current_wf="in"
		processed=False
		while not processed:
			# print(f"{item=},{current_wf=}")
			for rule_content,rule_fun in workflows[current_wf]:
				current_wf=rule_fun(item)
				# print(f"{rule_content} <{current_wf}>")
				if current_wf is None:
					pass
				elif current_wf=="A":
					# print("ACCEPTED")
					result+=sum([val for val in item.values()])
					processed=True
					break
				elif current_wf=="R":
					# print("REJECTED")
					processed=True
					break
				else:
					break
		# break



	print(f"ANSWER: {result}")


def make_final_rule(target):
	return lambda item:target

def make_rule(prop,comp_is_greater,num,target):
	if comp_is_greater:
		return lambda item:target if item[prop]>num else None
	else:
		return lambda item:target if item[prop]<num else None



main()
