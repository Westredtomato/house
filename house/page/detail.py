from flask import Blueprint, render_template, redirect,request, jsonify,Response
from models import House, User;
from config import db
import json

detail_page = Blueprint('detail_page', __name__)

@detail_page.route('/house/<int:hid>')
def index(hid):
    # 从数据库中查找房源ID为hid的房源对象
    house = House.query.get(hid)
    if house:
        # 获取房源对象的配套设施信息
        facilities = house.facilities
        # 将配套设施以-作为分割保存在列表facilities_list中
        facilities_list = facilities.split('-')

        # 定义一个用来存放推荐房源的列表变量
        recommend_list = House.query.filter(House.address == house.address).order_by(House.page_views.desc()).limit(6).all()

        # 增加浏览次数
        house.increment_view_count()

        # 获取用户信息
        name = request.cookies.get('name')
        user = User.query.filter(User.name == name).first()

        collection_status = False;

        if user:
            collect_id = user.collect_id
            # 收藏ID
            collect = collect_id.split(',') if collect_id else []
            # 判断是否有收藏 
            collection_status = True  if str(hid) in collect else False

            # 获取浏览ID值
            seen_ids = user.seen_id.split(',') if user.seen_id else []

            # 判断浏览记录有没有
            if str(hid) not in seen_ids:
                seen_ids.append(str(hid))
                data = {
                    'seen_id': ','.join(seen_ids)
                }
                db.session.query(User).filter_by(id=user.id).update(data)
                db.session.commit()
        else:
            collection_status = False

        return render_template('detail.html', house=house, facilities=facilities_list, recommend = recommend_list, collection = collection_status)
    else:
        return redirect('/')
    


# 处理交通有无的情况
def deal_none(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word
    
# 收藏功能
@detail_page.route('/collection/<int:hid>', methods=['post'])
def collection(hid):
    house = House.query.get(hid)
    if house:
        # 获取用户信息
        name = request.cookies.get('name')
        user = User.query.filter(User.name == name).first()

        if user:
            collect_id = user.collect_id
            collect = collect_id.split(',') if collect_id else []
            msg = ''
            # 已收藏
            if str(hid) in collect:
                # remove 移除列表中第一个匹配的元素
                collect.remove(str(hid))
                msg = "取消收藏成功"
            # 未收藏
            else:
                collect.append(str(hid))
                msg = "收藏成功"
            data = {
                'collect_id': ','.join(collect)
            }
            db.session.query(User).filter_by(id=user.id).update(data)
            db.session.commit()
            json_str = json.dumps({'code': 1, 'msg': msg,'data': ''})
            res = Response(json_str)
            return res
        else:
            return jsonify({'code': 0, 'msg': '未登陆，请先去登陆'})   
    else:
        return redirect('/')

detail_page.add_app_template_filter(deal_none, 'dealNone')