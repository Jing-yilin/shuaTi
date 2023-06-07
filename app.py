from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for

# from markupsafe import escape
import pandas as pd
import os
import yaml
import json

from flask_sqlalchemy import SQLAlchemy
import pymysql 
pymysql.install_as_MySQLdb()

user_config_path = './userconfig/'

def read_config(username):
    with open(f"{user_config_path}{username}config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        count_right_single = config["count_right_single"]
        count_wrong_single = config["count_wrong_single"]
        current_single = config["current_single"]
        right_id_list_single = config["right_id_list_single"]
        wrong_id_list_single = config["wrong_id_list_single"]
        count_right_multi = config["count_right_multi"]
        count_wrong_multi = config["count_wrong_multi"]
        current_multi = config["current_multi"]
        right_id_list_multi = config["right_id_list_multi"]
        wrong_id_list_multi = config["wrong_id_list_multi"]
    return (count_right_single, count_wrong_single, current_single, right_id_list_single, wrong_id_list_single), (count_right_multi, count_wrong_multi, current_multi, right_id_list_multi, wrong_id_list_multi), config


def create_config(username):
    with open(f"{user_config_path}{username}config.yaml", "w", encoding="utf-8") as f:
        f.write(
            "count_right_single: 0\ncount_wrong_single: 0\ncurrent_single: 0\nright_id_list_single: []\nwrong_id_list_single: []\ncount_right_multi: 0\ncount_wrong_multi: 0\ncurrent_multi: 0\nright_id_list_multi: []\nwrong_id_list_multi: []"
        )


def read_single():
    # 读取单选题
    singles = pd.read_csv("./data/maogai/单选题合并.csv", encoding="utf-8", index_col=0)
    singles["答案"] = singles["答案"].str.strip().replace(
        " ", "")  # 将所有的'答案'列去左右、中间空格
    # df的加上一个序号列
    singles.insert(0, "序号", range(1, len(singles) + 1))
    # Index(['序号', '题干', 'A', 'B', 'C', 'D', '答案'], dtype='object')
    # 将df转换为字典
    singles = singles.to_dict(orient="records")
    return singles


def read_multi():
    # 读取多选题
    multis = pd.read_csv("./data/maogai/多选题合并.csv", encoding="utf-8", index_col=0)
    multis["答案"] = multis["答案"].str.strip().replace(
        " ", "")  # 将所有的'答案'列去左右、中间空格
    multis.insert(0, "序号", range(1, len(multis) + 1))
    multis = multis.to_dict(orient="records")
    return multis


def read_user_json():
    with open("./user.json", "r", encoding="utf-8") as f:
        users = json.load(f)
        # print(users)
    return users

def check_user_exist(username, password):
    if username is None or password is None:
        return False
    user_exist = False
    users = read_user_json()
    for item in users:
        if username == item["username"] and password == item["password"]:
            user_exist = True
            break
    return user_exist


users = read_user_json()
singles = read_single()
multis = read_multi()

# 针对每个用户创建一个配置文件
for user in users:
    username = user['username']
    # 如果 config.yaml 不存在，新建一个
    if not os.path.exists(f"./{username}config.yaml"):
        create_config(username)

# (count_right_single, count_wrong_single, current_single, right_id_list_single, wrong_id_list_single), (count_right_multi,
#                                                                                                        count_wrong_multi, current_multi, right_id_list_multi, wrong_id_list_multi), config = read_config()


app = Flask(__name__)

# # TODO: 不再使用用户配置文件yaml，而是使用数据库,数据库中有2张表single和multi，每张表中都有id, question, a, b, c, d answer
# # 连接mysql数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jingyl@localhost:3306/maogai'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # 创建数据库模型
# class Single(db.Model):
#     __tablename__ = 'single'
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String(1024), nullable=False)
#     a = db.Column(db.String(512), nullable=False)
#     b = db.Column(db.String(512), nullable=False)
#     c = db.Column(db.String(512), nullable=False)
#     d = db.Column(db.String(512), nullable=False)
#     answer = db.Column(db.String(1), nullable=False)

#     def __repr__(self):
#         return '<Single %r>' % self.question
    
# class Multi(db.Model):
#     __tablename__ = 'multi'
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String(1024), nullable=False)
#     a = db.Column(db.String(512), nullable=False)
#     b = db.Column(db.String(512), nullable=False)
#     c = db.Column(db.String(512), nullable=False)
#     d = db.Column(db.String(512), nullable=False)
#     answer = db.Column(db.String(8), nullable=False)

#     def __repr__(self):
#         return '<Multi %r>' % self.question
    
# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     current_single = db.Column(db.Integer, nullable=False)
#     current_multi = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.question

# # 读取数据库中的single表的id=1的数据
# single = Single.query.filter_by(id=1).first()
# print(single.question)



@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/usercheck")
def user_check():
    username = request.args.get("username")
    password = request.args.get("password")
    user_exist = False
    # 对比users中的账号密码
    for item in users:
        if username == item["username"] and password == item["password"]:
            user_exist = True
            resp = make_response(redirect(url_for("single")))
            # 设置cookie
            resp.set_cookie('username', username)
            resp.set_cookie('password', password)
            return resp
    if not user_exist:
        return "<h1>用户不存在或密码错误!</h1>"


