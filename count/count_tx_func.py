import re
from matplotlib import pyplot as plt
import os
import json
import shutil
import nltk
import numpy as np
import lda
import spider.spider_contracts
import time
import scipy
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

documentfile = r'f:/contracts/lda/origin_document.txt'
traincontract = r'F:/contracts/lda/traincontract'
wordidmapfile = r'f:/contracts/lda/wordidmapfile.txt'
titlefile = r'f:/contracts/lda/titles.txt'
vocabfile = r'f:/contracts/lda/vocab.txt'
# 停用词
stopwords = nltk.corpus.stopwords.words("english")
# 自定义停用词
stoplist = ['uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256', 'pragma', 'solidity', 'function', 'event',
            'return', 'returns', 'constant', 'contract', 'address', 'bytes', 'bytes4', 'bytes32','abstract','public',
            'bool', 'string', 'success', 'true', 'false', 'mapping''if', 'else', 'continue', 'break', 'assert']

class DataClean:
    # 分词及过滤出单词
    def tokenize(text):
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z_]', token):
                filtered_tokens.append(token)
        # filtered_tokens = [word for word in filtered_tokens if word not in stopwords]
        filtered_tokens = [word for word in filtered_tokens if word not in stoplist]
        return filtered_tokens

    # 获取当前目录下的非目录文件
    def listdir():
        file_list = []
        for file in os.listdir(traincontract):
            file_path = os.path.join(traincontract, file)
            file_list.append(file_path)
        return file_list

    # 建立待加入词库的合约
    def create_contract_lib(file_list):
        i = 0
        if os.path.exists(titlefile):
            os.remove(titlefile)
        if os.path.exists(documentfile):
            os.remove(documentfile)
        for file in file_list:
            with open(titlefile, 'a', encoding='utf-8') as f:
                f.write('{} {}\n'.format(i, file.split('.')[0]))
            i = i + 1
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read().replace('/',' ').replace('\\',' ').replace('*',' ')
            text = DataClean.tokenize(text)
            with open(documentfile, 'a',encoding='utf-8') as f:
                f.write(' '.join(text)+'\n')

    # 建立词库
    def create_vocabularies(self):
        totalvocab_stemmed = []
        totalvocab_tokenized = []
        for i in self.contracts:
            allwords_tokenized = DataClean.tokenize(i)
            totalvocab_tokenized.extend(allwords_tokenized)


# 提取合约的地址和使用次数
def extract_address():
    address_list = []
    with open(filename, 'r+') as f:
        line = f.read().strip().split('\n')
        for item in line:
            item = json.loads(item)
            address_list.append(item['address'])
    return address_list

def create_documents(address_list, function_filepath):
    file = r'f:/python/etherscan/transactions/'
    with open(function_filepath, 'w+') as f:
        for address in address_list:
            contract_filepath = file + address + '.txt'
            temp = create_document(contract_filepath)
            if temp is not None:
                if len(temp) != 0 :
                    for i in temp:
                        f.write(i+' ')
                    f.write('\n')

def create_document(filepath):
    try:
        i = 0
        function_set = set()
        with open(filepath, 'r+') as f:
            line = f.readline().strip()
            while len(line)!=0:
                if 'Function' in line:
                    item = re.split(':', line)[1].strip()
                    function = re.split('\(', item)[0].strip()
                    function_set.add(function)
                line = f.readline().strip()
                i = i+1
        return function_set
    except Exception as e:
        return None

def create_topic():
    # 存取语料库， 一行为一个文档
    corpus = []
    for line in open(documentfile, 'r').readlines():
        corpus.append(line.strip())
    print(corpus)
    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    analyze = vectorizer.build_analyzer()
    weight = X.toarray()
    print(X.shape)
    # LDA算法
    model = lda.LDA(n_topics=10, n_iter=500, random_state=1)
    model.fit(np.asanyarray(weight))
    topic_word = model.topic_word_

    print(topic_word)
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = [np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    # 文档-主题分布
    doc_topic = model.doc_topic_
    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))

    # 输出前10篇文章最有可能的Topic
    label = []
    for n in range(10):
        topic_most_pr = doc_topic[n].argmax()
        label.append(topic_most_pr)
        print("doc: {} topic: {}".format(n, topic_most_pr))



def count_function(filepath):
    try:
        i = 0
        function_dict = {}
        with open(filepath, 'r+') as f:
            line = f.readline().strip()
            while len(line)!=0:
                if 'Function' in line:
                    item = re.split(':', line)[1].strip()
                    function = re.split('\(', item)[0].strip()
                    if function not in function_dict.keys():
                        function_dict[function] = 1
                    else:
                        function_dict[function] += 1
                line = f.readline().strip()
                i = i+1
        return function_dict
    except Exception as e:
        return None

def draw(function_dict):
    name = []
    count = []
    for (k,v) in function_dict.items():
        name.append(k)
        count.append(int(v))
    # 设置matplotlib正常显示中文和负号
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    bar_width = 0.3
    rects1 = plt.bar(range(len(count)), count, width=0.5, color='b')
    plt.xticks(range(len(count)), name)
    plt.xlabel('功能名称')
    plt.ylabel('功能的使用次数')
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    plt.show()

# 读取所有的合约名
def contracts_list():
    path = r'f:/python/contracts'
    file_list = []
    for file in os.listdir(path):
        file_list.append(file)
    return file_list

# 创建txt文件存储数据
def mkdir(filename):
    if not os.path.exists(filename):
        fp = open(filename, 'w+')
        fp.close()
        return True
    else:
        fp = open(filename, 'w+')
        fp.truncate()
        return False


filename = r'f:/contracts/lda/content.txt'
if __name__ == '__main__':
    # function_filepath = r'f:/contracts/lda/function.txt'
    # mkdir(function_filepath)
    # address_list =  extract_address()
    # create_documents(address_list, function_filepath)
    # 读取交易信息
    # create_topic()
    DataClean.create_contract_lib(DataClean.listdir())
    '''
    file_list = contracts_list()
    dstlist = []
    for address in address_list:
        dstfile = r'f:/contracts/lda/contract/' + address + '.txt'
        for file in file_list:
            if address in file:
                srcfile = r'f:/python/contracts/' + file
                shutil.copyfile(srcfile, dstfile)
                dstlist.append(address)
    for i in dstlist:
        address_list.remove(i)
    for address in address_list:
        spider.spider_contracts.spider_contracts(address)
    '''
    # print(preprocessing())

    # create_topic()