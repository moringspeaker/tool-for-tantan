# -*- encoding=utf8 -*-
__author__ = "15491"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import appearance_rating as ar
import pandas as pd
import time
import datetime

import logging
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)   #避免输出大量log

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Android:///",])

LIMIT_LINE=90   #超级喜欢标准
STANDARD=70     #颜值分及格标准
BLUR=0.7
ROUNDS=100      #一次划多少
Width,Height = poco.get_screen_size()

Time= datetime.datetime.now()
t=Time.strftime("%Y-%m-%d")
names=[]
ages=[]
zodiacs=[]
industries=[]
departments=[]
hometowns=[]
scores=[]
ids=[]
photo_ids=[]
is_shaoji=[]
likes=[]
for i in range(ROUNDS):
    time.sleep(1)
    if poco(name=r"com.p1.mobile.putong:id/cancel").exists():
        poco(name=r"com.p1.mobile.putong:id/cancel").click()
    if poco("com.p1.mobile.putong:id/quickchat_logo_ab").exists():#出现即刻聊天就立即右滑
         swipe(v1=(480,986), vector=[-0.6039, 0.0573])
    if  poco(name=r"com.p1.mobile.putong:id/view_profile_icon").exists():
        snapshot(filename=r'../photos/test'+str(i)+'.png', quality=90, max_size=1200)
        snapshot(filename='../test.png', quality=90, max_size=1200)
        touch((Width*0.9244, Height*0.7895),duration=0.3)
        time.sleep(1)
        name=poco(name="com.p1.mobile.putong:id/name").get_text()
        age=poco(name=r"com.p1.mobile.putong:id/age").get_text()
        if poco(name=r"com.p1.mobile.putong:id/zodiac_type").exists():
            zodiac=poco(name=r"com.p1.mobile.putong:id/zodiac_type").get_text()
        else:
            zodiac='空'
        if poco(name=r"com.p1.mobile.putong:id/industry").exists():
            industry=poco(name=r"com.p1.mobile.putong:id/industry").get_text()
        else:
            industry='空'
        if poco(name=r"com.p1.mobile.putong:id/department").exists():
            department=poco(name=r"com.p1.mobile.putong:id/department").get_text()
        else:
            department='空'
        if poco(name=r"com.p1.mobile.putong:id/hometown").exists():
            hometown=poco(name=r"com.p1.mobile.putong:id/hometown").get_text()
        else:
            hometown='空'
        swipe((Width*0.6,Height*0.8),(Width*0.6,Height*0.2),duration=1)
        swipe((Width*0.6,Height*0.8),(Width*0.6,Height*0.4),duration=1)
        while not poco(name="com.p1.mobile.putong:id/tantan_id_number").exists():
            swipe((Width * 0.6, Height * 0.4), (Width * 0.6, Height * 0.2), duration=1)
        # if poco(text='我的兴趣').exists() and not poco(name=r"com.p1.mobile.putong:id/places_left_bg ").exists():
        #     swipe((Width * 0.6, Height * 0.4), (Width * 0.6, Height * 0.2), duration=1)
        #     swipe((Width * 0.6, Height * 0.5), (Width * 0.6, Height * 0.3), duration=1)
        #
        # elif poco(text='我的兴趣').exists() and poco(name=r"com.p1.mobile.putong:id/places_left_bg ").exists():
        #     swipe((Width * 0.6, Height * 0.4), (Width * 0.6, Height * 0.2), duration=1)

        time.sleep(0.5)
        id=poco(name="com.p1.mobile.putong:id/tantan_id_number").get_text()
        ages.append(age)
        names.append(name)
        zodiacs.append(zodiac)
        industries.append(industry)
        departments.append(department)
        hometowns.append(hometown)
        ids.append(id)
        photo_ids.append(i)
        (blur,beauty)=ar.fuc()#查询颜值
        print(name,age)
        print('颜值：',beauty)
        print('清晰度: ',(1-blur)*100,'%')
        print('*****************分割线*****************')
        if blur>=BLUR:
            is_shaoji.append(1)
            scores.append(beauty)
            likes.append(1)
            poco(name="com.p1.mobile.putong:id/like").child(name="android.widget.ImageView").click()
        elif beauty>=LIMIT_LINE:
            is_shaoji.append(0)
            scores.append(beauty)
            likes.append(1)
            print('我超，大美女！')
            poco(name="com.p1.mobile.putong:id/superlike_btn ").click()
        elif beauty<=STANDARD:
            is_shaoji.append(0)
            scores.append(beauty)
            likes.append(0)
            poco(name="com.p1.mobile.putong:id/dislike").child(name="android.widget.ImageView").click()
        else:
            is_shaoji.append(0)
            scores.append(beauty)
            likes.append(1)
            poco(name="com.p1.mobile.putong:id/like").child(name="android.widget.ImageView").click()
    time.sleep(1)
df=pd.DataFrame({'id':ids,'姓名':names,'年龄':ages,'星座':zodiacs,'行业':industries,'领域':departments,'家乡':hometowns,'photo_id':photo_ids,'颜值':scores,'数一数二？':is_shaoji,'是否喜欢？':likes})
df.to_csv('./'+t+'df.csv')

