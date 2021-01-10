import recognition
import os
import shutil
from threading import Thread


def open_file(file):
    with open(file, 'r') as f:
    	read_file = f.read()
    return read_file

def combine_txt(txt_dir):
	num_files = len(os.listdir(txt_dir))
	out_file = os.path.join(txt_dir, 'out.txt')
	with open(out_file, 'a') as f:
		for i in range(num_files):
			file = os.path.join(txt_dir, f'{i}.txt')
			txt = open_file(file)
			f.write(txt)

if __name__ == "__main__":
	txt_dir = 'txt'
	recognition.run()

	if os.path.isdir(txt_dir):
		print('COMBINING')
		combine_txt(txt_dir)