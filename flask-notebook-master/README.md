# Flask框架开发博客系统

## 12.1需求分析

好记星博客系统应具有以下功能：

1.完整的用户管理模块，包括用户登录和退出登陆等功能。

2.完整的博客管理模块，包括添加博客，编辑博客，删除博客等。

3.完善的会员权限管理，只有登陆的用户才能访问控制台及管理博客。

4.响应式布局，用户在Web端和移动端都能达到较好的阅读体验。

## 12.2系统功能设计

### 12.2.1系统功能结构

博客系统的功能结构主要包括两部分：用户管理和博客管理。

### 12.2.2系统业务流程

以使用游客的身份浏览博客首页，以及博客内容。如果需要管理博客（如：添加编辑博客等），就必须先注册成为会员，登陆网站后才能执行相应的操作。

## 12.3系统开发必备

### 12.3.1系统开发环境

本系统开发环境如下：

操作系统：Windows7及以上

开发工具：Pycharm

数据库：MySQL+PyMySQL驱动

web框架：Flask

第三方模块：WTForms，passlib

## 12.4数据库设计

### 12.4.1数据库概要说明

本项目采用mysql数据库，数据库名称为notebook。创建数据库代码如下：

```
create database notebook default character ser uft8;
```

![1663815771(1)](D:\CodeAndProject\PycharmProjects\flask_related\博客系统\images\1663815771(1).jpg)

### 12.4.2创建数据表

本项目主要涉及到用户和博客两部分，分别创建下表：

user:用户表，用于存储用户信息。

articles:博客表，用于存储博客信息。

创建表sql语句如下：

```sql
use notebook;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
	id int(8) NOT NULL AUTO_INCREMENT,
    username varchar(255) DEFAULT NULL,
    email varchar(255) DEFAULT NULL,
    password varchar(255) DEFAULT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS artciles;
CREATE TABLE articles(
	id int(8) NOT NULL AUTO_INCREMENT,
    title varchar(255) DEFAULT NULL,
   	content text,
    author varchar(255) DEFAULT NULL,
    crate_date datetime DEFAULT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

![1663816688(1)](D:\CodeAndProject\PycharmProjects\flask_related\博客系统\images\1663816688(1).jpg)

users表结构如下：

![1663816765(1)](D:\CodeAndProject\PycharmProjects\flask_related\博客系统\images\1663816765(1).jpg)

articles表结构如下：![image-20220922112019121](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220922112019121.png)

### 12.4.3数据库操作类

在本项目中使用PyMySQ驱动来操作数据库，并实现对博客的增删改查功能。每次执行数据表操作时都需要遵循如下流程：连接数据库-执行sql语句-关闭数据库。

为了复用代码，单独创建一个mysql_util.py文件，其中包括一个MysqlUtil类，用于实现基本的增删改查，代码如下:

```python
import pymysql
# 引入python中的traceback模块，跟踪错误
import traceback
import sys


