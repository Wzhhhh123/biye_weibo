import json
from random import randrange

from flask.json import jsonify
from flask import Flask, render_template
from flask import request
import pandas as pd
import requests
import re
from pyecharts import options as opts
from pyecharts.charts import Line

from myScripts.mapchina import render_mapcountChina
from myScripts.mapworld import render_mapcountWorld
from myScripts.lineCountry import render_lines
from myScripts.jiebafenci import render_wordcloud
from myScripts.weiboAnalyse import weiboWordcloud

n = "dataSets/countrydata.csv"
data = pd.read_csv(n)
date_list = list(data[data['countryName'] == '中国']['dateId'])
countrylist = list(data[data['dateId'] == 20200412]['countryName'])
countrylist = ['中国'] + countrylist
# print(date_list)
# print(countrylist)

app = Flask(__name__, static_folder="templates")


@app.route("/login")
def index():
    return render_template("index_123.html",cates = countrylist)

@app.route("/")
def login():
    return render_template("/login/index.html",cates = countrylist)

@app.route("/es")
def es():
    return render_template("test00.html",cates = countrylist)

@app.route("/es2")
def es2():
    return render_template("test03.html",cates = countrylist)

@app.route("/es3")
def es3():
    return render_template("test04.html",cates = countrylist)

@app.route("/es4")
def es4():
    return render_template("test05.html",cates = countrylist)


@app.route("/yiqing1")
def yiqing1():
    return render_template("/yiqing1/index.html")


@app.route("/yiqing2")
def yiqing2():
    return render_template("/yiqing2/index.html")



@app.route("/document")
def document():
    return render_template("README.html")


@app.route("/nlp")
def nlpNotebook():
    return render_template("NLP.html")


@app.route("/analyse")
def anaNotebook():
    return render_template("analyse.html")


@app.route("/worldmap", methods=['POST', 'GET'])
def get_world_map():
    if request.method == 'GET':
        maptype = int(request.args.get('type', ''))
        i = int(request.args.get('index', ''))
        print(maptype)
        print(i)
        return render_mapcountWorld(date_list[int(i)], maptype).dump_options_with_quotes()


@app.route("/chinamap", methods=['POST', 'GET'])
def get_china_map():
    if request.method == 'GET':
        maptype = int(request.args.get('type', ''))
        i = int(request.args.get('index', ''))
        print(maptype)
        print(i)
        return render_mapcountChina(date_list[int(i)], maptype).dump_options_with_quotes()


@app.route("/lines")
def get_line_chart():
    return render_lines('中国').dump_options_with_quotes()


@app.route("/wordcloud", methods=['POST', 'GET'])
def get_word_chart():
    if request.method == 'GET':
        i = request.args.get('value', '')
        if not i:
            i = 0
        print(i)
        return render_wordcloud(i).dump_options_with_quotes()


@app.route("/weiboCloud", methods=['POST', 'GET'])
def get_weibo_chart():
    if request.method == 'GET':
        i = request.args.get('value', '')
        if not i:
            i = 0
        print(i)
        return weiboWordcloud(i).dump_options_with_quotes()


@app.route('/changecountry', methods=['POST', 'GET'])
def changeCountry():
    if request.method == 'GET':
        selectCountry = request.args.get('value', '')
        print(selectCountry)
        return render_lines(selectCountry).dump_options_with_quotes()


# 情感分析
@app.route('/sentimentAnalysis', methods=['GET'])
def sentimentAnalysis():
    data = pd.read_json("data_process/out.json")
    dataArr = {}

    areas = {"东北": [], "华东": [], "华中": [], "华北": [], "华南": [], "西北": [], "西南": []}
    arr = ["东北", "华东", "华中", "华北", "华南", "西北", "西南"]
    date = []
    for key, value in data.items():
        for k, v in value.items():
            areas[key].append(v)
            date.append(k)
    date = date[0:12]
    print(date)
    print(areas)
    return render_template("SentimentAnalysis.html", data=areas, arr=arr, date=date)


@app.route("/NLPP")
#定义方法 用jinjia2引擎来渲染页面，并返回一个index.html页面
def root():
    return render_template("NLPP.html")

@app.route("/submit",methods=["GET", "POST"])
def submit():
    #由于POST、GET获取数据的方式不同，需要使用if语句进行判断
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
    if request.method == "GET":
        name = request.args.get("name")
        age = request.args.get("age")
    print(name+age)
    #如果获取的数据为空
    if age != "weibo.marshal.3":
        return {'message':"读取模型失败，请确认路径"} 
    if name != None:
        session = requests.session()
        import json

        import pandas as pd
        try:
            df = pd.read_csv(name)
        except:
            return {'message':"读取数据集失败，请确认路径"} 
        df = df.loc[:, ["地区", "日期", "emotional"]]
        print(df.values.tolist())
        def dateConversion(days):
            year = month = day = 0
            if days > 365:
                year = days // 365
                if (days * year) / 30 < 1:
                    day = (days - 365 * year) % 30
                if (days * year) / 30 >= 1:
                    day = (days - 365 * year) % 30
                    month = (days - 365 * year) // 30
            elif days < 365 and days > 30:
                month = days // 30
                day = days % 30
            else:
                day = days
                return f"1月{day}日"
            if day == 0:
                day = 1
            return f"{month}月{day}日"

        areas = ["东北", "华东", "华中", "华北", "华南", "西北", "西南"]
        dic = {}
        for area, date, emo in df.values.tolist():
            if area not in dic:
                dic.update({area: {}})
            print(area, date, emo)
            tmp = dic.get(area)
            tmp.update({dateConversion(date): emo})
            dic.update({area: tmp})

        json_data = json.dumps(dic, ensure_ascii=False)
        with open("./out.json", "w", encoding="utf-8") as f:
            f.write(json_data)

        print(dic)

        
        #return {'message':"succes11s!",'id':1,'xc':dic} 
        return {'message':"success!",'id':1,'xc':dic}
    
    if age == None:
        

        return {'message':"success!",'name':"kk",'username':"ss"}

if __name__ == "__main__":
    app.run()
