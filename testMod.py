from SentSeg import Mod

M = Mod()
M.readWord('zh-wiki-dic.txt')

print(M.Word[0])

print(M.Word[-1])

print(M.Pt)

M.infoWord()

M.infoChar()

M.save('M')