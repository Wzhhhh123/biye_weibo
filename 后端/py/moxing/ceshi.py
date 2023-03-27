import re
import joblib
import jieba
# 获取停用词列表
import re
import joblib
stop_words_path = 'py/moxing/stopwords_cn.txt'
def remove_stropwords(mytext):
    return " ".join([word for word in mytext.split() if word not in cachedStopWords])
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file,encoding='utf-8') as f:                         
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file,encoding='utf-8') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list
 
 
# 去除停用词方法
def remove_stropwords(mytext,cachedStopWords):
    return " ".join([word for word in mytext.split() if word not in cachedStopWords])
 
# 处理否定词不的句子
def  Jieba_Intensify(text):
    word = re.search(r"不[\u4e00-\u9fa5 ]",text)
    if word!=None:
        text = re.sub(r"(不 )|(不[\u4e00-\u9fa5]{1} )",word[0].strip(),text)
    return text
 
# 判断句子消极还是积极
def IsPoOrNeg(text):
    # 加载训练好的模型     
#     model = joblib.load('tfidf_nb_sentiment.model')
    model = joblib.load('py/moxing/tfidf_svm1_sentiment.model')
    # 获取停用词列表   
    cachedStopWords = get_custom_stopwords(stop_words_path)
    # 去除停用词    
    text = remove_stropwords(text,cachedStopWords)
    # jieba分词         
    seg_list = jieba.cut(text, cut_all=False)
    text = " ".join(seg_list)
    # 否定不处理
    text = Jieba_Intensify(text)
    y_pre =model.predict([text])
    proba = model.predict_proba([text])[0]
    if y_pre[0]==1:
        return (y_pre[0]+"情绪，概率："+str(proba[1]))
    else:
        return (y_pre[0]+"情绪,概率："+str(proba[0]))
 
