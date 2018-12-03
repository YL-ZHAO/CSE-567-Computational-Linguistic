import imp
import nltk
import pickle
import time


f = open('test_2tags.txt','rb')
sq_test = pickle.load(f)
f.close()


f = open('hmm_2tags_1e4sent','rb')
hmm = pickle.load(f)
f.close()


hmm.test(sq_test, verbose=True)


