from flask import Flask

#引入数据库配置
from config import Config, db

# 首页
from page.index import index_page
from page.detail import detail_page
from page.user import user_page
from page.list import list_page
from page.query import query_page

# 用户API
from api.user import user_api
from api.detail import detail_api


app = Flask(__name__)
# Flask 会使用 db 来处理数据库交互，并且根据 Config 中的配置来连接到数据库
app.config.from_object(Config)
# Flask 应用加载配置，并初始化数据库连接。
db.init_app(app)

# 注册首页
app.register_blueprint(index_page, url_prefix='/')

# 详情页
app.register_blueprint(detail_page, url_prefix='/')

# 个人中心
app.register_blueprint(user_page, url_prefix='/')

# 列表
app.register_blueprint(list_page, url_prefix='/')

# 注册用户登录与注册接口
app.register_blueprint(user_api, url_prefix='/')

# 搜索页
app.register_blueprint(query_page, url_prefix='/')

# 详情页API
app.register_blueprint(detail_api, url_prefix='/get/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