@app.route("/single", methods=["GET"])
def single():
    # 读取cookie进行校验
    cookies = request.cookies
    username = cookies.get('username')
    password = cookies.get('password')
    if not check_user_exist(cookies['username'], cookies['password']):
        print("未检测到cookie，用户未登录过")
        resp = make_response(redirect(url_for("login")))
        return resp
    # print(request.args)
    wrong = request.args.get("wrong")
    print(f"wrong: {wrong}")
    last = (
        request.args.get("amp;last")
        if request.args.get("amp;last") is not None
        else request.args.get("last")
    )
    print(f"last: {last}")
    next = (
        request.args.get("amp;next")
        if request.args.get("amp;next") is not None
        else request.args.get("next")
    )
    reset = request.args.get("reset")
    # 读取config.yaml
    (count_right_single, count_wrong_single, current_single,
     right_id_list_single, wrong_id_list_single), _, config = read_config(username)

    if wrong == "1":  # 错误
        print(f"选择错误，序号为{current_single}")
        if current_single in right_id_list_single:
            right_id_list_single.remove(current_single)
            count_right_single -= 1
        if current_single not in wrong_id_list_single:
            wrong_id_list_single.append(current_single)
            count_wrong_single += 1
    elif wrong == '0':  # 正确
        print(f"选择正确，序号为{current_single}")
        if current_single in wrong_id_list_single:
            wrong_id_list_single.remove(current_single)
            count_wrong_single -= 1
        if current_single not in right_id_list_single:
            right_id_list_single.append(current_single)
            count_right_single += 1
    else:
        print(f"未选择，序号为{current_single}")

    # 判断是否要回到上一题
    if last == "1" and current_single > 0:
        current_single -= 1
    elif next == "1":
        current_single += 1
    else:
        pass

    if reset == "1":
        current_single = 0
        count_right_single = 0
        count_wrong_single = 0
        right_id_list_single = []
        wrong_id_list_single = []

    # 修改{username}config.yaml
    with open(f"./{username}config.yaml", "w") as f:
        config["count_right_single"] = count_right_single
        config["count_wrong_single"] = count_wrong_single
        config["current_single"] = current_single
        config["right_id_list_single"] = right_id_list_single
        config["wrong_id_list_single"] = wrong_id_list_single
        yaml.dump(config, f)

    return render_template(
        "single.html",
        single=singles[current_single],
        count_wrong=count_wrong_single,
        count_right=count_right_single,
        total_single=len(singles),
    )


@app.route("/multi", methods=["GET"])
def multi():
    # 读取cookie进行校验
    cookies = request.cookies
    username = cookies.get('username')
    password = cookies.get('password')
    if not check_user_exist(cookies['username'], cookies['password']):
        print("未检测到cookie，用户未登录过")
        resp = make_response(redirect(url_for("login")))
        return resp
    # print(request.args)
    wrong = request.args.get("wrong")
    print(f"wrong: {wrong}")
    last = (
        request.args.get("amp;last")
        if request.args.get("amp;last") is not None
        else request.args.get("last")
    )
    print(f"last: {last}")
    next = (
        request.args.get("amp;next")
        if request.args.get("amp;next") is not None
        else request.args.get("next")
    )
    reset = request.args.get("reset")
    # 读取config.yaml
    _, (count_right_multi, count_wrong_multi, current_multi,
        right_id_list_multi, wrong_id_list_multi), config = read_config(username)

    if wrong == "1":  # 错误
        print(f"选择错误，序号为{current_multi}")
        if current_multi in right_id_list_multi:
            right_id_list_multi.remove(current_multi)
            count_right_multi -= 1
        if current_multi not in wrong_id_list_multi:
            wrong_id_list_multi.append(current_multi)
            count_wrong_multi += 1
    elif wrong == '0':  # 正确
        print(f"选择正确，序号为{current_multi}")
        if current_multi in wrong_id_list_multi:
            wrong_id_list_multi.remove(current_multi)
            count_wrong_multi -= 1
        if current_multi not in right_id_list_multi:
            right_id_list_multi.append(current_multi)
            count_right_multi += 1
    else:
        print(f"未选择，序号为{current_multi}")

    # 判断是否要回到上一题
    if last == "1" and current_multi > 0:
        print("curren_multi-1, 上一题")
        current_multi -= 1
    elif next == "1" and current_multi < len(multis) - 1:
        print("curren_multi+1, 下一题")
        current_multi += 1
    else:
        pass

    if reset == "1":
        current_multi = 0
        count_right_multi = 0
        count_wrong_multi = 0
        right_id_list_multi = []
        wrong_id_list_multi = []

    # 修改config.yaml
    with open(f"./{username}config.yaml", "w") as f:
        config["count_right_multi"] = count_right_multi
        config["count_wrong_multi"] = count_wrong_multi
        config["current_multi"] = current_multi
        config["right_id_list_multi"] = right_id_list_multi
        config["wrong_id_list_multi"] = wrong_id_list_multi
        yaml.dump(config, f)

    return render_template(
        "multi.html",
        multi=multis[current_multi],
        count_wrong=count_wrong_multi,
        count_right=count_right_multi,
        total_multi=len(multis),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
