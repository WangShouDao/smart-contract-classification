import os, sys
import re
import shutil
import numpy as np
import pandas as pd
from sklearn import feature_extraction
import nltk
import nltk.data
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import matplotlib.pyplot as plt

# 停用词
stopwords = nltk.corpus.stopwords.words("english")
# 词干化
stemmer = SnowballStemmer("english")


# 定义了分词器和词干分析器，输出词干
def tokenize_and_stem(text):
    # 先分句， 再分词， 标点会包括在内
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        token.encode('utf-8')
        if re.match('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

# 仅对合约实现分词
def tokenize_only(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    # filtered_tokens = []
    # for token in tokens:
    #     if re.search('[a-zA-Z]', token):
    #         filtered_tokens.append(token)
    # return filtered_tokens
    return tokens

# 获取当前目录下的非目录文件
def listdir():
    path = r'F:\contracts\test'
    file_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        file_list.append(file_path)
    return file_list

contracts = []
# 建立待加入词库的合约
def create_contract_lib(file_list):
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as f:
            temp = f.read()
        contracts.append(temp)

# 建立词库
def create_vocabularies():
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    for i in contracts:
        allwords_stemmed = tokenize_and_stem(i)
        totalvocab_stemmed.extend(allwords_stemmed)
        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)
    # vocab_frame = pd.DataFrame({'words':totalvocab_tokenized}, index = totalvocab_stemmed)
    # return vocab_frame

# 建立分类的文件夹
def create_directory(n):
    path = r'F:\contracts\category'
    for i in range(n):
        file = os.path.join(path, str(i))
        if not os.path.exists(file):
            os.mkdir(file)

# 文件名集合
def listfile():
    path = r'F:\contracts\test'
    file_list = []
    for file in os.listdir(path):
        file_list.append(file)
    return file_list


# 分类
def classifation(class_list):
    file_list = listfile()
    filepath1 = r'F:\contracts\test\\'
    filepath2 = r'F:\contracts\category\\'
    for i in range(len(class_list)):
        shutil.copyfile(filepath1+file_list[i], filepath2+str(class_list[i])+'\\'+file_list[i])


# 定义向量化参数
def define_Vector():
    # tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.2, stop_words='english', use_idf = True,
    #                                    tokenizer=tokenize_and_stem, ngram_range=(1,3))
    # tfidf_vectorizer = TfidfVectorizer(min_df=0, tokenizer=tokenize_only)
    tfidf_vectorizer = TfidfVectorizer(min_df=0)
    tfidf_matrix = tfidf_vectorizer.fit_transform(contracts).toarray()
    print(tfidf_matrix.shape)
    # 写入txt文档
    # np.savetxt("F:\contracts\matrix.txt", tfidf_matrix, fmt='%f', delimiter=' ')
    # "terms” 这个变量只是tf - idf矩阵中的特征（features）表，也是一个词汇表
    terms = tfidf_vectorizer.get_feature_names()
    # print(len(terms))
    # with open(r'F:\contracts\terms.txt', 'w+', encoding='utf-8') as f:
    #     for i in range(len(tfidf_matrix)):
    #         f.write(u"第%s个合约\n"%i)
    #         for j in range(len(terms)):
    #             f.write('%s, %s\n'%(terms[j], tfidf_matrix[i][j]))
    # print(terms)
    # dist用来评估任意两个或多个合约之间的相似度
    # dist = 1 - cosine_similarity(tfidf_matrix)

    # kmeans
    num_clusters = 6
    create_directory(num_clusters)
    km = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10, max_iter=10).fit(tfidf_matrix)
    # 持久化
    # joblib.dump(km, r'F:\contracts\doc_cluster.pkl')
    # km = joblib.load(r'F:\contracts\doc_cluster.pkl')
    # clusters = km.labels_.tolist()
    '''
    clusters = km.labels_.tolist()
    # 使用DataFrame
    dt = {'contract':contracts, 'cluster':clusters}
    frame = pd.DataFrame(dt, index=[clusters], columns=['contract'])
    # 按离质心的距离排列聚类中心，由近到远
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    for i in range (num_clusters):
        print("Cluster %d words: "% i, end='')
        for j in order_centroids[i, :6]:
            print(' %s '%vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
        print()  # add whitespace
        print()  # add whitespace

        print("Cluster %d titles:" % i, end='')
        for title in frame.ix[i]['title'].values.tolist():
            print(' %s,' % title, end='')
        print()  # add whitespace
        print()  # add whitespace
    '''


    # 下面是三个属性
    # 把聚类的样本打标签
    labelPred = km.labels_.tolist()
    # 显示聚类的质心
    centroids = km.cluster_centers_
    # 这个可以看成损失，就是样本距其最近样本的平方总和
    inertia = km.inertia_

    print(labelPred)
    # print(centroids)
    # print(inertia)
    classifation(labelPred)
    '''  
    # 库里包装的方法
    # 返回预测的样本属于的类的聚类中心
    print(km.fit_predict(tfidf_matrix))
    print(km.predict(tfidf_matrix))
    # 返回每个样本与聚类中心的距离
    print(km.fit_transform(tfidf_matrix))
    print(km.transform(tfidf_matrix))
    # 和损失一样，评价聚类好坏
    print(km.score(tfidf_matrix))
'''


if __name__ == '__main__':
    create_contract_lib(listdir())
    # vocab_frame = create_vocabularies()
    define_Vector()
