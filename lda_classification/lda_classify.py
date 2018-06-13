from matplotlib import pyplot as plt
import shutil
import numpy as np
import lda


documentfile = r'f:/contracts/lda/origin_document.txt'
titlefile = r'f:/contracts/lda/titles.txt'
vocabfile = r'f:/contracts/lda/vocab.txt'
matrixfile = r'f:/contracts/lda/matrix.txt'

def load_matrix():
    return lda.utils.ldac2dtm(open(matrixfile), offset=0)

def load_vocab():
    with open(vocabfile, 'r') as f:
        vocab = tuple(f.read().split())
    return vocab

def load_titles():
    with open(titlefile, 'r') as f:
        titles = tuple(line.strip() for line in f.readlines())
    return titles


def classify():
    X = load_matrix()
    vocab = load_vocab()
    titles = load_titles()
    print(X.shape)

    model = lda.LDA(n_topics=5, n_iter=500, random_state=1)
    model.fit_transform(X)

    # 每个topic中频率最高的5个词
    topic_word = model.topic_word_
    n_top_words = 100
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    # 每个文档可能性最高的topic
    doc_topic = model.doc_topic_
    for i in range(10):
        print("{} (top topic:{})".format(titles[i], doc_topic[i].argmax()))

if __name__ == '__main__':
    # create_topic()
    classify()