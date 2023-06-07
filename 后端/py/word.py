import pyecharts.options as opts
from pyecharts.charts import WordCloud
import jieba

def wordcount1(resu) ->WordCloud:
    word_dict = {}
    for i in range(len(resu)):
        text = resu[i]['全文内容']
        stop_words = []
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                stop_words.append(line.strip())
        seg_list = jieba.cut(text)
        seg_list = [seg_list for seg_list in seg_list if len(seg_list) > 1 and seg_list not in stop_words]
        for word in seg_list:
            if word !='cn' and word !='http':
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
    sorted_word_dict = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)



    WordCloud1 = (
            WordCloud()
        .add(series_name="词云", data_pair=sorted_word_dict[0:100], word_size_range=[6, 66])
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="词云", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )

    )

    return WordCloud1