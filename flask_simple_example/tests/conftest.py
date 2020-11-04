import os
import tempfile

import pytest
from flaskBlog import create_app
from flaskBlog.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    #產生一個暫存檔並回傳file object和他的路徑，
    #測試用的sqlite會產生在暫存檔裡
    #測試後關閉並移除
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING':True,
        'DATABASE':db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

#藉由test_client不必啟動server就可以進行測試
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


#許多view都需要測試有沒有檢查使用者已登入，因此我們在這裡建立一個測試登入的class
#藉由對login view 發送POST request來檢查

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')

#有了auth fixture就用auth.login()在測試中登入測試帳號
@pytest.fixture
def auth(client):
    return AuthActions(client)