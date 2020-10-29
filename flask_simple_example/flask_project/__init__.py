import os

from flask import Flask

def create_app(test_config=None):
    #產生flask實體並且載入設定
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',#開發用途使用，在正式版的時候會被下面的app.config.from_pyfile讀取的SECRET_KEY覆蓋
        DATABASE=os.path.join(app.instance_path, 'flask_project.sqlite'),
    )

    if test_config is None:
        #非測試的情況下，載入普通設定檔
        app.config.from_pyfile('config.py')
    else:
        #測試情況下載入傳入的測試設定。
        app.config.from_mapping(test_config)

    #確保instance_path存在
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    print(app.instance_path)
    print(app.config['SECRET_KEY'])

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app