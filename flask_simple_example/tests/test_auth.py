#register view必須成功回傳註冊頁面，並在註冊成功後重新導向到login頁面

import pytest
from flask import g, session
from flaskBlog.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200#檢查頁面成功回傳
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']#檢查成功導向到login頁面

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


#pytest.mark.parametrize告訴pytest使用不同的參數來執行相同的test
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),

))#response.data是儲存在response body的資料，以bytes形式呈現，如果需要轉換成string可以使用get_data(as_text=True)
def  test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


#login view和register的側是很類似。login view要測試登入後user_id 有沒有被儲存到session
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    
#測試logout，並確認user_id從session中移除
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


