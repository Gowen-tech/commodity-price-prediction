# 基于网络关注度的大宗农产品价格预测

## 代码与部分数据简介

### 文件概览

```
── cs277_final
   ├── ADFTestResults
   ├── SecurityCheck.csv
   ├── adf_text.py
   ├── gc_test.ipynb
   ├── model_training
   │   ├── 棕榈油index.csv
   │   ├── 玉米index.csv
   │   ├── 豆油index.csv
   │   ├── 基准模型.ipynb
   │   ├── 网络关注度模型.ipynb
   │   └── 大连期货交易所大宗农产品DRR表.csv
   ├── preprocessing.py
   ├── related_words_extraction
   │   ├── Index_Crawler.md
   │   ├── bbs_spider.py
   │   └── word2vec_train.py
   ├── tools.py
   ├── 豆油
   │   ├── 豆油index
   │   └── 豆油价格
   └── 棕榈油
       ├── 棕榈油index
       ├── 棕榈油价格
       ├── 棕榈油结算价和棕榈index的比对.csv
       ├── 棕榈油结算价和橡胶index的比对.csv
       ├── 棕榈油结算价和大豆油index的比对.csv
       ├── 棕榈油结算价和棕榈树index的比对.csv
       ├── 棕榈油结算价和棕榈油index的比对.csv
       ├── 棕榈油结算价和植物油index的比对.csv
       ├── 棕榈油结算价和椰子油index的比对.csv
       ├── 棕榈油结算价和菜籽油index的比对.csv
       ├── 棕榈油结算价和起酥油index的比对.csv
       ├── 棕榈油结算价和棕榈油产地index的比对.csv
       ├── 棕榈油结算价和棕榈油价格index的比对.csv
       ├── 棕榈油结算价和棕榈油期货index的比对.csv
       └── 棕榈油结算价和棕榈油的危害index的比对.csv
```



### ADFTestResults

这个文件夹默认是空的，之后`adf_test.py`的结果会保存在这里。



### SecurityCheck.csv

这个文件是从大连期货交易所的网站上下载下来，反映了其交易合约代码和具体交易商品的名称的关系。



### adf_test.py

使用方法：

```
python adf_test.py <目录文件名>
```

这个python文件是用来做单位根检验并判断时间序列是否平稳的，使用时后面加入想要包含需要进行adf检验的文件的目录文件名，例如在本仓库中的 `豆油index` 以及 `棕榈油index`。

文件输出至 `ADFTestResults` 文件夹中。



### gc_test.ipynb

这是一个 `jupyter notebook` ，通过里面代码进行一步一步的操作。用于检验的文件，通过 `preprocessing.py` 生成，例如在本仓库中的 `棕榈油结算价和棕榈index的比对.csv` 、`棕榈油结算价和橡胶index的比对.csv` 等比对文件。



### model_training

这是一个文件夹，其中包含了两个SVR模型训练文件 `基准模型.ipynb` 以及 `网络关注度模型.ipynb` 。其他几个文件都是数据文件，这些数据文件是同样通过 `preprocessing.py` 中的方法生成的，因此这里就没有放生成这些数据文件的具体方法，而是直接将训练需要的数据直接放在这里。



### preprocessing.py

使用方法：

```
python preprocessing.py <目录文件名>
```

这个python文件是本仓库较为关键的一个文件，他对于raw data进行数据预处理，方便之后的数据检验的数据训练。此处的目录文件名是包含所有raw data的目录文件名。我们对于raw data的存放有一定的要求，本仓库以 `棕榈油/` 为例，初始文件摆放如下：

```
└── 棕榈油
    ├── 棕榈油index
    │   ├── 棕榈.csv
    │   ├── 橡胶.csv
    │   ├── ···
    │   └── 棕榈油的危害.csv
    └── 棕榈油价格
        ├── 棕榈油_2010.csv
        ├── 棕榈油_2011.csv
        ├── ···
        └── 棕榈油_2018.csv
```

对于每个大宗农产品，我们需要制作一个目录文件，其下需要有两个目录文件，分别存储相关词百度指数和大宗农产品的价格（均保存为csv文件）。执行 `python preprocessing.py 棕榈油/` 后，输出结果如下：

```
└── 棕榈油
    ├── 棕榈油index
    │   ├── log-diff-棕榈.csv
    │   ├── log-diff-橡胶.csv
    │   ├── ···
    │   ├── log-diff-棕榈油的危害.csv
    │   ├── ···
    ├── 棕榈油价格
    │   ├── ···
    │   ├── 棕榈油结算价数据表.csv
    │   └── 棕榈油结算价对数差分数据表.csv
    ├── 棕榈油结算价和棕榈index的比对.csv
    ├── 棕榈油结算价和橡胶index的比对.csv
    ├── ···
    └── 棕榈油结算价和棕榈油的危害index的比对.csv
```

输出主要分为三个部分：

- 在 `<大宗农产品>index` 目录下，应当生成将百度指数进行 `log-diff` 对数差分后的文件。
- 在 `<大宗农产品>价格` 目录下，应当生成结算价数据表（提取结算价，并将不同年份数据文件汇总）以及将结算价进行对数差分后的文件。
- 最后，在 `<大宗农产品>` 目录下，应当生成所有相关词的网络关注度指标（对数差分后）与结算价指标（对数差分后）的比对文件。

**本仓库提供了豆油的raw data给读者做测试，执行 `python preprocessing.py 豆油/` 即可。**



### related_keywords_extraction

文件目录下有两个python文件和一个markdown文件。python文件执行顺序如下：

1. `pip install gensim`
2. 执行 `python bbs_spider.py` ，输出结果：在当前文件夹下生成 `bbs_text.cor` 。
3. 修改 `word2vec_train.py` 中词库的路径（代码中有注释），将 `bbs_text.cor` 放到 `gensim` 放语料库的文件夹中，并将文件路径填入。
4. 执行 `python word2vec_train.py` ，输出结果：在当前文件夹下生成 `bbs.model` 。
5. 训练完模型，注释掉模型训练部分，激活剩余部分查看相似结果。

`Index Crawler.md` 文件中包含了我们对于百度爬虫的借鉴代码来源，我们没有对他进行框架性质的改动，只是改了部分内容，例如爬取单词的时间，以及基于csdn的破解方法（具体请查看论文内容）。我们在本仓库中提供了和豆油以及棕榈油相关词的百度指数，以供参考。



### tools.py

这个文件中为工具包，无需执行。为其他文件提供方法支持。



## 建议代码执行顺序

`bbs_spider.py` -> `word2vec_train.py` -> `preprocessing.py` -> `adf_test.py` -> `gc_test.ipynb` -> `基准模型.ipynb` -> `网络关注度模型.ipynb`