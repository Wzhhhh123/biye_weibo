import json
from random import randrange
from mysql_util import MysqlUtil
from flask.json import jsonify
from flask import Flask, render_template,url_for
from flask import request
import pandas as pd
import requests
import re
from pyecharts import options as opts
from pyecharts.charts import Line
import time
import datetime




app = Flask(__name__, static_folder="templates")

@app.route('/boob')
def index23():

    # 遍历文章数据
    return render_template('/cake/boob.html')  # 渲染模板


@app.route('/cake')
def index3():

    # 遍历文章数据
    return render_template('/cake/index.html')  # 渲染模板


@app.route('/')
def index():

    # 遍历文章数据
    return render_template('home.html')  # 渲染模板
@app.route('/liuxing')
def index4():

    # 遍历文章数据
    return render_template('liuxing.html')  # 渲染模板

@app.route('/hotpot')
def index2():
    db = MysqlUtil()  # 实例化数据库操作类
    page = request.args.get('page')  # 获取当前页码
    if page is None:  # 默认设置页码为1
        page = 0
    # 分页查询
    # 从article表中筛选5条数据，并根据日期降序排序
    m=re.findall("\d+", str(time.strftime("%Y-%m-%d", time.localtime())))
    m=m[0]+m[1]+m[2]
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
    m=date_delta(m,int(page))
    kk=m[0:4]+"-"+m[4:6]+"-"+m[6:8]
    sql = f'SELECT * FROM weibohotpot  where create_date="{kk}"'
#     sql = f'SELECT * FROM weibohotpot  ORDER BY create_date DESC LIMIT {(int(page) - 1) * count},{count}'
    articles = db.fetchall(sql)  # 获取多条记录
    # 遍历文章数据
    return render_template('hotpot.html', articles=articles, page=int(page))  # 渲染模板







if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0',port=5555)
