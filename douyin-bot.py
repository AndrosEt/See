# -*- coding: utf-8 -*-
import sys
import random
import time
from PIL import Image
import ssl
import face_recognition
ssl._create_default_https_context = ssl._create_unverified_context

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)
try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
    from common import apiutil
    from common.compression import resize_image
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

VERSION = "0.0.1"

# 我申请的 Key，随便用，嘻嘻嘻
# 申请地址 http://ai.qq.com
SecretId = '*'
SecretKey = '*'

DEBUG_SWITCH = True
FACE_PATH = 'face/'

adb = auto_adb()
adb.test_device()
config = config.open_accordant_config()

# 审美标准
BEAUTY_THRESHOLD = 80

# 最小年龄
GIRL_MIN_AGE = 18


def yes_or_no():
    """
    检查是否已经为启动程序做好了准备
    """
    while True:
        yes_or_no = str(input('请确保手机打开了 ADB 并连接了电脑，'
                              '然后打开手机软件，确定开始？[y/n]:'))
        if yes_or_no == 'y':
            break
        elif yes_or_no == 'n':
            print('谢谢使用', end='')
            exit(0)
        else:
            print('请重新输入')


def _random_bias(num):
    """
    random bias
    :param num:
    :return:
    """
    print('num = ', num)
    return random.randint(-num, num)


def next_page():
    """
    翻到下一页
    :return:
    """
    cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=config['center_point']['x'],
        y1=config['center_point']['y']+config['center_point']['ry'],
        x2=config['center_point']['x'],
        y2=config['center_point']['y'],
        duration=200
    )
    adb.run(cmd)
    time.sleep(1.5)


def follow_user():
    """
    关注用户
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['follow_bottom']['x'] + _random_bias(10),
        y=config['follow_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)


def thumbs_up():
    """
    点赞
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['star_bottom']['x'] + _random_bias(10),
        y=config['star_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)


def main():
    """
    main
    :return:
    """
    global img
    global imgOrg
    print('程序版本号：{}'.format(VERSION))
    print('激活窗口并按 CONTROL + C 组合键退出')
    debug.dump_device_info()
    screenshot.check_screenshot()

    while True:
        next_page()

        time.sleep(1)
        im = screenshot.pull_screenshot()
        cropped = im.crop((0, 0, 916, 1920))  # (left, upper, right, lower)
        cropped.load()
        cropped.save("./cropped.png")
        cropped.close()
        im.close()

        # resize_image('cropped.png', 'optimized.png', 1024*1024)

        with open('cropped.png', 'rb') as bin_data:
            image_data = bin_data.read()

            # 载入用户上传的图片
        img = face_recognition.load_image_file("cropped.png")
        # 为用户上传的图片中的人脸编码
        unknown_face_encodings = face_recognition.face_encodings(img)
        faceLocations = face_recognition.face_locations(img)



        if len(unknown_face_encodings) > 0:
            # Return the result as json
            result = []
            for face in faceLocations:
                width = face[1] - face[3]
                height = face[2] - face[0]
                quality = ((width + height) / 2 - 150)
                result.append(quality)
            if result[0] > 30:
                ai_obj = apiutil.AiPlat(SecretId, SecretKey)
                rsp = ai_obj.face_detectface(image_data)

        major_total = 0
        minor_total = 0

        # if rsp['ret'] == 0:
        #     beauty = 0
        #     for face in rsp['data']['face_list']:
        #         print(face)
        #         face_area = (face['x'], face['y'], face['x']+face['width'], face['y']+face['height'])
        #         print(face_area)
        #         img = Image.open("optimized.png")
        #         # imgOrg = Image.open("optimized.png")
        #         # 性别判断
        #         if face['beauty'] > beauty and face['gender'] < 50:
        #             beauty = face['beauty']
        #
        #         if face['age'] > GIRL_MIN_AGE:
        #             major_total += 1
        #         else:
        #             minor_total += 1
        #
        #     # 是个美人儿~关注点赞走一波
        #     if beauty > BEAUTY_THRESHOLD and major_total > minor_total:
        #         cropped_img = img.crop(face_area).convert('RGB')
        #         cropped_img.save(FACE_PATH + face['face_id'] + '.png')
        #         # imgOrg.save(FACE_PATH + face['face_id'] + 'a.png')
        #         print('发现漂亮妹子！！！')
        #         # thumbs_up()
        #         # follow_user()
        #
        # else:
        #     print(rsp)
        #     continue


if __name__ == '__main__':
    try:
        # yes_or_no()
        main()
    except KeyboardInterrupt:
        adb.run('kill-server')
        print('谢谢使用')
        exit(0)
