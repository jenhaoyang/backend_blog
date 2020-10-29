import sqlite3

import click
from flask import current_app, g
#g 是flask提供的全域變數，可以用來儲存request期間的資料，每一個request的g都是獨立的因此在多執行續的時候不會出問題。
from flask.cli import with_appcontext
#如果指令是用click產生的, 可以用with_appcontext包起來讓flask cli也可以呼叫

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #讓回傳的資料變成dict的形式，以便使用column名稱取得資料
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    #open_resource:開啟相對於flask_project 資料夾的檔案
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    #刪掉現有的資料並且建立新的table
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db) #告訴flask每個request結束後都要呼叫這個函示
    app.cli.add_command(init_db_command) #告訴flask將這個指令加入