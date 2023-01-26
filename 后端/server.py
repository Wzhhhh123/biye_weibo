import json
from random import randrange
from mysql_util import MysqlUtil
from flask.json import jsonify
from flask import Flask, render_template,url_for,request
import pandas as pd
import requests
import re
import os
import csv
from pyecharts import options as opts
from pyecharts.charts import Line,Bar
import time
import datetime
from flask_cors import CORS,cross_origin
from py.line import render_lines
from py.radar import radar
from py.sankey import sankey
from py.weibo import time_formater,get_single_page,getLongText,parse_page,kaishi
from py.graph import graph
from py.forp import forpa,get_single_page1,parse_page1,parse_page_twice,parse_page_third
import random
app = Flask(__name__, static_folder="templates")
CORS(app, resources=r'/*')
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
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login.html')
def login():
    return render_template('/SK2/login.html')

@app.route('/register.html')
def register():
    return render_template('/SK2/register.html')

@app.route('/forgot-password.html')
def forgot():
    return render_template('/SK2/forgot-password.html')


@app.route('/hotpot')
def index2():
    db = MysqlUtil()
    page = request.args.get('page')
    if page is None:
        page = 0
    m=re.findall("\d+", str(time.strftime("%Y-%m-%d", time.localtime())))
    m=m[0]+m[1]+m[2]
    m=date_delta(m,int(page))
    kk=m[0:4]+"-"+m[4:6]+"-"+m[6:8]
    sql = f'SELECT * FROM weibohotpot  where create_date="{kk}"'
    sql_2 = f'select create_date,count(create_date) as t from weibohotpot group by create_date'
#     sql = f'SELECT * FROM weibohotpot  ORDER BY create_date DESC LIMIT {(int(page) - 1) * count},{count}'
    articles = db.fetchall(sql)  # 获取多条记录
    db = MysqlUtil()
    count_number = db.fetchall(sql_2)
    return render_template('hotpot.html', articles=articles, page=int(page), numbers=count_number)  # 渲染模板

@app.route("/hotpot/barChart",methods=["GET", "POST"])
def submit():
    sql_2 = f'select create_date,count(create_date) as t from weibohotpot group by create_date'
    db = MysqlUtil()
    count_number = db.fetchall(sql_2)
    numbers=count_number
    return numbers

@app.errorhandler(404)
def page_not_found(error):
    return render_template('SK2/404.html'), 404

@app.route('/changecountry', methods=['POST', 'GET'])
def changeCountry():
    sql_2 = f'select create_date,count(create_date) as t from weibohotpot group by create_date'
    db = MysqlUtil()
    count_number = db.fetchall(sql_2)
    return render_lines(count_number).dump_options_with_quotes()

@app.route('/radar', methods=['POST', 'GET'])
def radar1():
    m=re.findall("\d+", str(time.strftime("%Y-%m-%d", time.localtime())))
    m=m[0]+m[1]+m[2]
    kk=m[0:4]+"-"+m[4:6]+"-"+m[6:8]
    sql_3 = f'select zhong,count(zhong) as t from weibohotpot  WHERE create_date="{kk}" group by zhong'
    db = MysqlUtil()
    count_number = db.fetchall(sql_3)
    return radar(count_number).dump_options_with_quotes()



@app.route('/DH')
def indqwex():
    db = MysqlUtil()  # 实例化数据库操作类
    page = request.args.get('page')  # 获取当前页码
    if page is None:  # 默认设置页码为1
        page = 0
    # 分页查询
    # 从article表中筛选5条数据，并根据日期降序排序
    m=re.findall("\d+", str(time.strftime("%Y-%m-%d", time.localtime())))
    m=m[0]+m[1]+m[2]
    m=date_delta(m,int(page))
    kk=m[0:4]+"-"+m[4:6]+"-"+m[6:8]
    sql = f'SELECT * FROM weibohotpot  where create_date="{kk}"'
    sql_2 = f'select create_date,count(create_date) as t from weibohotpot group by create_date'
