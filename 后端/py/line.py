import time, json
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
def date_delta(date,gap,formate = "%Y%m%d"):
        date = str2date(date)
        pre_date = date + datetime.timedelta(days=-gap)
        pre_str = date2str(pre_date,formate)  # date形式转化为str
        return pre_str


def str2date(str,date_format="%Y%m%d"):
    date = datetime.datetime.strptime(str, date_format)
    return date

def date2str(date,date_formate = "%Y%m%d"):
    str = date.strftime(date_formate)
    return str
def render_lines(count_number):
    date_list=[]
    number_list=[]

    for i in range(len(count_number)):
        date_list.append(date2str(count_number[i]['create_date']))
        number_list.append(count_number[i]['t'])
    line = (
            Line()
        .add_xaxis(date_list)
        .add_yaxis('热搜数量', number_list, is_smooth=True,
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                        opts.MarkPointItem(type_="min")]))

        # 隐藏数字 设置面积
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False))
        # 设置x轴标签旋转角度
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
                        yaxis_opts=opts.AxisOpts(name='数量', min_=0),
                        title_opts=opts.TitleOpts(title='每日微博热搜图'))
        )


    return line