from flask import Flask, Blueprint, render_template, redirect
from models import User,House;
from config import db
import pdb

user_page = Blueprint('user_page', __name__)

@user_page.route('/user/<name>')
def index(name):
    # 查询用户
    user = User.query.filter(User.name == name).first()
    if user:

        # 将字符串按逗号分割成 ID 列表
        seen_ids = user.seen_id.split(',') if user.seen_id else []

        # 将 ID 转换为整数（如果存储的是整数 ID）
        item_ids = [int(item_id) for item_id in seen_ids]

        # 数组倒序
        item_ids.reverse()

        seen_house_list = []

        if len(item_ids) > 0:
            # 查询出对应的 浏览历史记录，并按新的顺序排列, db.case() 被优化为在 order_by 中直接应用。使用 db.case() 对 item_ids 中每个 House.id 赋予顺序编号，确保结果按照 item_ids 中的顺序返回。通过 解包操作 *[]，避免了多次操作和冗余代码。enumerate() 用于遍历 item_ids 列表，同时获得每个元素的索引 idx。idx 用作排序的依据，item_id 是每个元素的实际值。
            seen_house_list = House.query.filter(House.id.in_(item_ids)).order_by(
                db.case(
                    *[
                        (House.id == item_id, idx) for idx, item_id in enumerate(item_ids)
                    ]
                )
            ).all()

        # 渲染页面 
        return render_template('user.html', user=user, seen_house_list=seen_house_list)

    else:
        #不存在则跳转回首页
        return redirect('/')

