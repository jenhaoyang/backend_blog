import os

from flask import Flask

def create_app(test_config=None):
    #產生flask實體並且載入設定
    app = Flask(__name__, instance_relative_config=True)#instance_relative_config告訴flask設定檔在相對於instance資料夾的路徑底下
    app.config.from_mapping(
        SECRET_KEY='dev',#開發用途使用，在正式版的時候會被下面的app.config.from_pyfile讀取的SECRET_KEY覆蓋
        DATABASE=os.path.join(app.instance_path, 'flask_project.sqlite'),#DB路徑
    )

    if test_config is None:
        #非測試的情況下，載入production設定檔，包含機敏資料
        app.config.from_pyfile('config.py')
    else:
        #測試情況下載入傳入的測試設定。
        app.config.from_mapping(test_config)

    #確保instance_path存在，因為flask不會自動產生instance資料夾
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app