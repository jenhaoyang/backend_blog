import os

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    #產生flask實體並且載入設定
    app = Flask(__name__, instance_relative_config=True)#instance_relative_config告訴flask設定檔在相對於instance資料夾的路徑底下
    app.config.from_mapping(
        SECRET_KEY='dev',#開發用途使用，在正式版的時候會被下面的app.config.from_pyfile讀取的SECRET_KEY覆蓋
        DATABASE=os.path.join(app.instance_path, 'flaskBlog.sqlite'),#DB路徑
    )
    CORS(app)
    
    #確保instance_path存在，因為flask不會自動產生instance資料夾
    #注意 這裡使用makedirs，而不是mkdir，因為建立的資料夾可能不只一層
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is None:
        #非測試的情況下，載入production設定檔，包含機敏資料
        #使用silent=True當找不到config.py不會跳錯誤
        app.config.from_pyfile('config.py', silent=True)
    else:
        #測試情況下載入傳入的測試設定。
        app.config.from_mapping(test_config)



    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    #初始化db
    from . import db
    db.init_app(app)

    from. import auth
    app.register_blueprint(auth.bp)

    from. import blog
    app.register_blueprint(blog.bp)
    #將'/'視為使用index endpoint
    app.add_url_rule('/', endpoint='index')

    return app
