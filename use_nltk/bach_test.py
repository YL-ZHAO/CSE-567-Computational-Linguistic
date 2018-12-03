import imp
import nltk
import pickle
import time


f = open('pku_test_data_2tags','rb')
sq_test = pickle.load(f)
f.close()


f = open('hmm_2tags_1e4sent','rb')
hmm = pickle.load(f)
f.close()


hmm.test(sq_test[:10], verbose=True)

