import lda
import numpy as np
import matplotlib.pyplot as plt
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

documentfile = r'f:/contracts/lda/origin_document.txt'


def create_topic():
    # 存取语料库， 一行为一个文档
    corpus = []
    for line in open(documentfile, 'r').readlines():
        corpus.append(line.strip())
    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    X = X.toarray()
    print(X.shape)
    # LDA算法
    model = lda.LDA(n_topics=5, n_iter=500, random_state=1)
    model.fit(np.asanyarray(X))
    topic_word = model.topic_word_

    # print(topic_word)
    # n_top_words = 8
    # for i, topic_dist in enumerate(topic_word):
    #     topic_words = [np.argsort(topic_dist)][:-(n_top_words+1):-1]
    #     print('Topic {}: {}'.format(i, ' '.join(topic_words)))

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

    # 计算文档主题分布图
    f, ax = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
    for i, k in enumerate([0, 1]):  # 两个主题
        ax[i].stem(topic_word[k, :], linefmt='b-',
                   markerfmt='bo', basefmt='w-')
        ax[i].set_xlim(-2, 20)
        ax[i].set_ylim(0, 1)
        ax[i].set_ylabel("Prob")
        ax[i].set_title("topic {}".format(k))
    ax[1].set_xlabel("word")
    plt.tight_layout()


if __name__ == '__main__':
    create_topic()
