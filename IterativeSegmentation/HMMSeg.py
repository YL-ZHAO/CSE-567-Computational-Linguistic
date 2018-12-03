#########################################################################################################
# HMM based Chinese Word Segmentation
#########################################################################################################

import imp
import nltk
import pickle
import time
import random

# Define {0,1}/{N,S} HMM tagging function


def HMM_NS_old(name_train, name_test, num_iteration):
    ''' define tag '''
    tag_set = ['N', 'S']

    '''
    unlabeled_sequences: for unsupervised training.
    example: [ [ 'st1_wd1', 'st1_wd2', ... ], [ 'st2_wd1', 'st2_wd2', ... ] ].
    each sentence is a sub-list.
    '''
    f = open(name_train, 'r')

    '''
    The number to read is by byte, not lines.
    In later step, random pick some sentences.
    '''
    unlabeled_sequences = f.readlines()
    f.close()

    ''' delet redundant symbols '''
    n = len(unlabeled_sequences)
    for i in range(n):
        unlabeled_sequences[i] = list(unlabeled_sequences[i].strip('\n'))

    ''' delet empty rows '''
    unlabeled_sequences = [x for x in unlabeled_sequences if x != []]

    '''
    The dictionary of characteristics, not the word.
    Example: ['word1', 'word2', 'word3', ... ,'word n'].
    '''
    f = open(name_train, 'r')
    symbols = f.read()
    f.close()

    symbols = symbols.replace('\n', '')
    symbols = list(set(symbols))

    ''' Define Trainner '''
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)

    ''' training the model, output the trained hmm model '''
    hmm = trainer.train_unsupervised(unlabeled_sequences, max_iterations=num_iteration)


    '''
    save the trained model in a file named "HMM_NS"
    f = open ('HMM_NS','wb')
    pickle.dump(hmm,f)
    f.close()
    '''

    ''' Test the Accuracy '''
    f = open(name_test, 'rb')
    test_sequences = pickle.load(f)
    f.close()

    '''
    Use first 50 to test, not all.
    Later will change to Gold.
    '''
    # here is some problem, the test number can't be larger...
    hmm.test(test_sequences[0:200], verbose=False)

    st = []
    for i in range(len(unlabeled_sequences)):
        result = hmm.tag(unlabeled_sequences[i])
        for j in range(len(unlabeled_sequences[i])-1):
            if result[j][1] == 'S':
                st += [result[j][0], ' ']
            else:
                st += [result[j][0]]

        st += [result[len(unlabeled_sequences[i])-1][0], '\n']

    st[-1] = ''
    st = ''.join(st)

    f = open('01_HMM_tagging.txt', 'w')
    f.write(st)
    f.close()


# given some segmented text, use supervised training
def HMM_NS_pre(name_train_1, name_train_2, name_test):

    ##########################################################################
    #                      Training                                          #
    ##########################################################################

    # name_train_1: result from morfessor
    # name_train_2: 00_st_train.txt
    # name_test:    00_st_test_ns

    # Define Tags
    tag_set = ['N', 'S']

    # Get Symbols
    symbols = GET_SYMBOLS(name_train_1)

    # Get Tagged Sentences
    labeled_sequences = GET_NS_TAG(name_train_1)

    # Define Trainner
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)

    # Pseudo-Supervised Training the model
    hmm = trainer.train_supervised(labeled_sequences)
    
    ##########################################################################
    #                     Testing                                            #
    ##########################################################################

    # Print segmentation accuracy
    print('Tagging accuracy after by HMM training:\n')
    f = open(name_test, 'rb')
    test_sequences = pickle.load(f)
    f.close()

    # sampling 200 setences and test
    test_sequences = random.sample(test_sequences,200)
    hmm.test(test_sequences, verbose=False) # the test data has been changed

    ##########################################################################
    #                   Output Seg Result                                    #
    ##########################################################################

    # file used for tagging
    f = open(name_train_2, 'r')
    unlabeled_sequences = f.readlines()
    f.close()

    # delet redundant symbols
    n = len(unlabeled_sequences)
    for i in range(n):
        unlabeled_sequences[i] = list(unlabeled_sequences[i].strip('\n'))
    # delet empty rows '''
    unlabeled_sequences = [x for x in unlabeled_sequences if x != []]

    st = []
    for i in range(len(unlabeled_sequences)):
        result = hmm.tag(unlabeled_sequences[i])
        for j in range(len(unlabeled_sequences[i])-1):
            if (result[j][1] == 'S'):
                st += [result[j][0], ' ']
            else:
                st += [result[j][0]]

        st += [result[len(unlabeled_sequences[i])-1][0], '\n']

    st[-1] = ''
    st = ''.join(st)
    
    # output the segmentation result
    f = open('01_HMM_tagging.txt', 'w')
    f.write(st)
    f.close()


