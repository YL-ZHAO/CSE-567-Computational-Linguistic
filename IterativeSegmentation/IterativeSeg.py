#########################################################################################################
# Combination of HMM and Morfessor Cost Function
#########################################################################################################

import HMMSeg
import os
import time
import SimpleSeg as SS

def MF():
    os.system("python2 mor.py 01_HMM_tagging.txt")

#########################################################################################################

'''
Conduct iterative, unsupervised word segmentation.
The processes are:

    1. {0,1}/{N,S} segmentation using HMM.
        output sentences segmented by spaces.
    
    2. Optimize the segmentation based on Morfessor cost calculation.
        combine oversegmented words.
        output sentences segmented by spaces.
    
    3. With output from Morfessor, train the HMM, {N,S}.
        then re-segment the same sentences.
        output sentences segmented by spaces.
    
    4. Repeat 2--3, untile accuracy change is less than threshold.
'''
#########################################################################################################
# 00. Given a small amount of training data for initialization, get corresponding transition probabilities

SS.Seg("00_st_train.txt",500,"01_SS_tagging.txt")


#########################################################################################################
# 01. {0,1}/{N,S} tagging by HMM

HMMSeg.HMM_NS_pre('01_SS_tagging.txt','00_st_train.txt','00_st_test_ns')


#########################################################################################################
# Repeat 2<-->3, untile converge, or reach certain iterations

iteration_num = 0


while (iteration_num<100): # or accuracy_value[-1]>60):
    print("==============================================================================================\n")
    print("Iteration Num:\t",iteration_num,'\n')
    # 2. Morfessor Part.
    MF()

    # 3. HMM Part.
    HMMSeg.HMM_NS_pre( '02_MF_tagging.txt', '00_st_train.txt', '00_st_test_ns')
    # HMMSeg.HMM_NS( '02_MF_tagging.txt', '00_st_train.txt', '00_st_test_ns',10)

    iteration_num = iteration_num + 1
    print("==============================================================================================\n")

