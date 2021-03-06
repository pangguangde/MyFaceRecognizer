import cv2  
import threading
# from qiniu_test import QiNiuHelper
from facepp import API
from hello import RecoHelper
import os
import numpy as np
from facepp import File
import datetime, time
import thread
from picamera import PiCamera
from picamera.array import PiRGBArray

# from tornado.httpclient import AsyncHTTPClient

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

glob_flag = False

exit_dict = {'庞广德': 1}

def wait_for_ESC():
    while True:
        if cv2.waitKey(10)==27:
            glob_flag = True
            thread.exit_thread()

def upload_and_reco(filename):
    # qiniuHelper = QiNiuHelper('test')
    # url = qiniuHelper.upload_img(filename)
    recoHelper = RecoHelper()
    return recoHelper.recognize(filename, 'family')

def getCam():  
    # window_name='show image'
    # http_client = AsyncHTTPClient()

    # face_cascade = cv2.CascadeClassifier('/Users/pangguangde/Downloads/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
    # cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(window_name, 1920, 1080)
    # video_cap_obj=cv2.VideoCapture(0)
    # if video_cap_obj==None:
    #     print('video caoture error')
    # if video_cap_obj.open(0)==False:
    #     print('open error')
    # retval,image=video_cap_obj.read()
    
    # thread.start_new_thread(wait_for_ESC, ())
    camera = PiCamera()
    register_openers()
    while True:
        # if glob_flag:
        #     break
        # retval,image=video_cap_obj.read()
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imwrite("./img/tmp.jpg", image)

        print '[DEBUG] %s| scanning...' % datetime.datetime.now()
        datagen, headers = multipart_encode({"file": open("./img/tmp.jpg", "rb")})

        request = urllib2.Request("http://192.168.0.108:5000/upload_image", datagen, headers)
        resp = urllib2.urlopen(request)

        ret = resp.read()
        face_num = eval(ret).get('face_num', 0)
        # print ret
        # print datetime.datetime.now()

        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.15,
        #     minNeighbors=5,
        #     minSize=(5,5),
        #     flags=cv2.CASCADE_SCALE_IMAGE
        # )
        
        
        if face_num > 0:
            print '[DEBUG] %s| I have read your face, uploading...' % datetime.datetime.now()
            cv2.imwrite("./img/cut_1.jpg", image) 
            img = image
            img = np.array(img)
            mean = np.mean(img)
            img = img - mean 
            img = img+mean*1.6
            save_name = "./img/cut.jpg"
            cv2.imwrite(save_name, img) 
            name = upload_and_reco(save_name)
            if exit_dict.get(name, 0) == 1:
                break
        # cv2.imshow(window_name, image)
        # if cv2.waitKey(5) == 27:
        #     break
        
    # video_cap_obj.release()
    # cv2.waitKey()
    # retval,image=video_cap_obj.read() 
    # cv2.destroyAllWindows()
    # video_cap_obj.release() 
    # th.join() 
      
if __name__=='__main__':  
    getCam()
    # img = cv2.imread('./img/cut_1.jpg',0)  
    # print img
    # img = np.array(img)  
    # mean = np.mean(img)  
    # img = img - mean  

    # img = img+mean*0.8
    # cv2.imwrite("./img/cut_2.jpg", img) 
    # img = img+mean*1
    # cv2.imwrite("./img/cut_3.jpg", img) 
    # img = img+mean*1.5
    # cv2.imwrite("./img/cut_4.jpg", img) 
    # img = img+mean*2
    # cv2.imwrite("./img/cut_5.jpg", img) 