def HMM_NS(name_train_1, name_train_2, name_test, num_iteration):

    # name_train_1: result from morfessor
    # name_train_2: 00_st_train.txt
    # name_test:    00_st_test_ns

    # Define Tags
    tag_set = ['N', 'S']

    # Get Symbols
    symbols = GET_SYMBOLS(name_train_1)

    # Get Tagged Sentences
    labeled_sequences = GET_NS_TAG(name_train_1)

    # Define Trainner
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)

    # Pseudo-Supervised Training the model
    hmm = trainer.train_supervised(labeled_sequences)

    # Tagging, testing, and output accuracy
    # here is some problem, the test number can't be larger...
    print('Tagging accuracy after pseudo-supervised training:\n')
    f = open(name_test, 'rb')
    test_sequences = pickle.load(f)
    f.close()
    hmm.test(test_sequences[0:200], verbose=False)
    

    # Continue training the model, base on given trainsion and emmision matrix
    # unsupervised training use the same file as test
    f = open(name_train_2, 'r')
    unlabeled_sequences = f.readlines()
    f.close()
    # delet redundant symbols
    n = len(unlabeled_sequences)
    for i in range(n):
        unlabeled_sequences[i] = list(unlabeled_sequences[i].strip('\n'))
    # delet empty rows '''
    unlabeled_sequences = [x for x in unlabeled_sequences if x != []]

    hmm = trainer.train_unsupervised(unlabeled_sequences, max_iterations=num_iteration)

    # Tagging, testing, and output accuracy
    # here is some problem, the test number can't be larger...
    print('Tagging accuracy after un-supervised training:\n')
    f = open(name_test, 'rb')
    test_sequences = pickle.load(f)
    f.close()
    hmm.test(test_sequences[0:200], verbose=False)

    # output the segmentation result
    st = []
    for i in range(len(unlabeled_sequences)):
        result = hmm.tag(unlabeled_sequences[i])
        for j in range(len(unlabeled_sequences[i])-1):
            if (result[j][1] == 'S'):
                st += [result[j][0], ' ']
            else:
                st += [result[j][0]]

        st += [result[len(unlabeled_sequences[i])-1][0], '\n']

    st[-1] = ''
    st = ''.join(st)

    f = open('01_HMM_tagging.txt', 'w')
    f.write(st)
    f.close()


# First train HMM as {S,B,M,E}, then use the trained model conduct segmentation
def HMM_SBME_pre(name_train_1, name_train_2, name_test, num_iteration):

    # name_train_1: result from morfessor
    # name_train_2: 00_st_train.txt
    # name_test:    00_st_test_sbme

    # Define Tags
    tag_set = ['S', 'B', 'M', 'E']

    # Get Symbols
    symbols = GET_SYMBOLS(name_train_2)

    # Get Tagged Sentences
    labeled_sequences = GET_SBME_TAG(name_train_1)

    # Define Trainner
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)

    # Pseudo-Supervised Training the model
    hmm = trainer.train_supervised(labeled_sequences)


    
    # Continue training the model, base on given trainsion and emmision matrix
    # unsupervised training use the same file as test
    f = open(name_train_2, 'r')
    unlabeled_sequences = f.readlines()
    f.close()
    
    # delet redundant symbols
    n = len(unlabeled_sequences)
    for i in range(n):
        unlabeled_sequences[i] = list(unlabeled_sequences[i].strip('\n'))
    # delet empty rows
    unlabeled_sequences = [x for x in unlabeled_sequences if x != []]
    
    '''
    hmm = trainer.train_unsupervised(unlabeled_sequences, max_iterations=num_iteration)
    '''

    # Tagging, testing, and output accuracy
    # here is some problem, the test number can't be larger...
    f = open(name_test, 'rb')
    test_sequences = pickle.load(f)
    f.close()
    hmm.test(test_sequences[0:200], verbose=False)

    # output the segmentation result
    st = []
    for i in range(len(unlabeled_sequences)):
        result = hmm.tag(unlabeled_sequences[i])
        for j in range(len(unlabeled_sequences[i])-1):
            if ( (result[j][1] == 'S') or (result[j][1] == 'E') ):
                st += [result[j][0], ' ']
            else:
                st += [result[j][0]]

        st += [result[len(unlabeled_sequences[i])-1][0], '\n']

    st[-1] = ''
    st = ''.join(st)

    f = open('01_HMM_tagging.txt', 'w')
    f.write(st)
    f.close()


