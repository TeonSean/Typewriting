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

def getCandCnt(pylist):
	cnt=1
	for py in pylist:
		cnt*=len(util.py2ch[py])
	return cnt

def int2array(n, pylist):
	re=list()
	pylist=list(reversed(pylist))
	for py in pylist:
		length=len(util.py2ch[py])
		re.append(util.py2ch[py][n%length])
		n //= length
	return list(reversed(re))

def getSentenceScore(chlist, pylist):
	return 1

def translate(input):
	pylist=util.input2array(input)
	if len(pylist) == 0:
		return None
	cnt=getCandCnt(pylist)
	optimal_list=list()
	optimal_score=float("-inf")
	for i in range(cnt):
		chlist=int2array(i, pylist)
		score=getSentenceScore(chlist, pylist)
		if score > optimal_score:
			optimal_score=score
			optimal_list=chlist
	return util.array2output(chlist)