class MysqlUtil():
    def __init__(self):
        """
            初始化方法，连接数据库
        """

        host = '127.0.0.1'
        user = 'root'
        password = 'wocaonima'
        database = 'notebook'
        self.db = pymysql.connect(
            host=host, user=user, password=password, db=database
        )  # 建立数据库连接

        # 设置游标，并将游标设置成字典类型
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def insert(self, sql):
        """
        插入数据库
        :param sql: 插入数据库是的sql语句
        
        
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 数据库提交
            self.db.commit()
        except Exception:  # 方法一:捕获所有异常
            # 如果发生异常，回滚
            print("发生异常", Exception)
            self.db.rollback()
        finally:
            # 最终数据库关闭
            self.db.close()

    def fetchone(self, sql):
        """
        查询数据库：单个数据集
        fetchone(): 该方法获取下一个查询结果集，结果集是一个对象
        :param sql: 
        :return: 
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except:  # 方法二:采用traceback模块查看异常
            # 输出异常信息
            traceback.print_exc()
            # 如果发生异常，回滚
            self.db.rollback()
            result = 'None'

        finally:
            # 最终数据库关闭
            self.db.close()
        return result

    def fetchall(self, sql):
        """
        查询数据库：多个数据集
        fetchall():接受全部的返回结果行
        :param sql: 
        :return: 
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:  # 方法三:采用sys模块回溯最后的异常
            # 输出异常信息
            info = sys.exc_info()
            print(info[0], ":", info[1])
            # 如果发生异常，回滚
            self.db.rollback()
            results = 'None'
        finally:
            # 最终数据库关闭
            self.db.close()
        return results

    def delete(self, sql):
        """
        删除结果集
        :param sql: 
        :return: 
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 数据库提交
            self.db.commit()
        except:  # 把异常保存到日志文件中， 并分析这些异常
            f = open('\log.txt', 'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            # 如果发生异常，回滚
            self.db.rollback()
        finally:
            # 最终数据库关闭
            self.db.close()

    def update(self, sql):
        """
        更新结果集
        :param sql: 
        :return: 
        """

        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 数据库提交
            self.db.commit()
        except:
            # 如果发生异常，回滚
            self.db.rollback()
        finally:
            # 最终数据库关闭
            self.db.close()
```

## 12.5用户模块设计

用户模块主要包括4部分功能：用户登录，用户注册，退出登录，用户权限管理。这里的用户权限管理是指，只有登陆后用户才能访问到某些页面（如访问台）。

### 12.5.1用户登录功能的实现

用户登录功能主要用于实现网站的会员登录。用户填写正确的用户名和密码，单机“登录”按钮，即可实现会员登录。如果没有输入账户或密码，账户密码长度不正确，都会给予错误提示。

#### 1.创建表单类

用户验证的规则较多，我们使用flask_wtf模块来验证功能。创建forms.py文件，在该文件中创建一个LoginForm类，关键代码如下：

```python
from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from mysql_util import MysqlUtil


# 创建登陆表单类
class LoginForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='请输入用户名'),
            Length(max=25, min=4, message='长度在4-25个字符之间')
        ]
    )

    password = StringField(
        '密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(max=25, min=4, message='长度在6-20个字符之间')
        ]
    )

    def validate_username(self, field):
        # 根据用户名查找user表记录
        sql = "SELECT * FROM user WHERE username = '%s'" % field.data
        db = MysqlUtil()  # 实例化数据库操作类
        result = db.fetchone(sql)  # 获取一条记录
        if not result:
            raise ValidationError("用户名不存在")
```

#### 2.创建模板文件

再/templates/路径下创建login.html模板文件。使用form.username和form.password显示用户名和密码元素。具体代码如下:

```html
{% extends 'layout.html' %}

{% block body %}
<div class="container content">
    <div class="card bg-light" style="width:600px;margin:auto">
        <article class="card-body mx-auto" style="width:400px">
            <h4 class="card-title mt-3 text-center">用户登录</h4>
            {% from "includes/_formhelpers.html" import render_field %}
            <form method="POST" action="">
              {{ form.csrf_token }}
              <div class="form-group">
                {{render_field(form.username, class_="form-control")}}
              </div>
              <div class="form-group">
                {{render_field(form.password, class_="form-control")}}
              </div>
              <div class="form-group">
                <button type="submit" class="btn btn-primary btn-block"> 登录 </button>
              </div>
            </form>
        </article>
    </div>
</div>
{% endblock %}
```

上述模板继承自layout.html:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>在线学习笔记</title>
    <!-- Bootstrap core CSS -->
    <link href="{{ url_for('static', filename='css/bootstrap.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/clean-blog.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
  </head>
  <body>
    {% include 'includes/_navbar.html' %}
    {% include 'includes/_messages.html' %}
    {% block body %}{% endblock %}
    {% include 'includes/_footer.html' %}
    <!-- Bootstrap core JavaScript -->
    <script src="{{ url_for('static', filename='js/jquery.js') }}"></script>
    <script src="{{ url_for('static', filename='js/popper.js') }}"></script>
    <script src="{{ url_for('static', filename='js/bootstrap.js') }}"></script>
  </body>
</html>
```

layout.html中body内引入文件结构如下

![image-20220922124653857](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220922124653857.png)

_footer.html

```html
<div class="footer">
    <div class="footer-nav">
        <a href="/index">首页</a>|
        <a href="#">元素</a>|
        <a href="#">元素</a>|
        <a href="#">元素</a>
    </div>
    <div id="j_footer" class="copy">元素&nbsp;&nbsp;&nbsp;&nbsp;
        <br>元素
    </div>
</div>
<!-- Footer -->
```

