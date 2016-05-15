# -*- coding: utf-8 -*-

# server.py
# 从wsgiref模块导入:
# from wsgiref.simple_server import make_server
# # 导入我们自己编写的application函数:
# from say_hello import application

# # 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
# httpd = make_server('', 8000, application)
# print "Serving HTTP on port 8000..."
# # 开始监听HTTP请求:
# httpd.serve_forever()
import json
import os
import cv2
import numpy
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from PIL import Image

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		filename = 'tmp.jpg'
		file.save('/Users/pangguangde/Documents/MyFaceRecognizer/tmp/tmp.jpg')
		image = numpy.array(Image.open('/Users/pangguangde/Documents/MyFaceRecognizer/tmp/tmp.jpg'))
		face_cascade = cv2.CascadeClassifier(
			'/Users/pangguangde/Downloads/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(
			gray,
			scaleFactor=1.15,
			minNeighbors=5,
			minSize=(5, 5),
			flags=cv2.CASCADE_SCALE_IMAGE
		)
		return json.dumps({'msg': 'suc', 'face_num': len(faces)})
	return json.dumps({'msg': 'error', 'face_num': None})


if __name__ == '__main__':
	app.run()
