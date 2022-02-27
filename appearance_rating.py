# -*- coding: utf-8 -*-

# 调用百度API完成人脸识别
"""
Created on 2019-06-21
@author: DaDaBaoBaoRen
"""

import requests
import base64
import tkinter.filedialog
import json

def get_access_token(client_id, client_secret):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    response1 = requests.post(url=host, headers=header)  # <class 'requests.models.Response'>
    json1 = response1.json()  # <class 'dict'>
    access_token = json1['access_token']

    return access_token
def open_pic2base64():
    # 本地图片地址，根据自己的图片进行修改
    # 打开本地图片，并转化为base64
    root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
    root.withdraw()  # 将Tkinter.Tk()实例隐藏
    file_path ='./test.png'
    f = open(file_path, 'rb')
    img = base64.b64encode(f.read()).decode('utf-8')
    return img

def bd_rec_face(client_id, client_secret):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {"image": open_pic2base64(), "image_type": "BASE64",
              "face_field": "quality,age,beauty,glasses,gender,race"}
    header = {'Content-Type': 'application/json'}

    access_token = get_access_token(client_id, client_secret)  # '[调用鉴权接口获取的token]'
    request_url = request_url + "?access_token=" + access_token

    request_url = request_url + "?access_token=" + access_token
    response1 = requests.post(url=request_url, data=params, headers=header)
    json1 = response1.json()
    if json1['error_code']!=0:
        print('不露脸，那没办法了')
        return(1,0)
    # print(json.loads(json.dumps(json1)))
    # print("性别为", json1["result"]["face_list"][0]['gender']['type'])
    # print("年龄为", json1["result"]["face_list"][0]['age'], '岁')
    # print("人种为", json1["result"]["face_list"][0]['race']['type'])
    # print("颜值评分为", json1["result"]["face_list"][0]['beauty'], '分/100分')
    # print("是否带眼镜", json1["result"]["face_list"][0]['glasses']['type'])
    # print("脸部模糊度",json1["result"]["face_list"][0]["quality"]['blur'])
    blur = json1["result"]["face_list"][0]["quality"]['blur']
    beauty = json1["result"]["face_list"][0]['beauty']
    score = (blur, beauty)
    return (score)
def fuc():
    # 以下为代码功能测试：
    # 账户id，client_id 为官网获取的AK， client_secret 为官网获取的SK。
    # https://console.bce.baidu.com/ai/?fromai=1#/ai/face/app/list
    client_id = 'AcXMIOyBlGd8IjpCZ7feLgvI'  # ak
    client_secret = 'C6ZfdlulNCL8cSfNfCrljT74nDTPvB4S'  # sk
    # 实例1：人脸识别
    return (bd_rec_face(client_id, client_secret))

if __name__=='__main__':
    fuc()