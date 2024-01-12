try:
	import datetime
	import pathlib
	import os
	from aocd.models import Puzzle
	import sys
	import traceback
	import shlex
	from enum import Enum

	import base64
	from cryptography.fernet import Fernet
except Exception:
	traceback.print_exc()
	input(f"Some import error happened. Press any key to continue.")
	exit()

NL="\n"
BOILERPLATE=("""
import numpy as np
import sys
def main():
	with open(sys.argv[1]) as f:
		inp=f.read().split("\\n")
	result=0

	print(f"ANSWER: {result}")
main()
""")

ROOT_PATH=pathlib.Path(__file__).parent

ENCR_SUFFIX="encrypted"
INPUT_SUFFIX="input"

def GET_PASSWORD():
	with open((ROOT_PATH/"password.secret").resolve(),"rb") as file:
		password=file.read()
	password=base64.urlsafe_b64encode(password)
	return password

def GET_SESSION_ID():
	with open((ROOT_PATH/"session-id.secret").resolve(),"r") as f:
		session_id=f.read()
	return session_id




class Ui:
	def __init__(self):
		self.queue=sys.argv[1:]
		self.mgr=None
		self.act={
			Ui.Cmd.none:lambda:None,
			Ui.Cmd.dirs:lambda:self.mgr.make_dirs(),
			Ui.Cmd.boilerplate:lambda:self.mgr.write_boilerplate(),
			Ui.Cmd.download:lambda:self.mgr.download_data(),
			Ui.Cmd.encrypt:lambda:self.mgr.encrypt_data(),
			Ui.Cmd.decrypt:lambda:self.mgr.decrypt_data(),
			Ui.Cmd.setDryRun:lambda:self.mgr.set_dry_run(),
			Ui.Cmd.exit:lambda:None,
		}

	def get_input(self,msg,as_int=False):
		from_queue=len(self.queue)!=0
		if not from_queue:
			inp=input(msg)
			self.queue=shlex.split(inp)
			if len(self.queue)==0:
				self.queue=[""]
		result=self.queue.pop(0)
		if as_int:
			result=int(result)
		return result,from_queue

	def start(self):

		year,from_queue=self.get_input("year: ",True)
		if from_queue:
			print(year)
		day,from_queue=self.get_input("day: ",True)
		if from_queue:
			print(day)
		self.mgr=AocManager(year,day)

		cmd=Ui.Cmd.none
		while not cmd==Ui.Cmd.exit:
			try:
				cmd=Ui.Cmd(self.get_input(" ")[0])
				self.act[cmd]()
			except Exception as exc:
				print(exc)


	class Cmd(Enum):
		none=""
		dirs="dirs"
		boilerplate="bp"
		download="dl"
		encrypt="enc"
		decrypt="dec"
		setDryRun="dry"
		exit="x"

class AocManager:
	def __init__(self,year,day):
		self.dry_run=False
		self.year=year
		self.day=day
		self.dir_path=ROOT_PATH/str(self.year)/f"{self.day:02d}"



	def make_dirs(self):
		dir_path=self.dir_path.resolve()
		print(f"AocManager: Making directory: \"{dir_path}\".")
		if not self.dry_run:
			os.makedirs(dir_path,exist_ok=True)

	def write_boilerplate(self):
		print(f"AocManager: Writing boilerplate.")
		files_to_write=[]
		for i in range(2):
			file_path=(self.dir_path/f"{i+1}.py").resolve()
			files_to_write.append((file_path,BOILERPLATE))
		self.write_files(files_to_write)

	def download_data(self):
		session_id=GET_SESSION_ID()
		os.environ["AOC_SESSION"]=session_id
		print(f"AocManager: Download data with session-id \"{session_id}\".")
		if not self.dry_run:
			puzzle=Puzzle(year=self.year,day=self.day)

			files_to_write=[]
			inp=puzzle.input_data
			files_to_write.append(((dir_path/f"data.{INPUT_SUFFIX}").resolve(),inp))

			for idx,example in enumerate(puzzle.examples):
				path=(dir_path/f"example{idx+1}.{INPUT_SUFFIX}").resolve()
				files_to_write.append((path,example.input_data))

			self.write_files(files_to_write)

	def encrypt_data(self):
		engine=Fernet(GET_PASSWORD())
		dir_path=self.dir_path.resolve()
		input_files=self.dir_path.glob(f"*.{INPUT_SUFFIX}")
		for old_file_path in input_files:
			new_file_path=f"{old_file_path}.{ENCR_SUFFIX}"
			print(f"AocManager: Encrypt \"{old_file_path}\" to \"{new_file_path}\".")
			if not self.dry_run:
				with open(old_file_path,"rb") as file:
					original=file.read()
				with open(new_file_path,"wb") as file:
					file.write(engine.encrypt(original))

	def decrypt_data(self):
		engine=Fernet(GET_PASSWORD())
		dir_path=self.dir_path.resolve()
		input_files=self.dir_path.glob(f"*.{ENCR_SUFFIX}")
		for old_file_path in input_files:
			new_file_path=old_file_path.resolve()
			new_file_path=str(new_file_path)[:-(len(ENCR_SUFFIX)+1)]
			print(f"AocManager: Decrypt \"{old_file_path}\" to \"{new_file_path}\".")
			if not self.dry_run:
				with open(old_file_path,"rb") as file:
					original=file.read()
				with open(new_file_path,"wb") as file:
					file.write(engine.decrypt(original))

	def set_dry_run(self):
		self.dry_run=True


	def write_files(self,files_to_write):
		for file_path,content in files_to_write:
			print(f"AocManager: Writing file \"{file_path}\".")
			if not self.dry_run:
				with open(file_path,"w") as f:
					f.write(content)


Ui().start()
