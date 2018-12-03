import imp
import pickle
import re

# Step 1
'''
first remove all unnecessary symbols
replace them by "\n"
or only delet them
save the result in "test", for other usage
'''

f = open('pku_training.txt')
st = f.read()
f.close()

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

f = open('test.txt','w')
f.write(st)
f.close



# Step 2
'''
tagging the sentences, based on spaces
2 tages are used:
{N}: not segment after the character
{S}: segment after the character
'''

f = open('test.txt','r')
sq_test = f.readlines()
f.close()

n = len(sq_test)
for i in range(n):
    sq_test[i] = list(sq_test[i].strip('\n'))

# del empty lists
sq_test = [x for x in sq_test if x != []]


# mannual tagging before test
sq_test2 = []

for i in range( len(sq_test) ):
        st = []
        for j in range(len(sq_test[i])-1):
                if sq_test[i][j]!=' ':
                        if sq_test[i][j+1]!=' ':
                                st += [ (sq_test[i][j],'N') ]
                        else:
                                st += [ (sq_test[i][j],'S') ]
        sq_test2 += [ st ]

sq_test = sq_test2
# del empty lists
sq_test = [x for x in sq_test if x != []]

f = open ('test_2tags.txt','wb')
pickle.dump(sq_test,f)
f.close()