#     sql = f'SELECT * FROM weibohotpot  ORDER BY create_date DESC LIMIT {(int(page) - 1) * count},{count}'
    articles = db.fetchall(sql)  # 获取多条记录
    db = MysqlUtil()
    count_number = db.fetchall(sql_2)
    sql_6=f'SELECT count(`id`) as t FROM `weiboevents`'
    sql_7=f'SELECT count(`id`) as t FROM `weibohotpot`;'
    db = MysqlUtil()
    count_eventsnumber = db.fetchall(sql_6)
    db = MysqlUtil()
    count_hotnumber = db.fetchall(sql_7)
    sql_8=f'SELECT count(`id`) as t FROM `weiboevents` WHERE gender="f"'
    db = MysqlUtil()
    count_famale = (db.fetchall(sql_8)[0]['t']/count_eventsnumber[0]['t'])*100
    count_male = 100-count_famale
    sql_9=f'SELECT count(`id`) as t FROM `weiboevents` WHERE `status_country`="中国" OR `status_country`!="中国"'
    db = MysqlUtil()
    zhan_1=db.fetchall(sql_9)[0]['t']
    sql_10=f'SELECT count(`id`) as t FROM `weiboevents` WHERE `status_country`="中国" '
    db = MysqlUtil()
    zhanbiCHI=round((db.fetchall(sql_10)[0]['t']/zhan_1)*100,1)

    return render_template('SK2/index.html', articles=articles, page=int(page), numbers=count_number, count_eventsnumber=count_eventsnumber ,count_hotnumber=count_hotnumber,f=count_famale,m=count_male,chi=zhanbiCHI)  # 渲染模板

@app.route('/table/events')
def tableEvent():
    sql_4="select (@id:=@id+1) as id,title,count(`id`) as t from weiboevents,(SELECT @id:=0 )as id_temp group by title"
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    for i in range(len(articles)):
        articles[i]["id"]=int(articles[i]["id"])
    # 遍历文章数据
    # 遍历文章数据
    return render_template('SK2/tables.html', articles=articles) # 渲染模板

@app.route('/table/detail')
def tableEventdetail():
    title = request.args.get('title')
    sql_4= f'SELECT * FROM weiboevents  where title="{title}"'
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    return render_template('SK2/tablesdetail.html', articles=articles, title=title) # 渲染模板

@app.route('/table/add')
def tableaddEvent():
    db = MysqlUtil()
    page = request.args.get('page')
    if page is None:
        page = 0
    m=re.findall("\d+", str(time.strftime("%Y-%m-%d", time.localtime())))
    m=m[0]+m[1]+m[2]
    m=date_delta(m,int(page))
    kk=m[0:4]+"-"+m[4:6]+"-"+m[6:8]
    sql = f'SELECT * FROM weibohotpot  where create_date="{kk}"'
    articles = db.fetchall(sql)  # 获取多条记录
    return render_template('SK2/table_add.html', articles=articles, page=int(page)) # 渲染模板


@app.route('/add',methods=["GET", "POST"])
def addevent():

    import os,csv
    global count
    global kkk
    kkk=kkk+1
    count=0
    save_per_n_page = 5
    event = request.args.get('event')

    keyword=event
    result_file = f'{keyword}.csv'

    if not os.path.exists(result_file):
        with open(result_file, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['wid', 'user_name', 'user_id', 'gender',
                             'publish_time', 'text', 'like_count', 'comment_count',
                             'forward_count','status_city','status_country','status_province'])
    temp_data = []
    empty_times = 0

    for page in range(kkk, kkk+5):  # 瀑布流下拉式，加载
        print(f'page: {page}')
        json_data = get_single_page(page, keyword)
        if json_data == None:
            print('json is none')
            break

        if len(json_data.get('data').get('cards')) <= 0:
            empty_times += 1
        else:
            empty_times = 0
        if empty_times > 3:
            print('\n\n consist empty over 3 times \n\n')
            break
        for result in parse_page(json_data):  # 需要存入的字段

            count=result['counts']
            temp_data.append(result)
        if page % save_per_n_page == 0:
            with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                for d in temp_data:
                    writer.writerow(
                        [d['wid'], d['user_name'], d['user_id'], d['gender'],
                         d['publish_time'], d['text'], d['like_count'], d['comment_count'],
                         d['forward_count'],d['status_city'],d['status_country'],d['status_province']])
            print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')




    return temp_data

