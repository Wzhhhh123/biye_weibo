import json
from random import randrange
from mysql_util import MysqlUtil
from flask.json import jsonify
from flask import Flask, render_template,url_for,request,session,flash,redirect
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
from functools import wraps
import random
from py.moxing.ceshi import IsPoOrNeg
from py.uploadre.upload import main1


app = Flask(__name__, static_folder="templates")
CORS(app, resources=r'/*')
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:  # 判断用户是否登录
            return f(*args, **kwargs)  # 如果登录，继续执行被装饰的函数
        else:  # 如果没有登录，提示无权访问
            flash('无权访问，请先登录', 'danger')
            return redirect(url_for('login'))
    return wrap

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


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login1():
    username = request.args.get("name")
    password_candidate = request.args.get("passwd")
    sql = "SELECT * FROM users  WHERE username = '%s'" % (username)  # 根据用户名查找user表中记录
    db = MysqlUtil()  # 实例化数据库操作类
    result = db.fetchone(sql)  # 获取一条记录
    try:
        password = result['password']  # 用户填写的密码
    except:
        return {'message':'用户名和密码不匹配！'}
    # 对比用户填写的密码和数据库中记录密码是否一致
    # if sha256_crypt.verify(password_candidate, password):  # 调用verify方法验证，如果为真，验证通过
    if password == password_candidate:
        # 写入session
        session['logged_in'] = True
        session['username'] = username
        return {'message':'登陆成功！'}
    else:  # 如果密码错误

        return {'message':'用户名和密码不匹配！'}



@app.route('/login.html')
def login():
    if "logged_in" in session:  # 如果已经登录，则直接跳转到控制台
        return redirect(url_for("indqwex"))
    return render_template('/SK2/login.html')

@app.route('/logout/')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('indqwex'))

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
#@is_logged_in
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
    if (articles==()):
        main1()
        db = MysqlUtil()
        sql = f'SELECT * FROM weibohotpot  where create_date="{kk}"'
        articles = db.fetchall(sql)
    db = MysqlUtil()
    count_number = db.fetchall(sql_2)
    sql_6=f'SELECT count(`id`) as t FROM `weiboevents`'
    sql_16=f'SELECT count(`id`) as t FROM `bigevent`'
    sql_17=f'SELECT count(`id`) as t FROM `bigevent_withoutsim`'
    db = MysqlUtil()
    count_eventsnumber_1 = db.fetchall(sql_16)
    db = MysqlUtil()
    count_eventsnumber_2 = db.fetchall(sql_17)
    sql_7=f'SELECT count(`id`) as t FROM `weibohotpot`;'
    db = MysqlUtil()
    count_eventsnumber = db.fetchall(sql_6)
    ttt=count_eventsnumber_1[0]['t']+count_eventsnumber_2[0]['t']+count_eventsnumber[0]['t']
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

    return render_template('SK2/index.html', articles=articles, page=int(page), numbers=count_number, ttt=ttt ,count_hotnumber=count_hotnumber,f=count_famale,m=count_male,chi=zhanbiCHI)  # 渲染模板

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


@app.route('/table/events_up')
def tableEvent_UP():
    sql_4="select (@id:=@id+1) as id,title,count(`id`) as t from bigevent,(SELECT @id:=0 )as id_temp group by title"
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    for i in range(len(articles)):
        articles[i]["id"]=int(articles[i]["id"])
        sql_5="select (@id:=@id+1) as id,title,count(`id`) as t from bigevent_withoutsim,(SELECT @id:=0 )as id_temp group by title"
    db = MysqlUtil()
    es1 = db.fetchall(sql_5)
    for i in range(len(es1)):
        es1[i]["id"]=int(es1[i]["id"])
    # 遍历文章数据
    # 遍历文章数据
    return render_template('SK2/tables_up.html', articles=articles,es1=es1) # 渲染模板
@app.route('/table/detail_up')
def tableEventdetail_UP():
    title = request.args.get('title')
    sql_4= f'SELECT * FROM bigevent  where title="{title}" LIMIT 100'
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    return render_template('SK2/tablesdetail_up.html', articles=articles, title=title) # 渲染模板
@app.route('/table/detail_up_withoutsim')
def tableEventdetail_UP_wit():
    title = request.args.get('title')
    sql_4= f'SELECT * FROM bigevent_withoutsim  where title="{title}" LIMIT 100'
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    return render_template('SK2/tablesdetail_up_wit.html', articles=articles, title=title) # 渲染模板
@app.route('/table/detail')
def tableEventdetail():
    title = request.args.get('title')
    sql_4= f'SELECT * FROM weiboevents  where title="{title}"'
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    return render_template('SK2/tablesdetail.html', articles=articles, title=title) # 渲染模板

