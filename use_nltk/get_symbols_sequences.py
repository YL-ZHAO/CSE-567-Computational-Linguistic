import re

# Generate training/test sentence

f = open('pku_training.txt')
st = f.read()
# list_all = f.readlines()
f.close()

st = re.sub('\ ','',st)

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


f = open('train.txt','w')
f.write(st)
f.close


'''
n = len(list_all)

for i in range(n):
    list_all[i] = list(list_all[i])
'''

