from flask import Flask,render_template,request
 
app = Flask(__name__)

@app.route('/test',methods=['GET','POST'])
def test():
    s = testDis()
    stop = 0
    # notify(access_token, ('调用地址：','tools_updateTimes'), ('调用名称','修改司机交易测试'),'','','','')
    if s == 'z':
        stop = 1
    return render_template("/test/test.html",s = s,stop=stop)
 
import random
def testDis():
    s =random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
    if s == 'a':
        s = s+'\n'+s
    return s
 
if __name__ == '__main__':
        app.run(host='0.0.0.0')
