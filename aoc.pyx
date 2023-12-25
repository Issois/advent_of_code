

def main():


	FILE_COUNT=2

	current_year=datetime.datetime.now().year
	if len(sys.argv)>1:
		year=sys.argv[1]
	else:
		year=input(f"Year (leave empty for {current_year}): ")
	# year="2023"

	if len(year)==0:
		year=current_year
	else:
		year=int(year)

	if len(sys.argv)>2:
		day=sys.argv[2]
	else:
		day=input("day: ")
	# day="7"
	day=int(day)
	day_padded=f"{day:02d}"

	root_path=pathlib.Path(__file__).parent
	dir_path=root_path/str(year)/day_padded

	dirs_to_make=[dir_path.resolve()]
	files_to_write=[]


	# print(dict(6))

	# return


	boilerplate="def main():\n\twith open(\"input\") as f:\n\t\tinp=f.read().split(\"\\n\")\n\nmain()"

	for i in range(FILE_COUNT):
		file_path=dir_path/f"{i+1}.py"
		files_to_write.append((file_path,boilerplate))

	with open((root_path/"session-id").resolve(),"r") as f:
		session_id=f.read()

	os.environ["AOC_SESSION"]=session_id
	# data=get_data(day=day,year=year)

	puzzle=Puzzle(year=year,day=day)

	# attrs=dir(puzzle)
	# for attr in attrs:
		# if attr[0]!="_":
			# print(f"{attr}:{getattr(puzzle,attr)}")
	# return

	inp=puzzle.input_data
	files_to_write.append(((dir_path/"input").resolve(),inp))

	for idx,example in enumerate(puzzle.examples):
		path=(dir_path/f"example{idx+1}_{example.answer_a}").resolve()
		files_to_write.append((path,example.input_data))


	# with open(,"w") as f:
		# f.write(data)


	# if False:
	if True:
		for dtm in dirs_to_make:
			os.makedirs(dtm,exist_ok=True)
		for file_path,content in files_to_write:
			if not file_path.is_file():
				with open(file_path.resolve(),"w") as f:
					f.write(content)
		puzzle.view()
	else:
		for dtm in dirs_to_make:
			print(f"Directory: {dtm}")
		for file_path,content in files_to_write:
			print(f"Path: {file_path}\nContent:<{content.split(NL)[0]}>")
NL="\n"
try:

	import datetime
	import pathlib
	import os
	import urllib.request
	# from aocd import get_data
	from aocd.models import Puzzle
	import sys
	import traceback

	main()
	# except Exception as exc:
except Exception:
	traceback.print_exc()
	input(f"Some error happened. Press any key to continue.")