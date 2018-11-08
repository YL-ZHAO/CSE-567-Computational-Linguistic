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
from multiprocessing import Pool

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
        
        # Using dictionary
        self.Word = []
        self.Char = []

        # HMM training
        self.count_s = 0
        self.count_b = 0
        self.count_m = 0
        self.count_e = 0
        
        self.count_bm = 0
        self.count_be = 0
        self.count_mm = 0
        self.count_me = 0

        self.Pt = np.zeros( (4,4) )     # {SBME}
        self.Pe = np.zeros( (len(self.Char),4) )

        # HDP training results


    #-----------------------------------------------------
    # Core Methods
    #-----------------------------------------------------
    
    # Read word data
    '''
    Word data should be preprocessed, so that each
        line is a chinese word.
    '''
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
        self.Pe = np.zeros( (len(self.Char),4) )


    # Read raw wiki data
    '''
    If the dictionary is from wiki, no preprocessing,
        then use this function to preprocess and read
    '''
    def readWiki(self,name1,name2):
        '''
        name1 : name of input file
        name2 : name of output file
            output it so no need to process next time
        '''
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

        self.trainHMM()
        self.trainHDP()
    

    # Train the HMM part
    def trainHMM(self):
        # Tags
        '''
        { S B M E }
          0 1 2 3
        '''
        # train HMM Pt
        '''
        must train HMM Pt first
        the count data will be used for Pe
        '''
        self.trainHMMPt()

        # train HMM Pe
        pool = Pool()
        results = pool.map(self.trainHMMPe,range(len(self.Char)))
        pool.close()
        pool.join()
        results = np.array(results)
        self.Pe = results


    # Train HMM Pt
    def trainHMMPt(self):
        #-----------------------------------------------------
        # Train Transition Probability
        #-----------------------------------------------------
        '''
        since we use the dictionary from wiki, not the corpus as the article,
        our word has no context relation with front and back
        in trainning HMM, I assume S->S and S->B are equal, they share have of
        the count of count_s
        same assumptions are also applied for other calculation
        '''
        for w in self.Word:
            
            if len(w)==1:
                self.count_s = self.count_s + 1
            elif len(w)==2:
                self.count_be = self.count_be + 1
            elif len(w)>2:
                self.count_bm = self.count_bm + 1
                self.count_me = self.count_me + 1
                self.count_mm = self.count_mm + (len(w)-3)
        
        self.count_b = self.count_bm + self.count_be
        self.count_m = self.count_bm + self.count_mm
        self.count_e = self.count_be + self.count_me
        
        # S->S
        self.Pt[0,0] = (self.count_s/2 + self.__the)/(self.count_s + self.__T*self.__the)
        # S->B
        self.Pt[0,1] = (self.count_s/2 + self.__the)/(self.count_s + self.__T*self.__the)
        
        # B->M
        self.Pt[1,2] = (self.count_bm + self.__the)/(self.count_bm + self.count_be + self.__T*self.__the)
        # B->E
        self.Pt[1,3] = (self.count_be + self.__the)/(self.count_bm + self.count_be + self.__T*self.__the)

        # M->M
        self.Pt[2,2] = (self.count_mm + self.__the)/(self.count_mm + self.count_me + self.__T*self.__the)
        # M->E
        self.Pt[2,3] = (self.count_me + self.__the)/(self.count_mm + self.count_me + self.__T*self.__the)

        # E->S
        self.Pt[3,0] = (self.count_e/2 + self.__the)/(self.count_e + self.__T*self.__the)
        # E->B
        self.Pt[3,1] = (self.count_e/2 + self.__the)/(self.count_e + self.__T*self.__the)


    # Train HMM Pe
    def trainHMMPe(self,idx):
        #-----------------------------------------------------
        # Train Emission Probability
        #-----------------------------------------------------
        '''
        row number corresponding to self.Char
        idx is the index of self.Char
        '''
        print(idx)
        c = self.Char[idx]
        Pe = [None]*4
        nt0 = 0
        nt1 = 0
        nt2 = 0
        nt3 = 0
        for w in self.Word:
            l = len(w)
            for i in range(l):
                if c == w[i]:
                    if l == 1:
                        nt0 = nt0 + 1
                    elif i == 0:
                        nt1 = nt1 + 1
                    elif i == l-1:
                        nt3 = nt3 + 1
                    else:
                        nt2 = nt2 + 1
        
        Pe[0] = (nt0 + self.__sig) / (self.count_s + self.__V*self.__sig)
        Pe[1] = (nt1 + self.__sig) / (self.count_b + self.__V*self.__sig)
        Pe[2] = (nt2 + self.__sig) / (self.count_m + self.__V*self.__sig)
        Pe[3] = (nt3 + self.__sig) / (self.count_e + self.__V*self.__sig)
        return Pe

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
    #-----------------------------------------------------

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
        print("HMM-Pe:")
        print(self.Pe)
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