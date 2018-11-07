# CSE-567-Computational-Linguistic
This is for the course project, unsupervised Chinese word segmentation.

## 1. Get the wiki index as our word dictionary.

For unsupervised methods, wiki is a good resource to acquire language resources.

> https://dumps.wikimedia.org/zhwiki/

## 2. Using Morfessor to realize word segmentation.

> http://morpho.aalto.fi/projects/morpho/

Morfessor is designed to conduct morphological segmentation. For Chinese word segementation,
we can compare each sentence to a single word, then segment it by Morfessor. The training of
Morfessor model uses the word dictionary extracted from wiki index.

Here are two segmentation examples from different type of resources.
### Online forum discussion:
https://www.1point3acres.com/bbs/thread-452818-1-1.html

> **Original:**  
收到了这个职位的面试邀请  
想请问一下地里面的小伙伴  
这个职位主要是做什么的  
我看职位描述  
又有SQL  
又有Python  
还有ML  
**Segmentation**  
收 到 了 这个 职位 的 面试 邀请  
想 请 问 一 下 地 里 面的 小 伙伴  
这个 职位 主要 是 做 什么 的  
我 看 职位 描述  
又 有 SQL  
又 有 Python  
还 有 ML  

### Online news:
https://news.qq.com/a/20181028/008376.htm

> **Original:**  
央视网消息新闻联播  
习近平总书记在广东考察时强调  
要高举新时代改革开放旗帜  
继续全面深化改革  
全面扩大开放  
并向世界宣示中国改革开放不停步  
总书记的重要讲话在各地干部群众中引发热烈反响  
大家表示  
要以更坚定的信心  
努力工作  
把改革开放不断推向深入  
**Segmentation:**  
央视 网 消息 新闻联播  
习近平 总书记 在 广东 考察 时 强 调  
要 高 举 新时代 改革开放 旗帜  
继续 全面深化改革  
全面 扩大 开放  
并 向 世界 宣 示 中国 改革开放 不 停 步  
总书记 的 重要 讲话 在各地 干部 群众 中 引 发 热 烈 反 响  
大家 表示  
要 以 更 坚 定 的 信心  
努力 工作  
把 改革开放 不 断 推 向 深入  

## 3. Realize HMM-HDP & Gibbs based algorithm.

### 3.1. Create Instance:

Import package, create instance:  
>
from SenSeg import Mod  
M = Mod()  

You can save the instance at anytime for later use:  
>
M.save('M')  

### 3.2. Read Dictionary Data:

If the data is the index from wiki directly:  
>
\# name1 is the wiki file name  
\# name2 is the output dictionary file name  
M.readWiki(name1, name2)  

If the data has been processed, read it directly:  
>
M.readWord('zh-wiki-dic.txt')  

### 3.3. Train Model

The method will train the model in HMM and HDP:  
>
M.trainMod()

It calls two methods:  
>
M.trainHMM()  
M.trainHDP()  


## Other resources:

> Dirichlet Distribution:
https://zh.wikipedia.org/wiki/%E7%8B%84%E5%88%A9%E5%85%8B%E9%9B%B7%E5%88%86%E5%B8%83

> LDA:
https://zh.wikipedia.org/wiki/%E9%9A%90%E5%90%AB%E7%8B%84%E5%88%A9%E5%85%8B%E9%9B%B7%E5%88%86%E5%B8%83

> https://zhuanlan.zhihu.com/p/31470216

> https://blog.csdn.net/v_july_v/article/details/41209515

![](/tobecontinued.jpg)