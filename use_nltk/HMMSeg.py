#########################################################################################################
# HMM based Chinese Word Segmentation
#########################################################################################################

import imp
import nltk
import pickle
import time


# Define {0,1}/{N,S} HMM tagging function
def HMM_NS_TAG ():

    ''' define tag '''
    tag_set = ['N','S']

    '''
    unlabeled_sequences: for unsupervised training.
    example: [ [ 'st1_wd1', 'st1_wd2', ... ], [ 'st2_wd1', 'st2_wd2', ... ] ].
    each sentence is a sub-list.
    '''
    f = open('train','r')

    '''
    The number to read is by byte, not lines.
    In later step, random pick some sentences.
    '''
    unlabeled_sequences = f.readlines(1000)
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
    f = open('train','r')
    symbols = f.read()
    f.close()

    symbols = symbols.replace('\n','')
    symbols = list(set(symbols))

    ''' Define Trainner '''
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)

    ''' training the model, output the trained hmm model '''
    hmm = trainer.train_unsupervised(unlabeled_sequences)

    ''' save the trained model in a file named "HMM_NS" '''
    f = open ('HMM_NS','wb')
    pickle.dump(hmm,f)
    f.close()

    ''' Test the Accuracy '''
    f = open('pku_test_data_2tags','rb')
    test_sequences = pickle.load(f)
    f.close()

    '''
    Use first 10 to test, not all.
    Later will change to Gold.
    '''
    hmm.test(test_sequences[:10], verbose=False)


# First train HMM as {S,B,M,E}, then use the trained model conduct segmentation
def HMM_SBME_TRAIN_AND_TAG():

    # Define Tags
    tag_set = ['S','B','M','E']

    # Get Symbols
    symbols = GET_SYMBOLS()

    # Get Tagged Sentences
    labeled_sequences = GET_SBME_TAG()

    # Define Trainner
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)

    # Pseudo-Supervised Training the model
    hmm = trainer.train_supervised(labeled_sequences)

    # Tagging, testing, and output accuracy
    # hmm.test(sq_test[500:510], verbose=True)


def GET_SYMBOLS():
    '''
    The dictionary of characteristics, not the word.
    Example: ['word1', 'word2', 'word3', ... ,'word n']
    '''

    f = open('MF_Result','r')
    symbols = f.read()
    f.close()

    symbols = symbols.replace('\n','')
    symbols = list(set(symbols))
    
    return symbols


# Get the {S,B,M,E} tagged sentences from Morfessor result
def GET_SBME_TAG():
    ''' read result from Morfessor '''
    f = open('MF_Result','r')
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
        for j in range(len(seged_sequences[i])):
            # Depends on Morfessor result, need to be modified
            # Here assume the last character is not "space"
            if ( j == (len(seged_sequences)-1) ):
                if ( seged_sequences[i][j-1]!=' ' ):
                    st += [ (seged_sequences[i][j],'E') ]
                else:
                    st += [ (seged_sequences[i][j],'S') ]
            elif ( seged_sequences[i][j]!=' ' ):
                if (seged_sequences[i][j-1]==' ') and (seged_sequences[i][j+1]==' '):
                    st += [ (seged_sequences[i][j],'S') ]
                elif (seged_sequences[i][j-1]==' ') and (seged_sequences[i][j+1]!=' '):
                    st += [ (seged_sequences[i][j],'B') ]
                elif (seged_sequences[i][j-1]!=' ') and (seged_sequences[i][j+1]==' '):
                    st += [ (seged_sequences[i][j],'E') ]
                else:
                    st += [ (seged_sequences[i][j],'M') ]
        
        tagged_sequences += [ st ]

    return tagged_sequences