# First train HMM as {S,B,M,E}, then use the trained model conduct segmentation
def HMM_SBME(name_train_1, name_train_2, name_test, num_iteration):

    # name_train_1: result from morfessor
    # name_train_2: 00_st_train.txt
    # name_test:    00_st_test_sbme

    # Define Tags
    tag_set = ['S', 'B', 'M', 'E']

    # Get Symbols
    symbols = GET_SYMBOLS(name_train_1)

    # Get Tagged Sentences
    labeled_sequences = GET_SBME_TAG(name_train_1)

    # Define Trainner
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)

    # Pseudo-Supervised Training the model
    hmm = trainer.train_supervised(labeled_sequences)

    # Tagging, testing, and output accuracy
    # here is some problem, the test number can't be larger...
    f = open(name_test, 'rb')
    test_sequences = pickle.load(f)
    f.close()
    hmm.test(test_sequences[0:200], verbose=False)
    

    # Continue training the model, base on given trainsion and emmision matrix
    # unsupervised training use the same file as test
    f = open(name_train_2, 'r')
    unlabeled_sequences = f.readlines()
    f.close()
    # delet redundant symbols
    n = len(unlabeled_sequences)
    for i in range(n):
        unlabeled_sequences[i] = list(unlabeled_sequences[i].strip('\n'))
    # delet empty rows '''
    unlabeled_sequences = [x for x in unlabeled_sequences if x != []]

    hmm = trainer.train_unsupervised(unlabeled_sequences, max_iterations=num_iteration)

    # Tagging, testing, and output accuracy
    # here is some problem, the test number can't be larger...
    f = open(name_test, 'rb')
    test_sequences = pickle.load(f)
    f.close()
    hmm.test(test_sequences[0:200], verbose=False)

    # output the segmentation result
    st = []
    for i in range(len(unlabeled_sequences)):
        result = hmm.tag(unlabeled_sequences[i])
        for j in range(len(unlabeled_sequences[i])-1):
            if ( (result[j][1] == 'S') or (result[j][1] == 'E') ):
                st += [result[j][0], ' ']
            else:
                st += [result[j][0]]

        st += [result[len(unlabeled_sequences[i])-1][0], '\n']

    st[-1] = ''
    st = ''.join(st)

    f = open('01_HMM_tagging.txt', 'w')
    f.write(st)
    f.close()


def GET_SYMBOLS(name):
    '''
    The dictionary of characteristics, not the word.
    Example: ['word1', 'word2', 'word3', ... ,'word n']
    '''

    f = open(name, 'r')
    symbols = f.read()
    f.close()

    symbols = symbols.replace('\n', '')
    symbols = list(set(symbols))

    return symbols


# Get the {S,B,M,E} tagged sentences from Morfessor result
def GET_SBME_TAG(name):
    ''' read result from Morfessor '''
    f = open(name, 'r')
    seged_sequences = f.readlines()
    f.close()

    ''' preprocessing '''
    n = len(seged_sequences)
    for i in range(n):
        seged_sequences[i] = list(seged_sequences[i].strip('\n'))

    ''' del empty lists '''
    seged_sequences = [x for x in seged_sequences if x != []]

    ''' tagging, used for HMM as a pseudo-supervised training data '''
    tagged_sequences = []
    for i in range(len(seged_sequences)):
        st = []

        if (len(seged_sequences[i]) == 1):
            st += [(seged_sequences[i][0], 'S')]
        else:
            for j in range(len(seged_sequences[i])):
                # Depends on Morfessor result, need to be modified
                if (seged_sequences[i][j] != ' '):

                    if (j == (len(seged_sequences[i])-1)):
                        if (seged_sequences[i][j-1] != ' '):
                            st += [(seged_sequences[i][j], 'E')]
                        else:
                            st += [(seged_sequences[i][j], 'S')]

                    if (j == 0):
                        if (seged_sequences[i][j+1] == ' '):
                            st += [(seged_sequences[i][j], 'S')]
                        else:
                            st += [(seged_sequences[i][j], 'B')]

                    if (j > 0 and j < (len(seged_sequences[i])-1)):
                        if (seged_sequences[i][j-1] == ' ') and (seged_sequences[i][j+1] == ' '):
                            st += [(seged_sequences[i][j], 'S')]
                        elif (seged_sequences[i][j-1] == ' ') and (seged_sequences[i][j+1] != ' '):
                            st += [(seged_sequences[i][j], 'B')]
                        elif (seged_sequences[i][j-1] != ' ') and (seged_sequences[i][j+1] == ' '):
                            st += [(seged_sequences[i][j], 'E')]
                        else:
                            st += [(seged_sequences[i][j], 'M')]

        tagged_sequences += [st]

    return tagged_sequences


# Get the {N,S} tagged sentences
def GET_NS_TAG(name):
    # load from "name" file
    f = open(name, 'r')
    sq_test = f.readlines()
    f.close()

    n = len(sq_test)
    for i in range(n):
        sq_test[i] = list(sq_test[i].strip('\n'))

    # mannual tagging
    sq_test2 = []

    for i in range(len(sq_test)):
        st = []
        for j in range(len(sq_test[i])):
            if sq_test[i][j] != ' ':
                if (j == len(sq_test[i])-1):
                    st += [(sq_test[i][j], 'S')]
                else:
                    if sq_test[i][j+1] != ' ':
                        st += [(sq_test[i][j], 'N')]
                    else:
                        st += [(sq_test[i][j], 'S')]

        sq_test2 += [st]

    sq_test = sq_test2

    return sq_test

