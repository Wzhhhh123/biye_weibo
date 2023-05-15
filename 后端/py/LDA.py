import jieba
import gensim
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from gensim.models import CoherenceModel
def LDA_1(sql_word1):
    data=[]
    for i in sql_word1:
        data.append(i["全文内容"])


    # 加载停用词表
    stop_words = []
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            stop_words.append(line.strip())

    # 对文本进行预处理
    processed_docs = []
    for doc in data:
        # 分词
        tokens = list(jieba.cut(doc))
        # 去除停用词
        tokens = [token for token in tokens if len(token) > 1 and token not in stop_words]
        processed_docs.append(tokens)

    # 构建词典
    dictionary = gensim.corpora.Dictionary(processed_docs)

    # 构建语料库
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # 训练LDA模型
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=dictionary,
                                                num_topics=3,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)


    baohan=[]

    # 查看每个主题下的关键词
    for idx, topic in lda_model.show_topics(formatted=True, num_topics=3, num_words=10):

        baohan.append('  关键词: {}'.format(topic))
    return baohan
