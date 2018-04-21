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

def test_input():
	in_fname=sys.argv[1]
	out_fname=sys.argv[2]
	re_fname=sys.argv[3]
	output=list()
	with open(in_fname, 'r') as fin:
		lines=fin.readlines()
	for idx,line in enumerate(lines):
		print('translating %dth sentence.'%idx)
		output.append(translator.translate(line)+'\n')
	total_st = len(output)
	correct_st = 0
	total_ch = 0
	correct_ch = 0
	with open(re_fname, 'r') as fre:
		result=fre.readlines()
	for out, re in zip(output, result):
		if out.strip() == re.strip():
			correct_st+=1
			total_ch+=len(out)-1
			correct_ch+=len(out)-1
		else:
			total_ch+=len(out)-1
			for i in range(len(out)-1):
				if out[i]==re[i]:
					correct_ch+=1
	with open(out_fname, 'w') as fout:
		fout.writelines(output)
	print('Sentence accuracy: %d/%d = %f'%(correct_st, total_st, correct_st/total_st))
	print('Character accuracy: %d/%d = %f'%(correct_ch, total_ch, correct_ch/total_ch))

if len(sys.argv) == 1:
	cmd_input()
elif len(sys.argv) == 3:
	file_input()
elif len(sys.argv) == 4:
	test_input()
else:
	print('Invalid number of arguments given.')
