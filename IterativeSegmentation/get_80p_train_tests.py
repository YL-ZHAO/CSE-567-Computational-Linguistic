import re
import pickle
import HMMSeg

# Generate training/test sentence

f = open('00_pku_training.txt')
st = f.read()
f.close()


# following remove symbols

st = re.sub('“','\n',st)
st = re.sub('”','\n',st)

st = re.sub('’','\n',st)
st = re.sub('‘','\n',st)

st = re.sub('『','\n',st)
st = re.sub('』','\n',st)

st = re.sub('《','\n',st)
st = re.sub('》','\n',st)

st = re.sub('、','\n',st)
st = re.sub('—','\n',st)
st = re.sub('：','\n',st)

st = re.sub('，','\n',st)
st = re.sub('；','\n',st)
st = re.sub('。','\n',st)
st = re.sub('！','\n',st)
st = re.sub('？','\n',st)
st = re.sub('（','\n',st)
st = re.sub('）','\n',st)

st = re.sub('％','',st)
st = re.sub('．','',st)
st = re.sub('℃','',st)

st = re.sub('∶','',st)
st = re.sub('·','',st)
st = re.sub('／','',st)

st = re.sub('\ \ \n','\n',st)
st = re.sub('\n\n*','\n',st)

l=int(len(st)/150)

st = st[:l]

# for different usage
st_train = st
st_test = st

###################################################################################
# for st_train, remove spaces
st_train = re.sub('\ ','',st_train)

print(st_train)

f = open('00_st_train.txt','w')
f.write(st_train)
f.close


###################################################################################
# for st_test
# first write the txt, then read by lines, and processing
f = open('00_st_test.txt','w')
f.write(st_test)
f.close


###################################################################################
# get NS tag by method in HMMSeg
st_test_ns = HMMSeg.GET_NS_TAG('00_st_test.txt')

f = open ('00_st_test_ns','wb')
pickle.dump(st_test_ns,f)
f.close()


###################################################################################
# get SBME tag by method in HMMSeg
st_test_sbme = HMMSeg.GET_SBME_TAG('00_st_test.txt')

f = open ('00_st_test_sbme','wb')
pickle.dump(st_test_sbme,f)
f.close()

