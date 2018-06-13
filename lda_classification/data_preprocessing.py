import re
import os
import json
import nltk
import numpy as np
import lda

documentfile = r'f:/contracts/lda/origin_document.txt'
traincontract = r'F:/contracts/lda/traincontract'
wordidmapfile = r'f:/contracts/lda/wordidmapfile.txt'
titlefile = r'f:/contracts/lda/titles.txt'
vocabfile = r'f:/contracts/lda/vocab.txt'
matrixfile = r'f:/contracts/lda/matrix.txt'
# 停用词
stopwords = nltk.corpus.stopwords.words("english")
# 自定义停用词
stoplist = ['uint','uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256', 'pragma', 'solidity', 'function', 'event',
            'return', 'returns', 'constant', 'contract', 'address', 'bytes', 'bytes4', 'bytes32', 'abstract', 'public',
            'bool', 'string', 'success', 'true', 'false', 'mapping''if', 'else', 'continue', 'break', 'assert',
            'github', 'ethereum','mappings','sol','param','value','internal','library','com']


# 获取当前目录下的非目录文件
def acquire_filename():
    file_list = []
    for file in os.listdir(traincontract):
        file_path = os.path.join(traincontract, file)
        file_list.append(file_path)
    return file_list


# 分词与去掉停用词
def tokenize(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.match('[a-zA-Z_]', token):
            filtered_tokens.append(token)
    filtered_tokens = [word for word in filtered_tokens if word not in stopwords]
    filtered_tokens = [word for word in filtered_tokens if word not in stoplist]
    return filtered_tokens


# 把所有分档分词并写入到一个文档中， 同时把文档名写入
def create_contract_lib(file_list):
    i = 0
    if os.path.exists(titlefile):
        os.remove(titlefile)
    if os.path.exists(documentfile):
        os.remove(documentfile)
    for file in file_list:
        with open(titlefile, 'a', encoding='utf-8') as f:
            f.write('{} {}\n'.format(i, file.split('.')[0].split('\\')[-1]))
        i = i + 1
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read().replace('/', ' ').replace('\\', ' ').replace('*', ' ').replace('\'', ' ').replace('.',' ').\
                replace('-',' ').replace('_',' ').replace('+',' ').replace('=',' ').replace('.',' ').replace('^',' ')
        text = tokenize(text)
        with open(documentfile, 'a', encoding='utf-8') as f:
            f.write(' '.join(text) + '\n')


# 建立词库
def create_vocabularies():
    vocab = set()
    with open(documentfile, 'r') as f:
        documents = f.readlines()
    for document in documents:
        words = document.strip().split()
        for word in words:
            vocab.add(word)
    if os.path.exists(vocabfile):
        os.remove(vocabfile)
    with open(vocabfile, 'a', encoding='utf-8') as f:
        for word in vocab:
            f.write(word + '\n')
    return list(vocab)

# 建立矩阵
def create_matrix(vocab):
    if os.path.exists(matrixfile):
        os.remove(matrixfile)
    with open(documentfile, 'r') as f:
        documents = f.readlines()
    for document in documents:
        temp = [0 for i in range(len(vocab))]
        words = document.strip().split()
        for word in words:
            temp[vocab.index(word)]+=1
        n = len(vocab)-temp.count(0)
        with open(matrixfile, 'a') as f:
            f.write(str(n))
            for i in range(len(temp)):
                if temp[i]!=0:
                    f.write(' '+ str(i)+':'+ str(temp[i]))
            f.write('\n')

if __name__ == '__main__':
    create_contract_lib(acquire_filename())
    create_matrix(create_vocabularies())
# 调整格式 shift + alt + ctrl + L
