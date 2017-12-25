#!/usr/bin/env python
#coding=utf8
"""
# Author: litc
# Created Time : 2016/1/18 15:31:54
  Last Modified: 2016/1/18 15:33:18
# File Name: app.py
# Description:

"""
from flask import Flask
#import MySQLdb
from flask.ext.sqlalchemy import SQLAlchemy

import json
import redis

app = Flask(__name__)

app.config['SECRET_KEY'] ='123456ggdsseee'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@127.0.0.1:3306/nocms'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class Poem(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(100))
    category = db.Column(db.String(100))
    content = db.Column(db.Text)
    zhujie = db.Column(db.Text)

    def __init__(self, title, author,category,content, zhujie):
        self.title = title
        self.author = author
        self.category = category
        self.content = content
        self.zhujie = zhujie


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    #db.create_all()
    #app.run(host='0.0.0.0',port=8000,debug=True)
    r= redis.Redis(host='127.0.0.1', port=6379)
    while r.llen('poem')>0:
        jstr = r.rpop('poem')
        item = json.loads(jstr,encoding='utf-8')
        poem = Poem(**item)
        db.session.add(poem)
        db.session.commit()
