from flask import Blueprint, request, Response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json, pdb
from models import User;
from config import db  #SQLAlchemy 数据库实例，用于数据库操作。

user_api = Blueprint('user_api', __name__)

# 注册
@user_api.route('/register', methods=['post'])
def register():

    # 判断用户是否注册
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']

    # 密码加密
    password = generate_password_hash(password)

    # 查询所有的用户名
    result = User.query.filter(User.name == name).all()

    # 如果查询出来的数据长度为0的话，则该用户名没有被注册过
    if len(result) == 0:

        user = User(name=name, password=password, email=email)
        # 将新创建的用户对象添加到数据库会话中，准备提交。
        db.session.add(user)
        # 提交会话，保存更改到数据库。此时，新用户的记录会被插入到数据库中
        db.session.commit()

        # 将字典数据转化为 JSON 字符串。在这里，返回一个表示成功注册的消息
        json_str = json.dumps({'code': 1, 'msg': '注册登陆成功','data': user.name})
        # 实例化的过程需要给他传入响应的内容
        res = Response(json_str)
        # 存储用户数据,设置过期时间
        res.set_cookie('name', user.name)
        return res
    else:
        return jsonify({'code': 0, 'msg': '该用户已被注册'})

# 登陆 
@user_api.route('/login', methods=['post'])
def login():
    
    name = request.form['name']
    password = request.form['password']

    result = User.query.filter(User.name == name).first()
    if result:
        if not  check_password_hash(result.password,password):
            return jsonify({'code': 0, 'msg': '密码错误'})
        else:
            json_str = json.dumps({'code': 1, 'msg': '登陆成功','data': result.name})
            res = Response(json_str)
            res.set_cookie('name', result.name)
            return res
    else:
        return jsonify({'code': 0, 'msg': '用户不存在'})

# 退出登陆
@user_api.route('/logout', methods=['post'])
def logout():
    name = request.cookies.get('name')
    if name:
        json_str = json.dumps({'code': 1, 'msg': '退出登录成功'})
        res = Response(json_str)
        # 删除存储的用户信信息
        res.set_cookie('name', '', expires=0)
        return res
    else:
        return jsonify({'code': 0, 'msg': '未登陆，请先去登陆'})
    
# 基本资料
@user_api.route('/profile', methods=['post'])
def profile():
        # 获取cookies存储的数据
        username = request.cookies.get('name')
        name = request.form['name']
        password = request.form.get('password', '')
        email = request.form['email']
        addr = request.form.get('addr', '')
        # pdb.set_trace()断点调式
        user = User.query.filter(User.name == username).first()
        if user:
            data = {
                'name': name,
                'email': email,
                "addr": addr
            }
            # 判断是否修改密码
            if password:
                password = generate_password_hash(password)
                data['password'] = password
          
            db.session.query(User).filter_by(id=user.id).update(data)
            db.session.commit()
            json_str = json.dumps({'code': 1, 'msg': '修改成功','data': name})
            res = Response(json_str)
            res.set_cookie('name', name)
            return res
        else:
             return jsonify({'code': 0, 'msg': '用户不存在'})
       

# 清空浏览记录
@user_api.route('/delseenlist', methods=['post'])
def delseenlist():
    username = request.cookies.get('name')
    user = User.query.filter(User.name == username).first()
    if user:
        data = {
            'seen_id': None,
        }
        db.session.query(User).filter_by(id=user.id).update(data)
        db.session.commit()
        json_str = json.dumps({'code': 1, 'msg': '删了成功', 'data': username})
        res = Response(json_str)
        return res
    else:
            return jsonify({'code': 0, 'msg': '用户不存在'})