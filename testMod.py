from SenSeg import Mod

M = Mod()
M.readWord('zh-wiki-dic.txt')

M.trainHMM()

M.infoTrain()

M.infoWord()

M.infoChar()

M.save('M')