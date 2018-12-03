import imp
import nltk
import pickle
import time

print('Define 2 Tags \n')
# Define 2 tags

tag_set = ['N','S']


f = open('pku_test_data_2tags','rb')
sq_test = pickle.load(f)
f.close()


# Read tagged data
labeled_sequences = sq_test[:10000]


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
hmm = trainer.train_supervised(labeled_sequences)
end = time.time()
print("running time:\t",(end-start)/3600,"\t hour(s) \n")



hmm.test(sq_test[500:510], verbose=True)

# Test result:
#   accuracy over 973 tokens: 86.43


