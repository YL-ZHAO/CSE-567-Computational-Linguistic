import imp
import pickle
import re

f = open('train.txt','r')
sq = f.read()
f.close()

sq = re.sub('\n\n*','\n',sq)

l=int(len(sq)/80)

sq = sq[:l]


f = open('train','w')
f.write(sq)
f.close