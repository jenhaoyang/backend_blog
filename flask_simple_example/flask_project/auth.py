import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flask_project.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth') 
#建立一個auth的blueprint, 需要到create_app裡面將blueprint註冊到app
#第二個參數__name__告訴blueprint被定義的地方
#https://flask.palletsprojects.com/en/1.1.x/api/#blueprint-objects
#url_prefix會將這個blueprint下的所有view function的URL前都會加上/auth


@bp.route('/register', method=('GET', 'POST'))#在 auth blueprint下新增register view function
def register():
    if request.methods == 'POST':# 使用者提交表單時觸發
        username = request.form['username'] #request.form是將使用者提交的form轉換成dict的結果
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is not None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))#generate_password_hash將使用者傳入的密碼以加密形式放入db
            )
            db.commit()
            return redirect(url_for('auth.login'))#成功新增使用者後直接導到登入頁面
            #url_for輸入的參數為viwe function的函式名稱，並且回傳他的URL，如此一來如果以後更改URL就不用更改所有相關的程式了

        flash(error) #flash訊息閃現，訊息不會自己顯示出來，前端必須要用get_flashed_messages把訊息取出，而且會一次取出全部訊息
    
    return render_template('auth/register.html')


@bp.route('/login', method=('GET', 'POST'))
def login():
    if request.method == 'POST'
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')