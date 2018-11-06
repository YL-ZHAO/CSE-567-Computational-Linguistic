'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    Class Mod

Define the class Sentence Segmentation Module/Model.
Its instance will save the trained data, and conduct
sentence segmentation.

                    Xingyu YAN
                xingyuyan@outlook.com
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class Mod:

    #-----------------------------------------------------
    # Define model parameters.
    # This is given based on the paper of Chen et al.

    # For HDP:
    __alf1 = 1000   # alpha 1
    __alf = 10      # alpha
    __ps = 0.5      # p#

    # For HMM:
    __the = 1       # theta
    __sig = 0.01    # sigma

    #-----------------------------------------------------
    # Define model data
    Word = []


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
        f.close()
        for i in range(len(self.Word)):
            self.Word[i] = self.Word[i].strip('\n')

    # Train the model
    def train(self):
        print("train fun not started...")

    # Train the HMM part
    def train_HMM(self):
        print("train_HMM fun not started...")
        print("alpha 1", self.__alf1)
        print("alpha", self.__alf)
        print("p#", self.__ps)

    # Train the HDP part
    def train_HDP(self):
        print("train_HDP fun not started...")
        print("theta", self.__the)
        print("sigma", self.__sig)

    #-----------------------------------------------------
    # Segment Stage
    # Read sentence to be segmented
    def readSent(self):
        print("readSent fun not started...")

    # Segment sentence
    def segSent(self):
        print("segSent fun not started...")

    #-----------------------------------------------------
    # Additional Methods

    # Print word info
    def infoWord(self):
        print('----------------------------------------')
        print('Word info:')
        print('\t # of words: \t', len(self.Word))
        print('----------------------------------------')

    # Print training info
    def infoTrain(self):
        print("infoTrain fun not started...")

    # Print segmentation result
    def infoSeg(self):
        print("infoDic fun not started...")

    # Save/export current model and data.
    # If the model has been trained, simply save it for next time.
    def save(self,name):

        import pickle

        f = open(name,'wb')     # write binary
        pickle.dump(self,f)
        f.close()

        # hint for load:
        import pickle
        f = open(name,'rb')
        mod = pickle.load(f)
        f.close()
