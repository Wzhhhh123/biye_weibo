import pyecharts.options as opts
from pyecharts.charts import WordCloud
import jieba

def wordcount1(resu) ->WordCloud:
    word_dict = {}
    for i in range(len(resu)):
        text = resu[i]['全文内容']
        seg_list = jieba.cut(text)
        for word in seg_list:
            if word !='，' and word != '、' and word != '的' and word != '。' and word != '“'  and word != '”'  and word != ' ':
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