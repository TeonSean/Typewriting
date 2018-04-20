import pickle
import util
import math

print('loading data...')
with open('prob.dat', 'rb') as fp:
	pFirstChar=pickle.load(fp)
	pLastChar=pickle.load(fp)
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
	sorted_cand=list(map(lambda x: [x,getScore(py, x, chlist[cur_idx-1], pylist[cur_idx+1] if cur_idx < len(pylist) - 1 else None)], util.py2ch[py]))
	sorted_cand.sort(key=lambda x: x[1], reverse=True)
	for item in sorted_cand:
		score=item[1]+prefix_score
		if score < optimal_score:
			continue
		getOptimal(pylist, chlist+[item[0]], cur_idx+1, score)

def getScore(py, ch, prev, next):
	if prev:
		score=alpha*pCharWithPrev[py][prev][ch]
	else:
		score=alpha*pFirstChar[py][ch]
	if next:
		score+=(1-alpha)*pCharWithNext[py][next][ch]
	else:
		score+=(1-alpha)*pLastChar[py][ch]
	return math.log(score)


def translate(input):
	global optimal_list, optimal_score
	pylist=util.input2array(input)
	if len(pylist) == 0:
		return None
	optimal_list=list()
	optimal_score=float('-inf')
	sorted_cand=list(map(lambda x: [x,getScore(pylist[0], x, None, pylist[1] if len(pylist) > 1 else None)], util.py2ch[pylist[0]]))
	sorted_cand.sort(key=lambda x: x[1], reverse=True)
	for item in sorted_cand:
		getOptimal(pylist, [item[0]], 1, item[1])
	return util.array2output(optimal_list)
