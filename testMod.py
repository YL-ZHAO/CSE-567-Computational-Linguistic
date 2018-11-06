from SentSeg import Mod

M = Mod()
M.readDic('zh-wiki-dic.txt')

print(M.Dic[0])

print(M.Dic[-1])

M.infoDic()