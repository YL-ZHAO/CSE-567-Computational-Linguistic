#---------------------------------------------------------
# Define the class Sentence Segmentation Module/Model
#   Its instance will save the trained data, and conduct
#   sentence segmentation.
#
#--------------------Xingyu YAN---------------------------
#----------------xingyuyan@outlook.com--------------------

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





    #-----------------------------------------------------
    # Define methods, read dict, train model, segment
    #-----------------------------------------------------
    # Training Stage
    # Read dictionary data
    def readDic(self):
        print("readDic fun not started...")

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

    # Print dictionary info
    def infoDic(self):
        print("infoDic fun not started...")

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
