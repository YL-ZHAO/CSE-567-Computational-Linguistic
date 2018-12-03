import imp
import nltk
import pickle
import time

print('Define 4 Tags \n')
# Define 4 tags
'''
1. I'm not sure, if HMM can find the sequencial relation between B-M-E.
    This strong sequence relation is not observed in other tagging.
2. I guess, punctuation symbles, will be tagged as "S".
'''
tag_set = ['S','B','M','E']


print('Read Unlabled Sequences \n')
# unlabeled_sequences: for unsupervised training
'''
Example:
[ [ 'st1_wd1', 'st1_wd2', ... ], [ 'st2_wd1', 'st2_wd2', ... ] ]
each sentence is a sub-list ???
'''
f = open('train','r')
sq_org = f.readlines(10000)
f.close()

n = len(sq_org)
for i in range(n):
    sq_org[i] = list(sq_org[i].strip('\n'))

# del empty lists
sq_org = [x for x in sq_org if x != []]

unlabeled_sequences = sq_org
del sq_org


print('Read Symbols \n')
# The dictionary of characteristics, not the word
'''
Example:
['word1', 'word2', 'word3', ... ,'word n']
'''
f = open('train','r')
sy_org = f.read()
f.close()

sy_org = sy_org.replace('\n','')
symbols = list(set(sy_org))
del sy_org


print('Define Trainer \n')
# trainner
trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)


print('Training the model... \n')
# training the model, output the trained hmm model
start = time.time()
hmm = trainer.train_unsupervised(unlabeled_sequences)
end = time.time()
print("running time:\t",(end-start)/3600,"\t hour(s) \n")

# save the trained model in a file named "hmm"
f = open ('hmm_4tags_10000sent','wb')
pickle.dump(hmm,f)
f.close()

print('Test Example \n')
# test
sq_test = [ [ ('我','S'), ('今','B'), ('天','E'), ('去','S'), ('健','B'), ('身','M'), ('房','E'), ('锻','B'), ('炼','E'), ('了','S'), ('。','S') ] ]
hmm.test(sq_test, verbose=True)