@app.route('/addevent')
def paqu():
    event = request.args.get('event')

    return render_template('SK2/charts.html',event=event)





def line_base() -> Line:
    line = (
        Line()
        .add_xaxis(["0.7,1.4,2,3,4"])
        .add_yaxis(
            series_name="爬取数据动态图",
            y_axis=["0"],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line

@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    global idx
    idx = -0.6
    global count
    count=0
    global kkk
    kkk = 0
    return c.dump_options_with_quotes()





@app.route("/lineDynamicData")
def update_line_data():
    global count
    global idx
    idx = idx + 0.7
    return jsonify({"name": round(idx, 1), "value": count, "suan": round(count/idx,1)})


@app.route("/daoru")
def daoru():
    event = request.args.get('event')
    import csv
    import emoji
    title=event
    with open(title+'.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_csv = list(csv_reader)

    for kk in range(len(list_of_csv)-1):
        kk = kk + 1

        ss=list_of_csv[kk][5]
        import demoji
        demoji.download_codes()
        res = emoji.replace_emoji(ss, replace=" ")
        if res!=ss:
            for o in demoji.findall(ss).values():
                res=res+''
                res=res+o
            list_of_csv[kk][5]=res
        sql = "INSERT INTO weiboevents(status_city,status_country,status_province,wid,title,user_id,user_name,gender,publish_time,text,like_count,comment_count,forward_count) \
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%d','%d','%d')" % (list_of_csv[kk][-1], list_of_csv[kk][-2], list_of_csv[kk][-3], list_of_csv[kk][0], title,list_of_csv[kk][2],list_of_csv[kk][1],list_of_csv[kk][3],list_of_csv[kk][4],list_of_csv[kk][5],int(list_of_csv[kk][6]),int(list_of_csv[kk][7]),int(list_of_csv[kk][8]))
        db = MysqlUtil()
        db.insert(sql)
    return jsonify({"name": event, "value": kk})



@app.route("/download1")
def download1():
    from flask import Flask, send_file, Response, send_from_directory
    event = request.args.get('event')
    store_path = event+'.csv'
    def send_file():
         with open(store_path, 'rb') as targetfile:
             while 1:
                data = targetfile.read(10 * 1024 * 1024) # 每次读取10M
                if not data:
                    break
                yield data
    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = ('attachment; filename='+event+'.csv').encode() # 取出下载的名字
#这里的filename是用户下载之后显示的文件名称，可以自己随意修改，而上边的test.xlsx是要你本地的文件，名称必须要对应。
    return response



@app.route('/forward')
def forwardEvent():
    sql_4="select (@id:=@id+1) as id,title,count(`id`) as t from weiboforword,(SELECT @id:=0 )as id_temp group by title"
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    for i in range(len(articles)):
        articles[i]["id"]=int(articles[i]["id"])
    # 遍历文章数据
    # 遍历文章数据
    return render_template('SK2/forward_table.html', articles=articles) # 渲染模板

@app.route('/for_detail')
def forwardEventdetail():
    title = request.args.get('title')
    sql_4= f'SELECT * FROM weiboforword where title="{title}"'
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    return render_template('SK2/forwarddetail.html', articles=articles, title=title) # 渲染模板

@app.route('/for_echart')
def for_echart():
    title = request.args.get('title')
    ll = request.args.get('ll')
    if ll == "sankey":
        ll = "SK2/charts_for.html"
    if ll == "graph":
        ll = "SK2/charts_for_graph.html"
    if ll == "force":
        ll = "SK2/charts_for_force.html"

    return render_template(ll, title=title)
@app.route('/for_echart/sankey', methods=['POST', 'GET'])
def sankey1():
    title = request.args.get('title')
    return sankey(title).dump_options_with_quotes()

@app.route('/for_echart/graph', methods=['POST', 'GET'])
def graph1():
    title = request.args.get('title')
    ll = request.args.get('ll')
    return graph(title,ll).dump_options_with_quotes()
@app.route('/for_add')
def for_addfor():
    from flask import Flask,flash
    wid = request.args.get('wid')

    if wid == "" or wid == None:
        ll = "SK2/forword_add.html"
        flash="请输入mid"
    elif len(wid) == 9 or len(wid) == 16:

        ll = "SK2/forword_add_pa.html"
    else:
        print(len(wid))
        flash="请检查mid是否正确"
        ll = "SK2/forword_add.html"
    return render_template(ll,flash=flash,wid=wid)

@app.route('/addf',methods=["GET", "POST"])
def addfor():
    global count
    wid = request.args.get('wid')


    result_file = f'{wid}.csv'
    if not os.path.exists(result_file):
        with open(result_file, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["wid","source","target","value","publish_time"])
    all_data = []
    temp_data = []
    temp_wid = []
    temp_wid_twice = []
    temp_user_twice = []
    temp_user = []
    empty_times = 0
    json_data = get_single_page1(wid)
    if json_data == None:
        print('json is none')
    for result in parse_page1(json_data):  # 需要存入的字段
        count=result['counts']
        temp_data.append(result)
        temp_wid.append(result['wid'])
        temp_user.append(result['source'])
    all_data=temp_data
    with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        for d in temp_data:
            writer.writerow(
                [d['wid'], d['source'], d['target'], d['value'], d['publish_time']])
    print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')
    time.sleep(random.randint(1, 4))  # 爬取时间间隔
    for i in range(len(temp_wid)):
        temp_data = []

        json_data = get_single_page1(temp_wid[i])
        if json_data == None:
            print('json is none')
            continue
        for result in parse_page_twice(json_data,temp_user[i]):
            temp_data.append(result)
            temp_wid_twice.append(result['wid'])
            temp_user_twice.append(result['source'])
        all_data=all_data+temp_data
        with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
            count=result['counts']
            writer = csv.writer(f)
            for d in temp_data:
                writer.writerow(
                    [d['wid'], d['source'], d['target'], d['value'], d['publish_time']])
        print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')
        time.sleep(random.randint(1, 4))
    for i in range(len(temp_wid_twice)):
        temp_data = []
        json_data = get_single_page1(temp_wid_twice[i])
        if json_data == None:
            print('json is none')
            continue
        for result in parse_page_third(json_data,temp_user_twice[i]):
            count=result['counts']
            temp_data.append(result)
        all_data=all_data+temp_data
        with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:

            writer = csv.writer(f)
            for d in temp_data:
                writer.writerow(
                    [d['wid'], d['source'], d['target'], d['value'], d['publish_time']])
        print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')
        time.sleep(random.randint(1, 4))


    return all_data

@app.route("/daoru2")
def daoru2():
    wid = request.args.get('wid')

    with open(wid+'.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_csv = list(csv_reader)

    for kk in range(len(list_of_csv)-1):
        kk = kk + 1



        sql = "INSERT INTO weiboforword(wid,title,source,target,value,publish_time) \
                           VALUES ('%s', '%s', '%s', '%s','%s','%s')" % (list_of_csv[kk][0],list_of_csv[1][2],list_of_csv[kk][1],list_of_csv[kk][2],list_of_csv[kk][3],list_of_csv[kk][4])
        db = MysqlUtil()
        db.insert(sql)
    return jsonify({"name": wid, "value": kk})



if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0',port=5555)

