#########################################################################################################
# Combination of HMM and Morfessor Cost Function
#########################################################################################################

import SimpleSeg
import HMMSeg

#########################################################################################################

'''
Conduct iterative, unsupervised word segmentation.
The processes are:

    1. {0,1}/{N,S} segmentation using HMM.
        output sentences segmented by spaces.
    
    2. Optimize the segmentation based on Morfessor cost calculation.
        combine oversegmented words.
        output sentences segmented by spaces.
    
    3. With output from Morfessor, train the HMM, {S,B,M,E}.
        then re-segment the same sentences.
        output sentences segmented by spaces.
    
    4. Repeat 2--3, untile accuracy change is less than threshold.
'''

#########################################################################################################


# Define simple segmentation function
'''
for the initial segmentation
the result from HMM is not good
'''
def SSeg():

    f = open('train.txt','r')
    sy_org = f.read()
    f.close()
    sy_org = sy_org.replace('\n','')
    sy_org = sy_org.replace(' ','')

    text = sy_org[:5000]

    seg1 = "1" * (len(text)-1)
    SimpleSeg.anneal(text, seg1, 5000, 1.2)




#########################################################################################################
# 01. {0,1}/{N,S} tagging by HMM
HMMSeg.HMM_NS_TAG()

#########################################################################################################
# 01. {0,1}/{N,S} tagging
SSeg()

#########################################################################################################
# Repeat 2<-->3, untile converge, or reach certain iterations
iteration_num = 0
accuracy_value = []
'''
while (iteration_num<100 or accuracy_value[-1]>60):
    # 2. Morfessor Part.
    
    # 3. HMM Part.
    HMM_SBME_TRAIN_AND_TAG()
'''