#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: hello.py

# In this tutorial, you will learn how to call Face ++ APIs and implement a
# simple App which could recognize a face image in 3 candidates.
# 在本教程中，您将了解到Face ++ API的基本调用方法，并实现一个简单的App，用以在3
# 张备选人脸图片中识别一个新的人脸图片。

# You need to register your App first, and enter you API key/secret.
# 您需要先注册一个App，并将得到的API key和API secret写在这里。
API_KEY = 'e0e5b6989cf28bd24682d025d9946d21'
API_SECRET = 'cgh0KpSOnTqO1nYlyANtoG529JxNDAGk'
name_map = {
    'pangguangde_1': '庞广德',
    'pangguangde_2': '庞广德',
    'pangguangde_3': '庞广德',
    'pangguangde_4': '庞广德',
    'pangguangde_0': '庞广德',
    'lianglixia_1': '梁丽霞',
    'lianglixia_2': '梁丽霞',
    'lianglixia_3': '梁丽霞',
    'lianglixia_4': '梁丽霞',
    'lianglixia_0': '梁丽霞',
    'pangxianfu_1': '庞先富',
    'pangxianfu_2': '庞先富',
    'pangxianfu_3': '庞先富',
    'pangxianfu_4': '庞先富',
    'pangxianfu_0': '庞先富',
    'wengwenxia_0': '翁文霞',
    'wengwenxia_1': '翁文霞',
    'wengwenxia_2': '翁文霞',
    'wengwenxia_3': '翁文霞',
    'wengwenxia_4': '翁文霞'
}

# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
import time
from pprint import pformat
import datetime
from facepp import File
def print_result(hint, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(k): encode(v) for (k, v) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])

