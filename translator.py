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
optimal_list=list()
optimal_score=float('-inf')
alpha=0.5

def getOptimal(pylist, chlist, cur_idx, prefix_score):
	global optimal_list, optimal_score,alpha
	if cur_idx == len(pylist):
		if prefix_score > optimal_score:
			optimal_score=prefix_score
			optimal_list=chlist
		return
	py=pylist[cur_idx]
	for ch in util.py2ch[pylist[cur_idx]]:
		if cur_idx < len(pylist)-1 :
			score=alpha*pCharWithPrev[py][chlist[cur_idx - 1]][ch]+(1-alpha)*(pCharWithNext[py][pylist[cur_idx+1]][ch])
		else:
			score=pCharWithPrev[py][chlist[cur_idx - 1]][ch]
		score*=prefix_score
		if score < optimal_score:
			continue
		getOptimal(pylist, chlist+[ch], cur_idx+1, score)

def translate(input):
	global optimal_list, optimal_score
	pylist=util.input2array(input)
	if len(pylist) == 0:
		return None
	optimal_list=list()
	optimal_score=float('-inf')
	for ch in util.py2ch[pylist[0]]:
		getOptimal(pylist, [ch], 1, 1)
	return util.array2output(optimal_list)