_formhelpers.html

```html
{% macro render_field(field) %}
  {{ field.label }}
  {{ field(**kwargs)|safe }}
  {% if field.errors %}
    {% for error in field.errors %}
      <span class="help-inline text-danger">{{ error }}</span>
    {% endfor %}
  {% endif %}
{% endmacro %}
```

_navbar.html

```html
<nav class="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav"
      style="background: #0085a1e8;">
      <div class="container">
        <a class="navbar-brand" href="{{ url_for('index') }}">博客</a>
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          Menu
          <i class="fa fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('index') }}">首页</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('about') }}">关于我们</a>
            </li>
            {% if session.logged_in %}
              <li class="nav-item">
                <a class="nav-link" href="/dashboard">控制台</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/logout">退出</a>
              </li>
            {% else %}
              <li class="nav-item">
                <a class="nav-link" href="/login">登录</a></li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>
```

_messages.html

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
  <div class="message-info" style="margin-top:80px">
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  </div>
  {% endif %}
{% endwith %}

{% if error %}
  <div class="alert alert-danger">{{error}}</div>
{% endif %}

{% if msg %}
  <div class="alert alert-success">{{msg}}</div>
{% endif %}
```

因为要引入一些js和css，所以再static文件下创建js和css文件夹，暂且先加入以下内容

![image-20220922124945829](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220922124945829.png)

3.实现登录功能

当用户填写信息登陆后，如果验证全部通过，需要将登录标识和username写入Session中，为后面判断用户是否登录做准备。此外，还需要在用户访问/login路由时，判断用户是否已将登陆。如果用户之前登陆过，则不需要登陆，否则直接跳转到登陆页面,在app.py中输入以下代码：

```python
from flask import Flask, session, redirect, url_for, request, flash, render_template
from mysql_util import MysqlUtil
from forms import LoginForm
from passlib.hash import sha256_crypt

app = Flask(__name__)


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "logged_in" in session:  # 如果已经登录，则直接跳转到控制台
        return redirect(url_for("dashboard"))

    form = LoginForm(request.form)  # 实例化表单类
    if form.validate_on_submit():   # 如果提交表单，并字段验证通过
        # 从表单中获取字段
        username = request.form['username']
        password_candidate = request.form['password']
        sql = "SELECT * FROM users  WHERE username = '%s'" % (username) # 根据用户名查找user表中记录
        db = MysqlUtil() # 实例化数据库操作类
        result = db.fetchone(sql) # 获取一条记录
        password = result['password']  # 用户填写的密码
        # 对比用户填写的密码和数据库中记录密码是否一致
        if sha256_crypt.verify(password_candidate, password): # 调用verify方法验证，如果为真，验证通过
            # 写入session
            session['logged_in'] = True
            session['username'] = username
            flash('登录成功！', 'success') # 闪存信息
            return redirect(url_for('dashboard')) # 跳转到控制台
        else:  # 如果密码错误
            flash('用户名和密码不匹配！', 'danger')  # 闪存信息

    return render_template('login.html',form=form)
    
    
  @route('/')
def dashboard():
    return '未完待续'


if __name__ == '__main__':
    app.run()
```

上述代码中，首先判断logged_in是否存在于session中，如果存在，则说明用户已将登录，直接调转到控制台，否则使用form.validate_on_submit()函数验证用户提交信息是否满足谁的那个条件。通过验证过，将用户提交的密码和数据库中密码进行匹配，使用sha256_crypt.vertify()方法，第一个参数是用户输入的密码，第二个是数据库加密的密码，如果返回True，则表示密码相同，否则不同

### 12.5.2退出登录功能实现

退出登录功能的实现比较简单，只要清空登录时的session中的值即可。使用session.clear函数来实现：

```python
# 退出
@app.route('/logout/')
@is_logged_in
def logout():
    session.clear()
    flash('你已成功退出', 'success')
    return redirect(url_for('login'))
