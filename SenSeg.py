'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    Class Mod

Define the class Sentence Segmentation Module/Model.
Its instance will save the trained data, and conduct
sentence segmentation.

                    Xingyu YAN
                xingyuyan@outlook.com
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import numpy as np
import pickle
import re

class Mod:

    def __init__(self):

        #-----------------------------------------------------
        # Define model parameters.
        # This is given based on the paper of Chen et al.

        # For HDP:
        self.__alf1 = 1000   # alpha 1
        self.__alf = 10      # alpha
        self.__ps = 0.5      # p#

        # For HMM:
        self.__the = 1       # theta
        self.__sig = 0.01    # sigma
        self.__T = 4         # 4 tags {SBME}
        self.__V = 0         # number of char, get value after readWord()

        #-----------------------------------------------------
        # Define model data, including training dictionary and
        #   training results.
        
        # Training dictionary
        self.Word = []
        self.Char = []

        # HMM training results
        self.Pt = np.zeros( (4,4) )     # {SBME}
        self.Pe = np.zeros( (4,len(self.Char)) )

        # HDP training results


    #-----------------------------------------------------
    # Define methods, read dict, train model, segment
    #-----------------------------------------------------
    # Training Stage
    # Read word data
    # Word data should be preprocessed, so that each
    # line is a chinese word.
    def readWord(self,name):

        f = open(name)
        self.Word = f.readlines()
        f.seek(0)
        self.Char = f.read()
        f.close()
        
        for i in range(len(self.Word)):
            self.Word[i] = self.Word[i].strip('\n')
        
        self.Char = self.Char.replace('\n','')
        self.Char = list(set(self.Char))    # set(), non-sequenced, no overlaping
        self.__V = len(self.Char)

    # If the dictionary is from wiki, no preprocessing,
    #   then use this function to preprocess and read
    def readWiki(self,name1,name2):
        # name1 : name of input file
        # name2 : name of output file
        #   output it so no need to process next time

        # read data
        f = open(name1)
        st = f.read()
        f.close()

        # processing
        # delete unnecessary characteristics and spaces
        nst = re.sub(r'([0-9]*:[0-9]*:)','',st)
        nst = re.sub(r'([A-Z]*[a-z]*:)','',nst)
        nst = re.sub(r'\(','\n',nst)
        nst = re.sub(r'\)','',nst)
        nst = re.sub(r'PRC\ admin\w*','',nst)
        nst = re.sub(r'\ ','',nst)

        # write in new file
        f = open(name2,'w')
        f.write(nst)
        f.close()

        del f, st, nst

        self.readWord(name2)


    # Train the model
    def trainMod(self):

        self.trainHMM
        self.trainHDP
    
    # Train the HMM part
    def trainHMM(self):
        # { S B M E }
        #   0 1 2 3

        #-----------------------------------------------------
        # Train Transition Probability
        '''
        since we use the dictionary from wiki, not the corpus as the article,
        our word has no context relation with front and back
        in trainning HMM, I assume S->S and S->B are equal, they share have of
        the count of count_s
        same assumptions are also applied for other calculation
        '''
        count_s = 0
        count_bm = 0
        count_be = 0
        count_mm = 0
        count_me = 0
        count_e = 0

        for w in self.Word:
            
            if len(w)==1:
                count_s = count_s + 1
            elif len(w)==2:
                count_be = count_be + 1
            elif len(w)>2:
                count_bm = count_bm + 1
                count_me = count_me + 1
                count_mm = count_mm + (len(w)-3)
        
        count_e = count_be + count_me
        
        # S->S
        self.Pt[0,0] = (count_s/2 + self.__the)/(count_s + self.__T*self.__the)
        # S->B
        self.Pt[0,1] = (count_s/2 + self.__the)/(count_s + self.__T*self.__the)
        
        # B->M
        self.Pt[1,2] = (count_bm + self.__the)/(count_bm + count_be + self.__T*self.__the)
        # B->E
        self.Pt[1,3] = (count_be + self.__the)/(count_bm +count_be + self.__T*self.__the)

        # M->M
        self.Pt[2,2] = (count_mm + self.__the)/(count_mm +count_me + self.__T*self.__the)
        # M->E
        self.Pt[2,3] = (count_me + self.__the)/(count_mm +count_me + self.__T*self.__the)

        # E->S
        self.Pt[3,0] = (count_e/2 + self.__the)/(count_e + self.__T*self.__the)
        # E->B
        self.Pt[3,1] = (count_e/2 + self.__the)/(count_e + self.__T*self.__the)

        #-----------------------------------------------------
        # Train Emission Probability


        


    # Train the HDP part
    def trainHDP(self):
        print("trainHDP fun not started...")
        print("theta", self.__the)
        print("sigma", self.__sig)

    #-----------------------------------------------------
    # Segment Stage
    # Read sentence to be segmented
    def readSen(self):
        print("readSen fun not started...")

    # Segment sentence
    def segSen(self):
        print("segSen fun not started...")

    #-----------------------------------------------------
    # Additional Methods

    # Print word info
    def infoWord(self):
        print('----------------------------------------')
        print('Word info:')
        print('\t # of words: \t', len(self.Word))
        print('----------------------------------------')

    # Print characteristic info
    def infoChar(self):
        print('----------------------------------------')
        print('Char info:')
        print('\t # of Chars: \t', len(self.Char))
        print('----------------------------------------')
    
    # Print training info
    def infoTrain(self):
        print('----------------------------------------')
        print("HMM-Pt:")
        print(self.Pt)

    # Print segmentation result
    def infoSeg(self):
        print("infoDic fun not started...")

    # Save/export current model and data.
    # If the model has been trained, simply save it for next time.
    def save(self,name):

        f = open(name,'wb')     # write binary
        pickle.dump(self,f)
        f.close()

        '''
        hint for load:
        import pickle
        f = open(name,'rb')
        mod = pickle.load(f)
        f.close()
        '''