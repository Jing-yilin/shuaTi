from flask import Flask, render_template, request, jsonify
# from markupsafe import escape
import pandas as pd
# from flask_sqlalchemy import SQLAlchemy
# import click

# 读取单选题
singles = pd.read_csv('./data/单选题合并.csv', encoding='utf-8', index_col=0)
singles['答案'] = singles['答案'].str.strip().replace(' ', '') # 将所有的'答案'列去左右、中间空格
# df的加上一个序号列
singles.insert(0, '序号', range(1, len(singles)+1))
# Index(['序号', '题干', 'A', 'B', 'C', 'D', '答案'], dtype='object')
# 将df转换为字典
singles = singles.to_dict(orient='records')

# 读取多选题
multis = pd.read_csv('./data/多选题合并.csv', encoding='utf-8', index_col=0)
multis['答案'] = multis['答案'].str.strip().replace(' ', '') # 将所有的'答案'列去左右、中间空格
multis.insert(0, '序号', range(1, len(multis)+1))
multis = multis.to_dict(orient='records')

# 新建错题本
wrong = pd.DataFrame(columns=['序号', '题干', 'A', 'B', 'C', 'D', '答案', '错误次数'])
wrong.to_csv('./data/错题本.csv', encoding='utf-8')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('single.html', single=singles[0], id=0)

@app.route('/single/<id>', methods=['GET'])
def single(id):
    return render_template('single.html', single=singles[int(id)], id=id)