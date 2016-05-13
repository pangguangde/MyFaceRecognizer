# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from qiniu import BucketManager

import qiniu.config
import string
import random
from scrapy.cmdline import execute

class QiNiuHelper(object):
	"""docstring for QiNiuHelper"""
	def __init__(self, space_name):
		if space_name == 'family':
			self.url_prefix = 'http://o6snbx1fs.bkt.clouddn.com'
		else:
			self.url_prefix = 'http://o6uabmaoe.bkt.clouddn.com'
			space_name = 'unrecognize'
		#需要填写你的 Access Key 和 Secret Key
		self.access_key = 'E9Ododz9fUu9jmqTD_Pz24LPldEmYWwxVWYLLiUD'
		self.secret_key = 'aem0Galcq2F8kMPEqMtNC21rC0q68P4CFAlTYGZt'

		#构建鉴权对象

		#要上传的空间
		self.bucket_name = space_name
		self.q = Auth(self.access_key, self.secret_key)


	def upload_img(self, file_name):


		#上传到七牛后保存的文件名
		key = '%s.jpg' % string.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 16)).replace(' ','');
		
		#生成上传 Token，可以指定过期时间等
		token = self.q.upload_token(self.bucket_name, key, 3600)
		
		#要上传文件的本地路径
		localfile = file_name
		
		ret, info = put_file(token, key, localfile)
		print(info)
		assert ret['key'] == key
		assert ret['hash'] == etag(localfile)
		return '%s/%s' % (self.url_prefix, key)

	def del_img(self, key):
		bucket = BucketManager(self.q)
		ret, info = bucket.delete(self.bucket_name, key)
		print(info)
		assert ret == {}

	def get_all_img_url(self):
		bucket = BucketManager(self.q)
		info = bucket.list(bucket = self.bucket_name, limit = 100, prefix = '', delimiter = '', marker= '')
		for it in info[0]['items']:
			print it['key']
# save_keys = set([
# 	'BFwTyNvDoPlcsqJu.jpg',
# 	'LM3CiUBVdg06bosW.jpg',
# 	'gA8CFh5wTbtpeVXY.jpg',
# 	'hIBPlt2UVNmaxprb.jpg',
# 	'ASP5Zqh3UFjuL4BH.jpg',
# 	'HU4TzvBf9aw2yAE6.jpg',
# 	'uEPTw7Y9DzfBgLMH.jpg',
# 	'yuS40o1kxLCz8dPi.jpg',
# 	'zhbrGiktLTCMd2WQ.jpg',
# 	'AdS2pqEQkNLgHGs9.jpg',
# 	'WIv9h8kErtXb26gS.jpg',
# 	'Sn1AaPQKZ8Of09Bd.jpg',
# 	'I8TbHafh5sC7ycAl.jpg',
# 	'tFVnO43GCpLzR6uD.jpg',
# 	'EiRlK8txuZA9QVSo.jpg',
# 	'8zObgNmhwd0ZicxC.jpg'
# 	])
# all_keys = set([
# 	'01XeWLy8oju7n5K4.jpg',
# 	'8ACOgdeVrnUfkKa2.jpg',
# 	'8zObgNmhwd0ZicxC.jpg',
# 	'ASP5Zqh3UFjuL4BH.jpg',
# 	'AdS2pqEQkNLgHGs9.jpg',
# 	'BFwTyNvDoPlcsqJu.jpg',
# 	'CLAub0oTBtMjGg31.jpg',
# 	'Cb3wI9RiNVzTkduj.jpg',
# 	'EiRlK8txuZA9QVSo.jpg',
# 	'Gp8ef4L3kNThlMID.jpg',
# 	'HU4TzvBf9aw2yAE6.jpg',
# 	'I8TbHafh5sC7ycAl.jpg',
# 	'LM3CiUBVdg06bosW.jpg',
# 	'Mly1OX08JwWtVDZ2.jpg',
# 	'PXM7vINgyciODYKR.jpg',
# 	'Q1wX48H2jAulRhai.jpg',
# 	'SYEZ7wTsv6WX9Rli.jpg',
# 	'Sn1AaPQKZ8Of09Bd.jpg',
# 	'U6y91ItEBivGqgYz.jpg',
# 	'WIv9h8kErtXb26gS.jpg',
# 	'c6tQVlCbxHqzoafA.jpg',
# 	'dxEQgIRrFYK1ei4H.jpg',
# 	'gA8CFh5wTbtpeVXY.jpg',
# 	'hIBPlt2UVNmaxprb.jpg',
# 	'hxSpFKbekzUaCqVI.jpg',
# 	'mngyS50EXiTe6fNk.jpg',
# 	'owPy61siZNQ3gAFk.jpg',
# 	'qW576ItRSVzfKimc.jpg',
# 	'rlCMdhT9Oncqkobv.jpg',
# 	'tFVnO43GCpLzR6uD.jpg',
# 	'tVD3cfFoX8N2bwxk.jpg',
# 	'tcIfKVjWoDmXUSl0.jpg',
# 	'uEPTw7Y9DzfBgLMH.jpg',
# 	'ymCUk97IhHx8FMPN.jpg',
# 	'yuS40o1kxLCz8dPi.jpg',
# 	'zhbrGiktLTCMd2WQ.jpg'
# 	])

# del_keys = list(all_keys - save_keys)

# file_names = [
# # './img/IMG_0478.JPG',
# # './img/IMG_0479.JPG',
# # './img/IMG_0480.JPG',
# './img/IMG_0482.JPG'
# ]

# qnHelper = QiNiuHelper('family')
# # qnHelper.upload_img("./img/cut.jpg")
# # for it in del_keys:
# # 	qnHelper.del_img(it)
# for fname in file_names:
# 	print qnHelper.upload_img(fname)





