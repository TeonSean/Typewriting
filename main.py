import sys
import translator

def file_input():
	in_fname=sys.argv[1]
	out_fname=sys.argv[2]
	with open(in_fname, 'r') as fin:
		with open(out_fname, 'w') as fout:
			line=fin.readline()
			while line:
				fout.write(translator.translate(line)+'\n')
				line=fin.readline()

def cmd_input():
	while True:
		string=input("Enter your input: ")
		if string in ['q', 'quit', 'exit']:
			return
		try:
			print(translator.translate(string))
		except ValueError as e:
			print(str(e))
			pass

if len(sys.argv) == 1:
	cmd_input()
elif len(sys.argv) == 3:
	file_input()
else:
	print('Invalid number of arguments given.')
