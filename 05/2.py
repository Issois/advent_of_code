
from pprint import pprint

class Rng:
	def __init__(self,start,length=None,stop=None):
		self.start=start
		self.length=length
		if stop is not None:
			self.length=stop-self.start

		self.offset=None
		self.pr_offs=False

	def __repr__(self):
		return str(self)

	def __str__(self):
		if self.pr_offs and self.offset is not None:
			return f"{self.start}~{self.length} {self.offset:+d}"
		else:
			return f"{self.start}~{self.length}"

	def stop(self):
		return self.start+self.length
	def last(self):
		return self.start+self.length-1

	# def __contains__(self,val):
	# 	return self.start<=val<self.start+self.length:

	# def is_strict_inside(self,val):
	# 	return self.start<=val<self.start+self.length:

	def from_str(text):
		return Rng(*[int(x) for x in text.split("~")])

	def split_by(self,other):
		pre=None
		ins=None
		pos=None
		if self.start<other.start:
			if self.last()<other.start:
				print("-  N: self completely left of other.")
				pre=self
			else:
				pre=Rng(self.start,stop=other.start)
				if self.last()>other.last():
					print("-  T: self completely encompassing other.")
					ins=other
					pos=Rng(other.stop(),stop=self.stop())
				else:
					print("-  R: self overlapping other from the right.")
					ins=Rng(other.start,stop=self.stop())
					ins.offset=other.offset
		else:
			print("- NOT IMPLEMENTED")


		return [x for x in [pre,ins,pos] if x is not None]



def main():

	if TEST(True):
		return

	with open("input") as f:
		inp=f.read()

	paras=inp.split("\n\n")

	seeds=[int(x) for x in paras[0].split(": ")[1].split(" ")]
	rngs=[Rng(seeds[i],seeds[i+1]) for i in range(0,len(seeds),2)]

	# for rng in rngs:
		# print(rng)

	# print(len(seeds))
	# return

	order=[
		"seed",
		"soil",
		"fertilizer",
		"water",
		"light",
		"temperature",
		"humidity",
	]

	rules={}

	for para in paras[1:]:
		lines=para.split("\n")
		header=lines[0].split("-")[0]
		rules[header]=[]
		for line in lines[1:]:
			arr=[int(x) for x in line.split(" ")]
			rule=Rng(arr[1],arr[2])
			rule.offset=arr[0]-arr[1]
			rules[header].append(rule)

	for h,rs in rules.items():
		print(f"- {h}")
		for r in rs:
			print(f" - {r}")


def TEST(test):
	if  test:
		test_rng()

	return test

def test_rng():
	cases=[
		["3~4","1~2",            "3~4"],
		["3~4","1~3",      "3~1","4~3"],
		["3~4","1~4",      "3~2","5~2"],
		["3~4","1~5",      "3~3","6~1"],
		["3~4","1~6",      "3~4"      ],
		["3~4","1~7",      "3~4"      ],
		["3~4","1~8",      "3~4"      ],
		["3~4","2~8",      "3~4"      ],
		["3~4","3~8",      "3~4"      ],
		["3~4","4~8","3~1","4~3"      ],
		["3~4","5~8","3~2","5~2"      ],
		["3~4","6~8","3~3","6~1"      ],
		["3~4","7~8","3~4"            ],
		["3~4","4~2","3~1","4~2","6~1"],
	]
	for idx,case in enumerate(cases):

		rng=Rng.from_str(case[0])
		rule=Rng.from_str(case[1])

		# print(f"{idx+1=},{rng=},{rule=}")

		res=rng.split_by(rule)

		res=[str(x) for x in res]

		success=True
		for a,b in zip(case[2:],res):
			if a!=b:
				success=False
		if not success:
			print(f" case {idx+1}/{len(cases)} ({case}) failed, result: {res}")
		# else:
		# 	print(f" case {idx+1}/{len(cases)} ({case}) succeeded, result: {res}")


main()
