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
STANDARD=65   #颜值分及格标准
BLUR=0.7
ROUNDS=1000#一次划多少
Width,Height = poco.get_screen_size()
def add_rows(df,l):

    print(l)
    print(df)
    df.loc[len(df)] = l
    return l

def detect():
    if os.path.exists('./result2.csv'):
        df1 = pd.read_csv('./result2.csv',index_col=0)
        num = df1.shape[0]  # 检测前面一共有几行
    else:
        df1 = pd.DataFrame(columns=['id', '姓名', '年龄', '星座', '行业', '领域', '家乡', 'photo_id', '颜值', '数一数二？', '是否喜欢？'])
        df1.to_csv("./result2.csv")
        num=-1
    time.sleep(1)
    if poco(name=r"com.p1.mobile.putong:id/cancel").exists():
        poco(name=r"com.p1.mobile.putong:id/cancel").click()
    if poco("com.p1.mobile.putong:id/quickchat_logo_ab").exists():  # 出现即刻聊天就立即右滑
        swipe(v1=(480, 986), vector=[-0.6039, 0.0573])
    if poco(name=r"com.p1.mobile.putong:id/view_profile_icon").exists():
        snapshot(filename=r'./photos_2/test' + str(num+1) + '.png', quality=90, max_size=1200)
        snapshot(filename='./test.png', quality=90, max_size=1200)
        (blur, beauty) = ar.fuc()  # 查询颜值
        touch((Width * 0.9244, Height * 0.7895), duration=0.3)
        time.sleep(1)
        name = poco(name="com.p1.mobile.putong:id/name").get_text()
        if poco(name="com.p1.mobile.putong:id/name").exists():
            age = poco(name=r"com.p1.mobile.putong:id/age").get_text()
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
        print(name, age)
        print('颜值：', beauty)
        print('清晰度: ', (1 - blur) * 100, '%')
        print('*****************分割线*****************')
        if blur >= BLUR:
            df1 = df1.append([{'id': id, '姓名': str(name), '年龄': age, '星座': zodiac, '行业': industry, '领域': department,
                               '家乡': hometown, 'photo_id': num + 1, '颜值': beauty, '数一数二？': 1, '是否喜欢？': 1}],
                             ignore_index=True)
            poco(name="com.p1.mobile.putong:id/like").child(name="android.widget.ImageView").click()
        elif beauty >= LIMIT_LINE:
            print('我超，大美女！')
            df1 = df1.append([{'id': id, '姓名': str(name), '年龄': age, '星座': zodiac, '行业': industry, '领域': department,
                               '家乡': hometown, 'photo_id': num + 1, '颜值': beauty, '数一数二？': 1, '是否喜欢？': 1}],
                             ignore_index=True)
            poco(name="com.p1.mobile.putong:id/superlike_btn ").click()
        elif beauty <= STANDARD:
            os.remove('./photos_2/test' + str(num+1) + '.png')    #太丑的删掉照片
            df1 = df1.append([{'id': id, '姓名': str(name), '年龄': age, '星座': zodiac, '行业': industry, '领域': department,
                               '家乡': hometown, 'photo_id': num + 1, '颜值': beauty, '数一数二？': 1, '是否喜欢？': 1}],
                             ignore_index=True)
            poco(name="com.p1.mobile.putong:id/dislike").child(name="android.widget.ImageView").click()
        else:
            df1=df1.append([{'id': id, '姓名': str(name), '年龄':age, '星座': zodiac, '行业': industry, '领域': department,
                         '家乡': hometown, 'photo_id': num + 1, '颜值': beauty, '数一数二？': 1, '是否喜欢？': 1}], ignore_index=True)
            poco(name="com.p1.mobile.putong:id/like").child(name="android.widget.ImageView").click()
            time.sleep(1)
    else:
        print('找不到按键，界面有问题')
        swipe(v1=(480, 986), vector=[-0.6039, 0.0573])
        return 0
    df1.to_csv('result2.csv')
if __name__=='__main__':
    Tf = time.perf_counter()
    for i in range(ROUNDS):
        try:
            detect()
        except:
            try:
                poco(name="com.p1.mobile.putong:id/dislike").child(name="android.widget.ImageView").click()
                time.sleep(1)
                continue
            except:
                swipe(v1=(480, 986), vector=[-0.6039, 0.0573])
                time.sleep(1)
                continue
    Ts=time.perf_counter()
    print('程序运行时间:%s秒' % (Ts - Tf))