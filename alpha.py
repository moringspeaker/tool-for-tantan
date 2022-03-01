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
poco = AndroidUiautomationPoco(use_airtest_input=False, screenshot_each_action=False)

if not cli_setup():
    auto_setup(__file__, logdir=None, devices=["Android:///",])


LIMIT_LINE=90   #超级喜欢标准
STANDARD=65     #颜值分及格标准
BLUR=0.7
ROUNDS=100#一次划多少
Width,Height = poco.get_screen_size()

# Time= datetime.datetime.now()
# t=Time.strftime("%Y-%m-%d-%H")
def detect():
    names = []
    ages = []
    zodiacs = []
    industries = []
    departments = []
    hometowns = []
    scores = []
    ids = []
    photo_ids = []
    is_shaoji = []
    likes = []
    if os.path.exists('./result.csv'):
        df1 = pd.read_csv('./result.csv',encoding='unicode_escape')
        num = df1.shape[0]  # 检测前面一共有几行
    else:
        df1 = pd.DataFrame(columns=['id', '姓名', '年龄', '星座', '行业', '领域', '家乡', 'photo_id', '颜值', '数一数二？', '是否喜欢？'])
        with open("./result.csv", "w",newline='') as f:
            df1.to_csv(f,index=0)
            num=-1
    for i in range(5):
        time.sleep(1)

        if poco(name=r"com.p1.mobile.putong:id/cancel").exists():
            poco(name=r"com.p1.mobile.putong:id/cancel").click()
        if poco("com.p1.mobile.putong:id/quickchat_logo_ab").exists():  # 出现即刻聊天就立即右滑
            swipe(v1=(480, 986), vector=[-0.6039, 0.0573])
        if poco(name=r"com.p1.mobile.putong:id/view_profile_icon").exists():
            snapshot(filename=r'./photos/test' + str(num + i + 1) + '.png', quality=90, max_size=1200)
            snapshot(filename='./test.png', quality=90, max_size=1200)
            try:
                (blur, beauty) = ar.fuc()       # 查询颜值
            except:
                try:
                    (blur, beauty) = ar.fuc()       #再试一次
                except :
                    print('调用接口失败')
                    swipe(v1=(480, 986), vector=[0.6039, 0.0573])  #直接左滑走尝试下一张
                    i-=1
                    continue
            touch((Width * 0.9244, Height * 0.7895), duration=0.3)
            time.sleep(1)
            try:
                name = poco(name="com.p1.mobile.putong:id/name").get_text()
                age = poco(name=r"com.p1.mobile.putong:id/age").get_text()
            except Exception:
                poco(name="com.p1.mobile.putong:id/dislike").child(name="android.widget.ImageView").click() #出现问题立刻不喜欢划走
                i -= 1
                continue
            if poco(name=r"com.p1.mobile.putong:id/zodiac_type").exists():
                zodiac = poco(name=r"com.p1.mobile.putong:id/zodiac_type").get_text()
            else:
                zodiac = '空'
            if poco(name=r"com.p1.mobile.putong:id/industry").exists():
                industry = poco(name=r"com.p1.mobile.putong:id/industry").get_text()
            else:
                industry = '空'
            if poco(name=r"com.p1.mobile.putong:id/department").exists():
                department = poco(name=r"com.p1.mobile.putong:id/department").get_text()
            else:
                department = '空'
            if poco(name=r"com.p1.mobile.putong:id/hometown").exists():
                hometown = poco(name=r"com.p1.mobile.putong:id/hometown").get_text()
            else:
                hometown = '空'
            swipe((Width * 0.6, Height * 0.8), (Width * 0.6, Height * 0.2), duration=1)
            swipe((Width * 0.6, Height * 0.8), (Width * 0.6, Height * 0.4), duration=1)
            while not poco(name="com.p1.mobile.putong:id/tantan_id_number").exists():
                swipe((Width * 0.6, Height * 0.4), (Width * 0.6, Height * 0.2), duration=1)
            time.sleep(0.5)
            id = poco(name="com.p1.mobile.putong:id/tantan_id_number").get_text()
            ages.append(age)
            names.append(name)
            zodiacs.append(zodiac)
            industries.append(industry)
            departments.append(department)
            hometowns.append(hometown)
            ids.append(id)
            photo_ids.append(num + i + 1)
            print(name, age)
            print('颜值：', beauty)
            print('清晰度: ', (1 - blur) * 100, '%')
            print('*****************分割线*****************')
            if blur >= BLUR:
                is_shaoji.append(1)
                scores.append(beauty)
                likes.append(1)
                poco(name="com.p1.mobile.putong:id/like").child(name="android.widget.ImageView").click()
            elif beauty >= LIMIT_LINE:
                is_shaoji.append(0)
                scores.append(beauty)
                likes.append(1)
                print('我超，大美女！')
                poco(name="com.p1.mobile.putong:id/superlike_btn ").click()
            elif beauty <= STANDARD:
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
        else:
            print('找不到按键，界面有问题')
            exit(0)
    df2 = pd.DataFrame.from_dict(
        {'id': ids, '姓名': names, '年龄': ages, '星座': zodiacs, '行业': industries, '领域': departments,
         '家乡': hometowns, 'photo_id': photo_ids, '颜值': scores, '数一数二？': is_shaoji,
         '是否喜欢？': likes})
    with open('./result.csv','a',newline='') as f:
        df2.to_csv(f, mode='a', header=None, index=False)
if __name__=='__main__':
    Tf = time.perf_counter()
    for i in range(ROUNDS):
        detect()
    Ts=time.perf_counter()
    print('程序运行时间:%s秒' % (Ts - Tf))