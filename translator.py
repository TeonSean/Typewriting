import pickle
import util
import math

print('loading data...')
with open('prob.dat', 'rb') as fp:
	pFirstChar=pickle.load(fp)
	pOccur=pickle.load(fp)
	pCharWithNext=pickle.load(fp)
	pCharWithPrev=pickle.load(fp)
print('done')

def probFirstChar(py0, py1, ch_idx):
	if not py1:
		return pFirstChar[py0][ch_idx]*multiplier
	alpha=0.3
	re=alpha*pFirstChar[py0][ch_idx]+(1-alpha)*pCharWithNext[py0][py1][ch_idx]
	return re

def getFirstChar(py0, py1):
	cand=util.py2ch[py0]
	occur=list(map(lambda x:[x, pOccur[py0][x]], cand))
	occur.sort(key=lambda x:x[1], reverse=True)
	multiplier=dict()
	descend=(1-0.5)/len(cand)
	tmp=1
	for i in range(len(occur)):
		multiplier[occur[i][0]]=tmp
		tmp-=descend
	sortable=list(map(lambda x:[x, probFirstChar(py0, py1, x)], cand))
	sortable.sort(key=lambda x:x[1], reverse=True)
	return sortable[0][0]

def probNextChar(py, prev, next, cur):
	if not next:
		return pCharWithPrev[py][prev][cur]
	alpha=0.5
	re=alpha*pCharWithPrev[py][prev][cur]+(1-alpha)*pCharWithNext[py][next][cur]
	return re

def getNextChar(py, ch, next):
	cand=util.py2ch[py]
	occur=list(map(lambda x:[x, pOccur[py][x]], cand))
	occur.sort(key=lambda x:x[1], reverse=True)
	multiplier=dict()
	descend=(1-0.5)/len(cand)
	tmp=1
	for i in range(len(occur)):
		multiplier[occur[i][0]]=tmp
		tmp-=descend
	sortable=list(map(lambda x:[x, probNextChar(py, ch, next, x)], cand))
	sortable.sort(key=lambda x:x[1], reverse=True)
	return sortable[0][0]

def translate(input):
	pylist=util.input2array(input)
	if len(pylist) == 0:
		return None
	elif len(pylist) == 1:
		return util.idx2ch[getFirstChar(pylist[0], None)]
	else:
		chlist=list()
		chlist.append(getFirstChar(pylist[0], pylist[1]))
		for i in range(1, len(pylist)):
			chlist.append(getNextChar(pylist[i], chlist[i-1], pylist[i+1] if i < len(pylist)-1 else None))
		return util.array2output(chlist)
