import matplotlib.pyplot as plt
import numpy as np
import sys
from queue import Queue
import networkx as nx

HI=1
LO=0

SRC=0
TGT=1
SIG=2


BR=0
FL=1
CO=2
FI=3

MOD_NAME={
	BR:" ",
	FL:"%",
	CO:">",
	FI:"#",
}

class Module:
	NEXT_ID=0
	def __init__(self,line):
		self.name,out_list=line.split(" -> ")
		self.inp=[]
		self.out=[]
		self.output_names=out_list.split(", ")
		if len(out_list)==0:
			self.output_names=[]
		self.kind=None
		self.id=Module.NEXT_ID
		Module.NEXT_ID+=1
		self.print_signal=False
		self.on_signal=lambda src,dst,sig:None

	def initialize(self):
		pass

	def link(self,module_from_name):
		for output_name in self.output_names:
			if output_name not in module_from_name:
				print(f" Output of {self.name} \"{output_name}\" is not a valid module.")
				mod=Module(f"{output_name} -> ")
			else:
				mod=module_from_name[output_name]
			self.out.append(mod)
			mod.inp.append(self)

	def signal(self,queue,sig):
		queue.pop()

		for mod in self.out:
			self.on_signal(self,mod,sig)
			queue.push((self,mod,sig))

	def gen(line):
		return GEN[line[0]](line[1:])

	def __repr__(self):return str(self)
	def __str__(self):
		return f"{self.name:2}/{self.id:2} {MOD_NAME[self.kind]} from [{mod_list_str(self.inp):35}] to [{mod_list_str(self.out):35}]"


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
		src,dst,sig=queue.peek()
		prev_state=self.states[src.name]
		self.states[src.name]=sig

		# if self.name=="gf":
			# print(src.name,dst.name,sig)
			# print(self.states)

		if prev_state!=sig:
			if sig==HI:
				self.hi_count+=1
			else:
				self.hi_count-=1

		new_signal=LO if self.hi_count==len(self.states) else HI

		# if self.name=="gf":
			# print(f"gf was signaled {sig} from {src.name} and now signals {new_signal} (hc: {self.hi_count}).")

		super(Conjunction,self).signal(queue,new_signal)

class Broadcast(Module):
	def __init__(self,line):
		super(Broadcast,self).__init__(line)
		self.kind=BR
	def signal(self,queue):
		super(Broadcast,self).signal(queue,queue.peek()[2])

class Final(Module):
	def __init__(self,line):
		super(Final,self).__init__(line)
		self.kind=FI

	def signal(self,queue):
		_,_,sig=queue.peek()
		if sig==LO:
			print("FINAL received LO signal.")
			queue.q.clear()

		super(Final,self).signal(queue,sig)






def mod_list_str(modules):
	return ",".join([m.name for m in modules])

GEN={
	"b":Broadcast,
	"%":FlipFlop,
	"&":Conjunction,
	"#":Final

}

class SignalQueue:
	def __init__(self):
		self.q=Queue()
		# self.pulse_count={LO:0,HI:0}
	def push(self,elem):
		# self.pulse_count[elem[SIG]]+=1
		self.q.put(elem)
	def pop(self):
		return self.q.get()
	def peek(self):
		return self.q.queue[0]
	def empty(self):
		return self.q.empty()
	def run(self):
		while not self.empty():
			_,mod,sig=self.peek()
			# print("QUEUE: "+str(self))
			mod.signal(self)
	def __str__(self):
		return "  ".join([f"{src.name if src is not None else '  '}:{dst.name if dst is not None else '  '}:{sig}" for src,dst,sig in self.q.queue])

def main():
	start_module_name="__"
	with open("custom_example1.input" if "e" in sys.argv else "data.input") as f:
		inp=f.read().replace("broadcaster","b"+start_module_name).split("\n")
		if not "e" in sys.argv:
			inp+=["#rx -> "]
	# start_signals=inp[0].split(" -> ")[1].split(", ")

	mfn={}
	for line in inp:
		mod=Module.gen(line)
		mfn[mod.name]=mod

	# mod=Module()

	for mod in mfn.values():
		mod.link(mfn)

	for mod in mfn.values():
		mod.initialize()
		print(mod)


	# dof=0

	# for mod in mfn.values():
	# 	if mod.kind==FL:
	# 		dof+=1
	# 	elif mod.kind==CO:
	# 		for imod in mod.inp:
	# 			if imod.kind!=FL:
	# 				dof+=1

	# print(f"Number of states: {dof}")

	# graph=nx.DiGraph()

	# for mod in mfn.values():
	# 	graph.add_node(mod.name,subs=-1)
	# for mod in mfn.values():
	# 	for omod in mod.out:
	# 		graph.add_edge(mod.name,omod.name)

	# find_subsytems(mfn,"__","rx")

# def find_subsytems(mfn,start_nn,end_nn):

	# pass
	# start_node=graph[]

	# graph.nodes[start_node_name]["subs"]=0
	# nn_to_check=[start_node_name]

	# while len(nn_to_check)>0:
	# 	nn=nn_to_check.pop()
	# 	if graph.nodes[nn]["subs"]=-1:



	# # nn=start_node_name
	# print(graph.nodes[nn])
	# print(graph.nodes[nn])

	# while True:



	# nx.draw_networkx(graph,with_labels=True)
	# plt.show()

	def on_signal(src,dst,sig):
		nonlocal found
		if sig==HI:
			found=True
			# print(f" RUN {run_num+1}: {src.name} signals {sig} to {dst.name}")

	mfn["qs"].on_signal=on_signal
	mfn["sv"].on_signal=on_signal
	mfn["pg"].on_signal=on_signal
	mfn["sp"].on_signal=on_signal
	# mfn["gf"].print_signal=True
	# mfn["rx"].print_signal=True

	# # return
	mods=["bx","jq","nv","jp"]



	COUNT=100000
	count_from_mod={}
	for mod in mods:
		print(f"Checking {mod}")
		queue=SignalQueue()
		found=False
		for run_num in range(COUNT):
			queue.push((None,mfn[mod],LO))
			queue.run()
			if found:
				count_from_mod[mod]=run_num+1
				break
	print(count_from_mod)
	result=1
	for val in count_from_mod.values():
		result*=val

		# print(f"{i+1}/{COUNT}")
	# 	# if i%1000==0:
	# 	# print(i)

	# 	# print([f"{mod.name}: {mod.hi_count}/{len(mod.states)}" for mod in mfn.values() if mod.kind==CO])


	# 		# print(mfn["gf"].states)
	# 		# print(mfn["qs"].states)
	# 		# print(mfn["sv"].states)
	# 		# print(mfn["pg"].states)
	# 		# print(mfn["sp"].states)

	# 		# if mod.name=="rx":
	# 			# print(i,sig)
	# 			# break



	# # print(signal_queue)
	# # result=queue.pulse_count[LO]*queue.pulse_count[HI]

	print(f"ANSWER: {result}")



main()
