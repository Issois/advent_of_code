
import base64

import sys
from cryptography.fernet import Fernet


ENCRYPT="e"
DECRYPT="d"

def main():
	_,mode,file_path=sys.argv
	encr_suffix=".encrypted"
	with open("password","rb") as file:
		password=file.read()

	password=base64.urlsafe_b64encode(password)

	fernet=Fernet(password)

	if mode==ENCRYPT:
		with open(file_path,"rb") as file:
			original=file.read()
		with open(file_path+encr_suffix,"wb") as file:
			file.write(fernet.encrypt(original))
	elif mode==DECRYPT:
		with open(file_path,"rb") as file:
			original=file.read()
		with open(file_path[:-len(encr_suffix)],"wb") as file:
			file.write(fernet.decrypt(original))


main()