@app.route('/table/add')
@is_logged_in
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

def line_base2() -> Line:
    line = (
        Line()
        .add_xaxis(["0.7,1.4,2,3,4"])
        .add_yaxis(
            series_name="上传数据动态图",
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


def line_base1() -> Line:
    line = (
        Line()
        .add_xaxis(["0.7,1.4,2,3,4"])
        .add_yaxis(
            series_name="上传数据动态图",
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
@app.route("/lineChart1")
def get_line_chart1():
    c = line_base1()
    global idxx
    idxx = -0.6
    global kk
    kk = 0
    return c.dump_options_with_quotes()

@app.route("/lineChart2")
def get_line_chart2():
    c = line_base2()
    global idxxx1
    idxxx1 = -0.6
    global kkkkk
    global aIDID
    global acomment
    global pdqinggan
    kkkkk = 0
    aIDID=''
    acomment=''
    pdqinggan=''
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
    global count
    count = 0
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
@is_logged_in
def for_addfor():

    wid = request.args.get('wid')
    flash12 = ""
    if wid == "" or wid == None:
        ll = "SK2/forword_add.html"
        flash12="请输入mid"
    elif len(wid) == 9 or len(wid) == 16:

        ll = "SK2/forword_add_pa.html"
    else:
        flash12="请检查mid是否正确"
        ll = "SK2/forword_add.html"
    return render_template(ll,flash12=flash12,wid=wid)

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
                           VALUES ('%s', '%s', '%s', '%s','%s','%s')" % (list_of_csv[kk][0],wid,list_of_csv[kk][1],list_of_csv[kk][2],list_of_csv[kk][3],list_of_csv[kk][4])
        db = MysqlUtil()
        db.insert(sql)
    return jsonify({"name": wid, "value": kk})



@app.route("/echart")
def echart():
    title = request.args.get('title')
    db = MysqlUtil()
    sql = f'select status_province,count(status_province) as t from weiboevents WHERE title="{title}" group by status_province'
    articles = db.fetchall(sql)  # 获取多条记录
    db = MysqlUtil()
    sql_2=f'select date_format(publish_time, "%Y-%m-%d %H:%i") AS days,COUNT(1) AS total from weiboevents WHERE title="{title}" group by days ORDER BY `days`  ASC'
    hotchange = db.fetchall(sql_2)


    return render_template('daping/index.html',title=title,articles=articles[1:],hotchange=hotchange)

@app.route("/echart_big")
def echart_big():
    title = request.args.get('title')
    db = MysqlUtil()
    sql = f'select `城市`,count(`城市`) as t from bigevent WHERE title="{title}" group by `城市`'
    articles = db.fetchall(sql)  # 获取多条记录
    db = MysqlUtil()
    sql_2=f'select date_format(`发布日期`, "%Y-%m-%d %H:%i") AS days,COUNT(1) AS total from bigevent WHERE title="{title}" group by days ORDER BY `days`  ASC'
    hotchange = db.fetchall(sql_2)
    sql_q = f'select `微博情绪`,count(`微博情绪`) as t from bigevent WHERE title="{title}" group by `微博情绪`'
    db = MysqlUtil()
    qgfb = db.fetchall(sql_q)

    return render_template('daping/index_big.html',title=title,articles=articles[1:],hotchange=hotchange,qgfb=qgfb)

@app.route("/qinggan")
def qinggan():
    chengshi = request.args.get('chengshi')
    title = request.args.get('title')
    db = MysqlUtil()
    sql_2=f'select date_format(`发布日期`, "%Y-%m-%d %H:%i") AS days,COUNT(1) AS total from bigevent WHERE title="{title}" group by days ORDER BY `days`  ASC'
    hotchange = db.fetchall(sql_2)
    sql_q = f'select `微博情绪`,count(`微博情绪`) as t from bigevent WHERE title="{title}" group by `微博情绪`'
    db = MysqlUtil()
    qgfb = db.fetchall(sql_q)

    sql_cs=f'select `微博情绪`,count(`微博情绪`) as t from bigevent WHERE title="{title}" AND `城市`="{chengshi}" group by `微博情绪`'
    db = MysqlUtil()
    qgfb_cs = db.fetchall(sql_cs)
    zong_1=0
    jiji_1=0
    xiaoji_1=0
    zong_2=0
    jiji_2=0
    xiaoji_2=0
    for i in qgfb:
        zong_1+=i['t']
        if i['微博情绪']=='喜悦':
            jiji_1+=i['t']
        if i['微博情绪']=='恐惧':
            xiaoji_1+=i['t']
        if i['微博情绪']=='悲伤':
            xiaoji_1+=i['t']
        if i['微博情绪']=='惊奇':
            jiji_1+=i['t']
        if i['微博情绪']=='愤怒':
            xiaoji_1+=i['t']
    for i in qgfb_cs:
        zong_2+=i['t']
        if i['微博情绪']=='喜悦':
            jiji_2+=i['t']
        if i['微博情绪']=='恐惧':
            xiaoji_2+=i['t']
        if i['微博情绪']=='悲伤':
            xiaoji_2+=i['t']
        if i['微博情绪']=='惊奇':
            jiji_2+=i['t']
        if i['微博情绪']=='愤怒':
            xiaoji_2+=i['t']

    if (jiji_2/zong_2 < jiji_1/zong_1):

        az="偏悲观"
        azz="急需监控是否可能发生舆情事件"
    elif (xiaoji_2/zong_2 < xiaoji_1/zong_1):

        az="偏乐观"
        azz="不易发生舆情事件"
    else:
         az="既不乐观也不悲观"
         azz="需要后续急需观察"
    if (jiji_2 == xiaoji_2):

        az="既不乐观也不悲观"
        azz="需要后续急需观察"

    xiaojilv=xiaoji_2/zong_2
    jijilv=jiji_2/zong_2
    print(xiaoji_1/zong_1,xiaoji_2/zong_2,jiji_1/zong_1,jiji_2/zong_2)
    return render_template('daping/qinggan.html',xiaojilv=round(xiaojilv,5),jijilv=round(jijilv,5),title=title,hotchange=hotchange,qgfb=qgfb,qgfb_cs=qgfb_cs,chengshi=chengshi,az=az,azz=azz)

@app.route("/yuqing")
def ech():
    title = request.args.get('title')
    db = MysqlUtil()

    sql = f'select `城市`,count(`城市`) as t from bigevent WHERE title="{title}" group by `城市`'


    articles = db.fetchall(sql)  # 获取多条记录
    db = MysqlUtil()
    sql_2=f'select date_format(`发布日期`, "%Y-%m-%d %H:%i") AS days,COUNT(1) AS total from bigevent WHERE title="{title}" group by days ORDER BY `days`  ASC'
    hotchange = db.fetchall(sql_2)
    sql_q = f'select `微博情绪`,count(`微博情绪`) as t from bigevent WHERE title="{title}" group by `微博情绪`'
    db = MysqlUtil()
    qgfb = db.fetchall(sql_q)
    sql_y = f'select date_format(`发布日期`, "%Y-%m-%d") AS days,COUNT(1) AS total from bigevent WHERE title="{title}" group by days ORDER BY `days`  ASC'
    db = MysqlUtil()
    yqqx = db.fetchall(sql_y)
    daysyu=[]
    for i in range(len(yqqx)):
        if (i==0):
            kk=int(yqqx[i]['total'])
            continue
        if ((int(yqqx[i]['total'])-kk)/kk > 3):
            daysyu.append(yqqx[i]['days'])


        kk=int(yqqx[i]['total'])
    return render_template('daping/yuqing.html',title=title,articles=articles[1:],hotchange=hotchange,qgfb=qgfb,daysyu=daysyu)




@app.route("/uploud_file")
def upload253523():
     return render_template('elel/upup.html')









@app.route('/checkChunk', methods=['POST'])
def checkChunk():
    return jsonify({'ifExist':False})


@app.route('/mergeChunks', methods=['POST'])
def mergeChunks():
    fileName=request.form.get('fileName')

    md5=request.form.get('fileMd5')
    chunk = 0  # 分片序号
    with open(u'./upload/{}'.format(fileName), 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/{}-{}'.format(md5, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    return jsonify({'upload':True})


@app.route('/upload', methods=['POST'])
def upload():  # 接收前端上传的一个分片
    md5=request.form.get('fileMd5')
    chunk_id=request.form.get('chunk',0,type=int)
    filename = '{}-{}'.format(md5,chunk_id)
    upload_file = request.files['file']
    upload_file.save('./upload/{}'.format(filename))

    return jsonify({'upload_part':True})



@app.route('/file/list', methods=['GET'])
def file_list():
    files = os.listdir('./upload/')  # 获取文件目录
    files = map(lambda x: x if isinstance(x, unicode) else x.decode('utf-8'), files)  # 注意编码
    return render_template('./list.html', files=files)


@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):

    def send_chunk():  # 流式读取
        store_path = './upload/%s' % filename

        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(200000000 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')

@app.route('/upupup', methods=['GET'])
def upupup():
    return render_template('/upup/index.html')

@app.route('/biaozhu')
def biaozhu():
    title = request.args.get('title')
    return render_template('/SK2/biaozhu.html',title=title)



@app.route('/daorubig', methods=['POST', 'GET'])
def daorubig():
    global kk
    name = request.args.get('name')
    try:
        with open('upload/'+name, 'r',encoding='gb18030', errors='ignore') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_csv = list(csv_reader)
    except:
        return jsonify("上传失败")
    if (len(list_of_csv[0])==10):
        for kk in range(len(list_of_csv)-1):
            kk = kk + 1

            sql = "INSERT INTO `bigevent_withoutsim` ( `标题／微博内容`, `信息属性`, `原创/转发`, `地址`, `媒体名称`, `发布日期`, `媒体类型`, `地域`, `全文内容`, `精准地域`,`title`)  \
                               VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                            % (list_of_csv[kk][0],list_of_csv[kk][1],list_of_csv[kk][2],list_of_csv[kk][3],list_of_csv[kk][4],\
                               list_of_csv[kk][5],list_of_csv[kk][6],list_of_csv[kk][7],list_of_csv[kk][8],list_of_csv[kk][9],name)

            db = MysqlUtil()
            db.insert(sql)
    if (len(list_of_csv[0])>10):
        for kk in range(len(list_of_csv)-1):
            kk = kk + 1

            sql = "INSERT INTO `bigevent` ( `标题／微博内容`, `信息属性`, `原创/转发`, `发布日期`, `原微博内容`, `认证类型`, `地域`, `城市`, `性别`, `全文内容`, `粉丝数`, \
            `微博数`, `转`, `评`, `赞`, `话题`, `微博情绪`, `精准地域`, `中图地址`, `title`)  \
                               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')"\
                            % (list_of_csv[kk][0],list_of_csv[kk][1],list_of_csv[kk][2],list_of_csv[kk][3],list_of_csv[kk][4],list_of_csv[kk][5],list_of_csv[kk][6],\
                               list_of_csv[kk][7],list_of_csv[kk][8],list_of_csv[kk][9],list_of_csv[kk][10],list_of_csv[kk][11],list_of_csv[kk][12],list_of_csv[kk][13],list_of_csv[kk][14],list_of_csv[kk][15],list_of_csv[kk][16],list_of_csv[kk][17],list_of_csv[kk][18],name)

            db = MysqlUtil()
            db.insert(sql)
    return jsonify({"name": name, "value": kk})

@app.route("/lineDynamicData1")
def update_line_data1():
    global kk
    global idxx
    idxx = idxx + 0.7
    return jsonify({"name": round(idxx, 1), "value": kk, "suan": round(kk/idxx,1)})

@app.route("/lineDynamicData2")
def update_line_data2():
    global kkkkk
    global idxxx1
    idxxx1 = idxxx1 + 0.7
    global aIDID
    global acomment
    global pdqinggan
    return jsonify({"name": round(idxxx1, 1), "value": kkkkk, "ID": aIDID,  "comment": acomment,  "pdqinggan": pdqinggan, "suan": round(kkkkk/idxxx1,1)})

@app.route('/biaozhu1',methods=["GET", "POST"])
def biaozhu1():
    title = request.args.get('title')
    sql_4= f'SELECT * FROM bigevent_withoutsim  where title="{title}" LIMIT 1000'
    db = MysqlUtil()
    articles = db.fetchall(sql_4)
    for i in range(len(articles)):
        global aIDID
        global kkkkk
        kkkkk=i
        global acomment
        global pdqinggan
        aIDID=articles[i]['ID']
        acomment=articles[i]['全文内容']
        pdqinggan=IsPoOrNeg(acomment)
    return articles

@app.route('/biaozhu2',methods=["GET", "POST"])
def biaozhu2():
    title = request.args.get('title')

    pdqinggan=IsPoOrNeg(title)
    return {"qg":pdqinggan}
if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0',port=5556, threaded=True)

#     UPDATE `bigevent_withoutsim` SET `微博情绪` = '喜悦' WHERE `bigevent_withoutsim`.`ID` = 1
