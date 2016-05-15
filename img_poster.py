# -*- coding: utf-8 -*-

# hello.py


# test_client.py
import datetime

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

# 在 urllib2 上注册 http 流处理句柄
register_openers()
print datetime.datetime.now()
datagen, headers = multipart_encode({"file": open("img/9.jpg", "rb")})

request = urllib2.Request("http://192.168.0.108:5000/upload_image", datagen, headers)
resp = urllib2.urlopen(request)
print resp.read()
print datetime.datetime.now()
