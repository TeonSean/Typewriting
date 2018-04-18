import json
import sys
import util
import _thread
import threading
import pickle
from pypinyin import lazy_pinyin, Style
from queue import Queue

content=Queue()
read_info=str()
process_info=str()
lock=threading.Lock()

pFirstChar=list()
pLastChar=list()
pCharWithNext=list()
pCharWithPrev=list()

def getNewDict(ch_list):
	re=dict()
	re['sum']=0
	for idx in ch_list:
		re['sum']+=1
		re[idx]=1
	return re

def updateDict(d):
	sum=d['sum']
	del d['sum']
	for k,v in d.items():
		d[k]=math.log(v/sum)

def init():
	global pFirstChar, pOccur, pCharWithNext, pCharWithPrev
	for ch_list in util.py2ch:
		pFirstChar.append(getNewDict(ch_list))
		pLastChar.append(getNewDict(ch_list))
	for i in range(len(util.py2idx)):
		pCharWithNext.append(list())
		pCharWithPrev.append(list())
		for j in range(len(util.py2idx)):
			pCharWithNext[i].append(getNewDict(util.py2ch[i]))
		for j in range(len(util.ch2idx)):
			pCharWithPrev[i].append(getNewDict(util.py2ch[i]))

def calculate():
	global pFirstChar, pLastChar, pCharWithNext, pCharWithPrev
	print('Calculating pFirstChar...')
	for d in pFirstChar:
		updateDict(d)
	print('Calculating pOccur...')
	for d in pLastChar:
		updateDict(d)
	print('Calculating pCharWithNext...')
	for l in pCharWithNext:
		for d in l:
			updateDict(d)
	print('Calculating pCharWithPrev...')
	for l in pCharWithPrev:
		for d in l:
			updateDict(d)

def process(content):
	global pFirstChar, pOccur, pCharWithNext, pCharWithPrev
	segment=content.strip().split(' ')
	py_content=list()
	ch_content=list()
	for seg in segment:
		if len(seg) == 0:
			continue
		if seg[0] in util.ch2idx:
			py=util.idx_of_py(lazy_pinyin(seg[0], style=Style.NORMAL)[0])
			ch=util.ch2idx[seg[0]]
			if ch in util.py2ch[py]:
				pFirstChar[py][ch]+=1
				pFirstChar[py]['sum']+=1
		if seg[-1] in util.ch2idx:
			py=util.idx_of_py(lazy_pinyin(seg[-1], style=Style.NORMAL)[0])
			ch=util.ch2idx[seg[-1]]
			if ch in util.py2ch[py]:
				pLastChar[py][ch]+=1
				pLastChar[py]['sum']+=1
		py_seg=lazy_pinyin(seg, style=Style.NORMAL)
		for ch,py in zip(seg,py_seg):
			if ch not in util.ch2idx:
				continue
			py=util.idx_of_py(py)
			ch=util.ch2idx[ch]
			if ch not in util.py2ch[py]:
				continue
			ch_content.append(ch)
			py_content.append(py)
	for i in range(len(ch_content)-1):
		pCharWithNext[py_content[i]][py_content[i+1]][ch_content[i]]+=1
		pCharWithNext[py_content[i]][py_content[i+1]]['sum']+=1
	for i in range(1, len(ch_content)):
		pCharWithPrev[py_content[i]][ch_content[i-1]][ch_content[i]]+=1
		pCharWithPrev[py_content[i]][ch_content[i-1]]['sum']+=1

class processThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global content, read_info, process_info, lock
        while True:
        	lock.acquire()
        	if not content.empty():
        		d=content.get()
        		if d == None:
        			process_info='%7d entries in queue to process' % content.qsize()
        			lock.release()
        			sys.stdout.write('\r%s;%s.' % (read_info, process_info))
        			sys.stdout.flush()
        			break
        		else:
        			process_info='%7d entries in queue to process' % content.qsize()
        			lock.release()
        			sys.stdout.write('\r%s;%s.' % (read_info, process_info))
        			sys.stdout.flush()
        			process(d)
        	else:
        		lock.release()
        print('')

def filterChar(content):
	re = ''
	has_space = False
	for i in range(len(content)):
		uchar = content[i]
		if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
			re = re + uchar
			has_space = False
		elif not has_space:
			re = re + u' '
			has_space = True
	return re

init()
thread1=processThread()
thread1.start()
for i in range(1,16):
	path='data\\jinyong\\%d.txt'%i
	with open(path, 'r') as fp:
		lock.acquire()
		lines=fp.readlines()
		lock.release()
		for j,line in enumerate(lines):
			entry=filterChar(line)
			lock.acquire()
			content.put(entry)
			read_info='Reading %s: %5d/%5d' % (path, j + 1, len(lines))
			lock.release()
			sys.stdout.write('\r%s;%s.' % (read_info, process_info))
			sys.stdout.flush()
for i in range(1,12):
	path='data\\sina_news_gbk\\2016-%02d.txt'%i
	with open(path,'r') as fp:
		lock.acquire()
		lines=fp.readlines()
		lock.release()
		for j,line in enumerate(lines):
			obj=json.loads(line)
			entry1=filterChar(obj['html'])
			entry2=filterChar(obj['title'])
			lock.acquire()
			content.put(entry1)
			content.put(entry2)
			read_info='Reading %s: %5d/%5d' % (path, j + 1, len(lines))
			lock.release()
			sys.stdout.write('\r%s;%s.' % (read_info, process_info))
			sys.stdout.flush()
lock.acquire()
content.put(None)
lock.release()
thread1.join()
calculate()
print('\nSaving data')
with open('prob.dat', 'wb') as fp:
	pickle.dump(pFirstChar, fp)
	pickle.dump(pLastChar, fp)
	pickle.dump(pCharWithNext, fp)
	pickle.dump(pCharWithPrev, fp)
print('Finished.')