```

## 12.6博客模块设计

#### 12.6.1博客功能列表实现

博客模块主要包括4部分功能：博客列表、添加博客、编辑博客、和删除博客。用户必须登录后才能执行相应的操作，所以在每一个方法前添加装饰器：

```python
@app.route('/dashboard/')
@is_logged_in
def dashboard():
    db = MysqlUtil
    sql = "SELECT * FROM articles WHERE author = '%s' ORDER BY create_date DESC" % (session['username'])  # 根据用户名查找用户博客，并根据时间降序
    result = db.fetchall(sql)       # 查找所有博客
    if result:  # 若找到，赋值给articles变量
        return render_template('dashboard.html', article=result)
    else:  # 如果博客不存在，提示暂无博客信息
        msg = '暂无博客信息'
        return render_template('dashboard.html', msg=msg)
```

上述代码，需要注意的地方就是使用session函数来获取用户名。根据装饰器判断是否登录

接下来，创建模板文件，关键代码如下：

```html
{% for article in articles %}
  <tr>
    <td>{{article.id}}</td>
    <td>{{article.title}}</td>
    <td>{{article.author}}</td>
    <td>{{article.create_date}}</td>
    <td><a href="edit_article/{{article.id}}" class="btn btn-info" style="float:right">Edit</a></td>
    <td>
      <form action="{{url_for('delete_article', id=article.id)}}" method="post">
        <input type="hidden" name="_method" value="DELETE">
        <input type="submit" value="Delete" class="btn btn-danger">
      </form>
    </td>
  </tr>
{% endfor %}
```

上述代码,articles变量表示所有博客对象，通过for标签来遍历每一个博客对象。

#### 12.6.2添加博客功能实现

在控制台列表页面点击“添加博客”按钮，即可进入添加博客页面，在该页面中，用户需要填写博客标题和内容：

```python
# 添加博客
@app.route('/add_article', methods=['GET', "POST"])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        # 获取表单字段内容
        title = form.title.data
        content = form.content.data
        author = session['username']
        create_date = time.shrftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db = MysqlUtil()
        # 插入数据的sql语句
        sql = "INSERT INTO articles(title,content,author,create_date) \
                      VALUES ('%s', '%s', '%s','%s')" % (title, content, author, create_date)  # 插入数据的SQL语句
        db.insert(sql)
        flash('发布成功', "success")
        return redirect(url_for('dashboard'))
    return render_template('add_article.html',form=form)
```

在上述代码中，接收表单的字段只包含标题和内容，此外，还需要使用session()函数获取用户名，

使用time模块获取当前时间

#### 12.6.3编辑博客功能的实现

在控制台列表中，编辑博客代码如下：

```python
# 编辑笔记
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    db = MysqlUtil()  # 实例化数据库操作类
    fetch_sql = "SELECT * FROM articles WHERE id = '%s' and author = '%s'" % (id, session['username'])  # 根据笔记ID查找笔记信息
    article = db.fetchone(fetch_sql)  # 查找一条记录
    # 检测笔记不存在的情况
    if not article:
        flash('ID错误', 'danger')  # 闪存信息
        return redirect(url_for('dashboard'))
    # 获取表单
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():  # 如果用户提交表单，并且表单验证通过
        # 获取表单字段内容
        title = request.form['title']
        content = request.form['content']
        update_sql = "UPDATE articles SET title='%s', content='%s' WHERE id='%s' and author = '%s'" % (
            title, content, id, session['username'])
        db = MysqlUtil()  # 实例化数据库操作类
        db.update(update_sql)  # 更新数据的SQL语句
        flash('更改成功', 'success')  # 闪存信息
        return redirect(url_for('dashboard'))  # 跳转到控制台

    # 从数据库中获取表单字段的值
    form.title.data = article['title']
    form.content.data = article['content']
    return render_template('edit_article.html', form=form)  # 渲染模板
```

12.6.4删除博客功能实现

```py
# 删除笔记
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    db = MysqlUtil()  # 实例化数据库操作类
    sql = "DELETE FROM articles WHERE id = '%s' and author = '%s'" % (id, session['username'])  # 执行删除笔记的SQL语句
    db.delete(sql)  # 删除数据库
    flash('删除成功', 'success')  # 闪存信息
    return redirect(url_for('dashboard'))  # 跳转到控制台
```



TO BE CONTINUE

gitee:https://gitee.com/laoliNb666/flask-notebook.git