#!/usr/bin/env python
#coding=utf8

import redis

r = redis.Redis(host='127.0.0.1', port=6379,decode_responses=True)

print r.get('name')

with open('./logo.json','r') as f:
    for line in f.readlines():
        #print(line.strip())
        r.lpush('poem',line)

