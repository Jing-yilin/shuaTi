from flask import Flask # 导入Flask类
from markupsafe import escape # 防止XSS攻击

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

