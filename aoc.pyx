
import datetime
import pathlib
import os
import urllib.request
from aocd import get_data

def main():


	FILE_COUNT=2

	current_year=datetime.datetime.now().year
	year=input(f"Year (leave empty for {current_year}): ")
	# year="2023"

	if len(year)==0:
		year=str(current_year)

	day=int(input("day: "))
	# day="7"
	day_padded=f"{day:02d}"

	root_path=pathlib.Path(__file__).parent
	dir_path=root_path/year/day_padded

	os.makedirs(dir_path.resolve(),exist_ok=True)



	boilerplate="def main():\n\twith open(\"input\") as f:\n\t\tinp=f.readlines()\n\nmain()"

	for i in range(FILE_COUNT):
		file_path=dir_path/f"{i+1}.py"
		if not file_path.is_file():
			with open(file_path.resolve(),"w") as f:
				f.write(boilerplate)

	with open((root_path/"session-id").resolve(),"r") as f:
		session_id=f.read()

	os.environ["AOC_SESSION"]=session_id
	data=get_data(day=day,year=year)


	with open((dir_path/"input").resolve(),"w") as f:
		f.write(data)



try:
	main()
except Exception as exc:
	input(f"Some error happened: {exc}")