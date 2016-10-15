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
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