# First import the API class from the SDK
# 首先，导入SDK中的API类
from facepp import API
import os
class RecoHelper(object):
    def __init__(self):
        self.api = API(API_KEY, API_SECRET)
        
        # Here are the person names and their face images
        # 人名及其脸部图片
        self.PERSONS = [
            ('pangguangde_0', 'http://o6snbx1fs.bkt.clouddn.com/EiRlK8txuZA9QVSo.jpg'),
            ('pangguangde_1', 'http://o6snbx1fs.bkt.clouddn.com/BFwTyNvDoPlcsqJu.jpg'),
            ('pangguangde_2', 'http://o6snbx1fs.bkt.clouddn.com/LM3CiUBVdg06bosW.jpg'),
            ('pangguangde_3', 'http://o6snbx1fs.bkt.clouddn.com/gA8CFh5wTbtpeVXY.jpg'),
            ('pangguangde_4', 'http://o6snbx1fs.bkt.clouddn.com/hIBPlt2UVNmaxprb.jpg'),

            ('wengwenxia_0' , 'http://o6snbx1fs.bkt.clouddn.com/ASP5Zqh3UFjuL4BH.jpg'),
            ('wengwenxia_1' , 'http://o6snbx1fs.bkt.clouddn.com/3mRhos2drEe0M7fF.jpg'),
            ('wengwenxia_2' , 'http://o6snbx1fs.bkt.clouddn.com/OgQqUxScZAv8JpbH.jpg'),
            # ('wengwenxia_3' , 'http://o6snbx1fs.bkt.clouddn.com/xq8eLwJn2okpSQXG.jpg'),
            ('wengwenxia_4' , 'http://o6snbx1fs.bkt.clouddn.com/u4k3IBCNDYrcElAT.jpg'),

            ('lianglixia_0' , 'http://o6snbx1fs.bkt.clouddn.com/tFVnO43GCpLzR6uD.jpg'),
            ('lianglixia_1' , 'http://o6snbx1fs.bkt.clouddn.com/HU4TzvBf9aw2yAE6.jpg'),
            ('lianglixia_2' , 'http://o6snbx1fs.bkt.clouddn.com/uEPTw7Y9DzfBgLMH.jpg'),
            ('lianglixia_3' , 'http://o6snbx1fs.bkt.clouddn.com/yuS40o1kxLCz8dPi.jpg'),
            ('lianglixia_4' , 'http://o6snbx1fs.bkt.clouddn.com/zhbrGiktLTCMd2WQ.jpg'),

            ('pangxianfu_0' , 'http://o6snbx1fs.bkt.clouddn.com/Gf6AuYFNwha8S1Vv.jpg'),
            ('pangxianfu_1' , 'http://o6snbx1fs.bkt.clouddn.com/AdS2pqEQkNLgHGs9.jpg'),
            ('pangxianfu_2' , 'http://o6snbx1fs.bkt.clouddn.com/WIv9h8kErtXb26gS.jpg'),
            ('pangxianfu_3' , 'http://o6snbx1fs.bkt.clouddn.com/Sn1AaPQKZ8Of09Bd.jpg'),
            ('pangxianfu_4' , 'http://o6snbx1fs.bkt.clouddn.com/I8TbHafh5sC7ycAl.jpg')
        ]
        self.TARGET_IMAGE = ''
    # Step 1: Create a group to add these persons in
    # 步骤1： 新建一个group用以添加person
    def create_group(self, group_name):
        self.api.group.create(group_name = group_name)
    
    # Step 2: Detect faces from those three images and add them to the persons
    # 步骤2：从三种图片中检测人脸并将其加入person中。 
    def add_persons_to_group(self, group_name):
        for (name, url) in self.PERSONS:
            result = self.api.detection.detect(url = url, mode = 'oneface')
            print_result('Detection result for {}:'.format(name), result)
        
            face_id = result['face'][0]['face_id'] 
        
            # Create a person in the group, and add the face to the person
            # 在该group中新建一个person，并将face加入期中
            self.api.person.create(person_name = name, group_name = group_name,
                    face_id = face_id)
    
    
    # Step 3: Train the group.
    # Note: this step is required before performing recognition in this group,
    # since our system needs to pre-compute models for these persons
    # 步骤3：训练这个group
    # 注：在group中进行识别之前必须执行该步骤，以便我们的系统能为这些person建模
    def training_group(self, group_name):
        result = self.api.recognition.train(group_name = group_name, type = 'all')
    
        # Because the train process is time-consuming, the operation is done
        # asynchronously, so only a session ID would be returned.
        # 由于训练过程比较耗时，所以操作必须异步完成，因此只有session ID会被返回
        print_result('Train result:', result)
    
        session_id = result['session_id']
        
        # Now, wait before train completes
        # 等待训练完成
        while True:
            result = self.api.info.get_session(session_id = session_id)
            if result['status'] == u'SUCC':
                print_result('Async train result:', result)
                break
            time.sleep(1)
        
        #也可以通过调用self.api.wait_async(session_id)函数完成以上功能
    
    
    # Step 4: recognize the unknown face image
    # 步骤4：识别未知脸部图片
    def recognize(self, file_name, group_name):
        print '[DEBUG] %s| recognize begin' % datetime.datetime.now()

        result = self.api.recognition.recognize(img = File(r'%s' % file_name), group_name = group_name)
        # print_result('Recognize result:', result)
        if len(result['face']) == 0:
            os.system('say "no face in the picture"')
        else:
            if result['face'][0]['candidate'][0]['confidence'] >= 15:
                print '[DEBUG] %s| The person with highest confidence: %s, %s' % (datetime.datetime.now(), result['face'][0]['candidate'][0]['person_name'], result['face'][0]['candidate'][0]['confidence'])

            else:
                result['face'][0]['candidate'][0]['person_name'] = 'stranger'
                print result['face'][0]['candidate'][0]['person_name'], result['face'][0]['candidate'][0]['confidence']
            # # Finally, delete the persons and group because they are no longer needed
            # # 最终，删除无用的person和group
            print '[DEBUG] %s| recognize done' % datetime.datetime.now()

            # os.system('say "welcome!!!"')
            name = name_map.get(result['face'][0]['candidate'][0]['person_name'], 'stranger')
            print name
            my_cmd = ''
            if name == 'stranger':
                my_cmd = 'say "stranger"'
            else:
                my_cmd = ('say "Hello!!!%s"' % name) 
            os.system(my_cmd)
            # self.welcome(name, file_name)
            
    def set_target(self, target_url):
        self.TARGET_IMAGE = target_url
        print self.TARGET_IMAGE

    def reco_new_face(self, target_url, group_name):
        self.set_target(target_url)
        self.recognize(group_name)

    def get_group_info(self, group_name):
        result = self.api.group.get_info(group_name = group_name)
        print_result('group info:', result)

    def get_person_info(self, person_name):
        result = self.api.person.get_info(person_name = person_name)
        print_result('person info:', result)

    def welcome(self, name, file_name):
        my_cmd = ''
        if name == 'stranger':
            my_cmd = 'say "stranger"'
        else:
            my_cmd = ('say "Hello!!!%s"' % name) 
        os.system(my_cmd)
        print '[DEBUG] %s| recognize done' % datetime.datetime.now()
        result = self.api.detection.detect(img = File(r'%s' % file_name), mode = 'oneface')
        if len(result['face']) > 0:
            smiling = result['face'][0]['attribute']['smiling']['value']
            gender = result['face'][0]['attribute']['gender']['value']
            print 'smiling value is %s' % smiling
            if gender == 'Female':
                if smiling < 10:
                    os.system('say "哪个不识相的惹了你，我去帮你教育他"')
                else:
                    os.system('say "今天气色不错，你每天都这么漂亮吗"')
            else:
                if smiling < 10:
                    os.system('say "世间唯有美酒佳人不能辜负，要不咱俩喝一杯？"')
                else:
                    if name == '庞广德':
                        os.system('say "卧槽！是谁帅瞎了我的眼睛？"')
                    else:
                        os.system('say "哇！除了广德就是你最帅啦！"')

    # Congratulations! You have finished this tutorial, and you can continue
    # reading our API document and start writing your own App using Face++ API!
    # Enjoy :)
    # 恭喜！您已经完成了本教程，可以继续阅读我们的API文档并利用Face++ API开始写您自
    # 己的App了！
    # 旅途愉快 :)
# names = [
#     'pangguangde_1',
#     'pangguangde_2',
#     'pangguangde_3',
#     'pangguangde_4',
#     'wengwenxia_1',
#     'lianglixia_1',
#     'lianglixia_2',
#     'lianglixia_3',
#     'lianglixia_4',
#     'pangxianfu_1',
#     'pangxianfu_2',
#     'pangxianfu_3',
#     'pangxianfu_4',
#     '庞广德',
#     '梁丽霞',
#     '庞先富'
#     ]
# import numpy as np
# import cv2
# from facepp import File
# # from facepp import facepp.File
# a = RecoHelper()
# # a.create_group('family')
# # a.add_persons_to_group('family')
# # a.training_group('family')
# # for name in names:
# #     a.get_person_info(name)
# # img = open('./img/20.jpg', 'rb')
# ret = a.api.recognition.recognize(img = File(r'%s' % './img/cut.jpg'), group_name = 'family')
# print_result('reco result:', ret)
        