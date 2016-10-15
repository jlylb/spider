#!/usr/bin/env python
#coding=utf8
"""
# Author: litc
# Created Time : 2016/1/21 9:28:34
  Last Modified: 2016/1/21 10:35:29
# File Name: app.py
# Description:

"""
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html',data={'name':'hello world'})

if __name__ == '__main__':
    app.run(debug=True)
