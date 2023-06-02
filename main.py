'''
项目名称：基于Python的毛概网页刷题
项目功能：显示题干、选项，在答题者输入答案后，给出正确选项，并记录当前错题编号,并将错题编号写入错题集 data/错题集.csv
'''

import pandas as pd
import numpy as np
import flask
import os

# 读取 ./data/单选题合并.csv
df = pd.read_csv('./data/单选题合并.csv', encoding='utf-8', index_col=0)
# 检查缺失值
# print(df.isnull().sum()) # 0
# 将所有的'答案'列去左右、中间空格
df['答案'] = df['答案'].str.strip()

# 用for循环打印df里的题干和选项
for i in range(len(df)):
    print(f"第{i+1}题：{df['题干'][i]}")
    print(f"A.{df['A'][i]}")
    print(f"B.{df['B'][i]}")
    print(f"C.{df['C'][i]}")
    print(f"D.{df['D'][i]}")
    answer = input("请输入答案：")
    # 输入q退出程序，无视大小写
    if (answer.lower() == 'q'):
        print("退出程序！")
        break
    if (answer == df['答案'][i]):
        print("回答正确！")
    else:
        print(f"回答错误！正确答案为：{df['答案'][i]}")
        # 将错误题目的编号写入错题集
        with open('./data/错题集.csv', 'a', encoding='utf-8') as f:
            f.write(f"{i+1}\n")
        f.close()
    print("="*40, '\n') # 分割线

# 现在我需要一个网页页面来显示题干和选项，然后输入答案，再显示正确答案，最后记录错题编号
# 用flask框架来实现
# 用flask框架来实现
app = flask.Flask(__name__)
# 设置网页标题
app.config['TITLE'] = '毛概刷题'
# 设置网页图标
app.config['FAVICON'] = 'https://www.maozhanggui.cc/favicon.ico'
# 设置网页背景颜色
app.config['BACKGROUND_COLOR'] = '#f8f9fa'
# 设置网页字体颜色
app.config['FONT_COLOR'] = '#212529'
# 设置网页字体
app.config['FONT_FAMILY'] = 'Microsoft YaHei'
# 设置网页字体大小
app.config['FONT_SIZE'] = '16px'
# 设置网页题干字体大小
app.config['TITLE_FONT_SIZE'] = '20px'
# 设置网页选项字体大小
app.config['OPTION_FONT_SIZE'] = '16px'
# 设置网页答案字体大小
app.config['ANSWER_FONT_SIZE'] = '16px'
# 设置网页题干字体颜色
app.config['TITLE_FONT_COLOR'] = '#212529'
# 设置网页选项字体颜色
app.config['OPTION_FONT_COLOR'] = '#212529'
# 设置网页答案字体颜色
app.config['ANSWER_FONT_COLOR'] = '#212529'
# 设置网页题干字体
app.config['TITLE_FONT_FAMILY'] = 'Microsoft YaHei'
# 设置网页选项字体
app.config['OPTION_FONT_FAMILY'] = 'Microsoft YaHei'
# 设置网页答案字体
app.config['ANSWER_FONT_FAMILY'] = 'Microsoft YaHei'
# 设置网页题干字体粗细
app.config['TITLE_FONT_WEIGHT'] = 'bold'