#提供拼音、汉字与int类型id的转换，以及拼音与汉字的对应关系查询

ch2idx=dict()
idx2ch=list()
ch2py=list()
py2ch=list()
py2idx=dict()
idx2py=list()

with open('data\\ch.txt') as fp:
	idx2ch=list(fp.read())
	for i,ch in enumerate(idx2ch):
		ch2idx[ch]=i
		ch2py.append(list())

with open('data\\py-ch.txt') as fp:
	for i, line in enumerate(fp.readlines()):
		line=line.strip().split(' ')
		py2idx[line[0]] = i
		idx2py.append(line[0])
		py2ch.append(list())
		for ch in line[1:]:
			py2ch[i].append(ch2idx[ch])
			ch2py[ch2idx[ch]].append(i)

correction={'lve':'lue', 'nve':'nue', 'fenɡ':'feng', 'bia':'bian', 'puo':'po', \
			'yie':'ye', 'piang':'pian', 'we':'wei', 'jion':'jiang', 'xhao':'shao', \
			'tia':'tiao', 'ng':'en', 'sho':'shou', 'n':'en', 'f':'feng', 'm':'fu'}

def idx_of_py(py, ch):
	if py in py2idx:
		return py2idx[py]
	else:
		try:
			return py2idx[correction[py]]
		except KeyError as e:
			print('\n\n'+py+'   '+ch+'\n\n')
			return None

def input2array(input):
	input=input.strip().split(' ')
	for i in range(len(input)):
		input[i]=py2idx[input[i]]
	return input

def array2output(output):
	for i in range(len(output)):
		output[i]=idx2ch[output[i]]
	return ''.join(output)
