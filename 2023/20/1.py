
import numpy as np
import sys
from queue import Queue

HI=1
LO=0

SRC=0
TGT=1
SIG=2

BR=0
FL=1
CO=2

MOD_NAME={
	BR:"casts",
	FL:"flips",
	CO:"conjs",
}

class Module:
	def __init__(self,line):
		self.name,out_list=line.split(" -> ")
		self.inp=[]
		self.out=[]
		self.output_names=out_list.split(", ")
		self.kind=None

	def initialize(self):
		pass

	def link(self,module_from_name):
		for output_name in self.output_names:
			if output_name not in module_from_name:
				print(f" Output of {self.name} \"{output_name}\" is not a valid module.")
				mod=Module(f"b{output_name} -> ")
			else:
				mod=module_from_name[output_name]
			self.out.append(mod)
			mod.inp.append(self)

	def signal(self,queue,new_signal=None):
		_,_,sig=queue.pop()
		if new_signal is not None:
			sig=new_signal
		# print(f" Module {self.name} signals {sig} to ",end="")
		for mod in self.out:
			# print(f"{mod.name} ",end="")
			queue.push((self,mod,sig))
		# print()

	def gen(line):
		return GEN[line[0]](line[1:])

	def __repr__(self):return str(self)
	def __str__(self):
		return f"{self.name:3} {MOD_NAME[self.kind]} from [{mod_list_str(self.inp):15}] to [{mod_list_str(self.out):15}]"


class FlipFlop(Module):
	def __init__(self,line):
		super(FlipFlop,self).__init__(line)
		self.kind=FL

	def initialize(self):
		self.state=LO

	def signal(self,queue):
		_,_,sig=queue.peek()
		if sig==LO:
			self.state=HI-self.state
			new_signal=self.state
			super(FlipFlop,self).signal(queue,new_signal)
		else:
			queue.pop()


class Conjunction(Module):
	def __init__(self,line):
		super(Conjunction,self).__init__(line)
		self.kind=CO

	def initialize(self):
		self.states={mod.name:LO for mod in self.inp}
		self.hi_count=0

	def signal(self,queue):
		src,_,sig=queue.peek()

		prev_state=self.states[src.name]
		self.states[src.name]=sig

		if prev_state!=sig:
			if sig==HI:
				self.hi_count+=1
			else:
				self.hi_count-=1

		new_signal=LO if self.hi_count==len(self.states) else HI
		super(Conjunction,self).signal(queue,new_signal)

class Broadcast(Module):
	def __init__(self,line):
		super(Broadcast,self).__init__(line)
		self.kind=BR


def mod_list_str(modules):
	return ",".join([m.name for m in modules])

GEN={
	"b":Broadcast,
	"%":FlipFlop,
	"&":Conjunction,
}

class SignalQueue:
	def __init__(self):
		self.q=Queue()
		self.pulse_count={LO:0,HI:0}
	def push(self,elem):
		self.pulse_count[elem[SIG]]+=1
		self.q.put(elem)
	def pop(self):
		return self.q.get()
	def peek(self):
		return self.q.queue[0]
	def empty(self):
		return self.q.empty()


def main():
	start_module_name="__"
	with open("example1.input" if "e" in sys.argv else "data.input") as f:
		inp=f.read().replace("broadcaster","b"+start_module_name).split("\n")
	# start_signals=inp[0].split(" -> ")[1].split(", ")

	mfn={}
	for line in inp:
		mod=Module.gen(line)
		mfn[mod.name]=mod

	for mod in mfn.values():
		mod.link(mfn)

	for mod in mfn.values():
		mod.initialize()


	queue=SignalQueue()

	for i in range(1000):
		print(i)
		queue.push((None,mfn[start_module_name],LO))
		while not queue.empty():
			queue.peek()[TGT].signal(queue)



	# print(signal_queue)
	result=queue.pulse_count[LO]*queue.pulse_count[HI]

	print(f"ANSWER: {result}")
main()
