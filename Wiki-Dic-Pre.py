# Preprocessing for the Dictionary, from zhwiki
# Using Regular Expression
import re

# read data
zh = open('zhwiki.txt')
str = zh.read()
zh.close()

# processing
# delete unnecessary characteristics and spaces
nstr = re.sub(r'([0-9]*:[0-9]*:)','',str)
nstr = re.sub(r'([A-Z]*[a-z]*:)','',nstr)
nstr = re.sub(r'\(','\n',nstr)
nstr = re.sub(r'\)','',nstr)
nstr = re.sub(r'PRC\ admin\w*','',nstr)
nstr = re.sub(r'\ ','',nstr)

# write in new file
nzh = open('zh-wiki-dic.txt','w')
nzh.write(nstr)
nzh.close()