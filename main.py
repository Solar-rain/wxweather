import random
from time import time, localtime

import requests
from bs4 import BeautifulSoup

import cityinfo
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token


def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]

    ##===================================================================================
    headers1 = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    HTML = "https://tianqi.2345.com/pudong1d/71146.htm"

    response1 = requests.get(HTML, headers=headers1)
    response1.encoding = "utf-8"
    my_soup = BeautifulSoup(response1.text, "html.parser")

    # 获取信息主标签
    main_str = my_soup.find("div", attrs={"class": "real-mess"})

    # 获取今天天气、温度
    # weather_main = main_str.find("div", attrs={"class": "real-today"})
    # split = weather_main.text.split("：")[1]
    # # 今天天气
    # weather = split.split("° ")[1]
    # # 最高气温
    # temp = split.split("° ")[0].split("-")[1] + "°C"
    # # 最低气温
    # tempn = split.split("° ")[0].split("-")[0] + "°C"

    # 现在的天气 多云
    now_weather = main_str.find("em", attrs={"class": "cludy"}).text
    find_all = main_str.findAll("span", attrs={"class": "real-data-mess fl"})
    # 当前风向 东北风3级
    wind_direction = find_all[0].text.replace(' ', '')
    # 当前空气湿度 86%
    air_humidity = find_all[1].text.replace('湿度 ', '')
    # 当前紫外线  很弱
    ultraviolet_rays = find_all[2].text.replace('紫外线 ', '')

    # 空气主要标签
    air_main = my_soup.find("div", attrs={"class": "box-mod-tb"})
    # 空气质量  优-16
    air_quality = air_main.find("em").text + "-" + air_main.find("span").text
    # pm 2.5    10
    pm = air_main.find("div", attrs={"class": "aqi-map-style-tip"}).find("em").text

    hours24_main = my_soup.find("div", attrs={"class": "hours24-data-th-right"})
    # 日出时间  06:01
    sunrise = hours24_main.findAll("span")[0].text.split(" ")[1]
    # 日落时间  19:00
    sunset = hours24_main.findAll("span")[1].text.split(" ")[1]

    str_all = """怎么去拥有 一道彩虹 怎么去拥抱 一夏天的风
我不怕千万人阻挡 只怕自己投降
星空下 最明亮的是你 眼中闪烁的光 像烟火升起
终于你身影 消失在 人海尽头 才发现 笑着哭 最痛
恋爱ing 快乐ing 心情就像是 坐上一台 喷射机
那年夏天 我和你 躲在 这一大片 宁静的海
你是空气 但是好闻胜过了空气 你是阳光 但是却能照进半夜里
不打扰 是我的 温柔 不知道 不明了 不想要 为什么 我的心
私奔到月球 两脚悬空 着地球 念紧你的双手
才发现 笑着哭 最痛 知足的快乐 叫我忍受心痛
我不愿让你一个人 一个人在人海浮沉
如果还有遗憾 又怎么样呢 伤了痛了懂了 就能好了吗
突然好想你 你会在哪里 过得快乐或委屈
你是遥远的星河 耀眼得让人想哭
每一次 再一次 你慢慢的 靠近我 告诉我 都是我的错
思念像 无形红线 一端系着我 一端系着你
你不是真正的快乐 你的笑只是 你穿的保护色
我的世界 你曾经来过 留下的痕迹 无法抹去
爱 是踏破红尘 望穿秋水 只因为 爱过的人 不说后悔
我想我 很适合 当一个 歌颂者 青春在 风中 飘着
平凡的我们 也拥有 不平凡的梦 三餐四季 有你就足够
最怕此生 已经决心自己过 没有你 却又突然 听到你的消息
想和你 再去吹吹风 虽然已是 不同时空
时间是 贼 偷走一切 但偷不走 我们的纪念
你是天使 你是天使 你是我最初和最后的天堂
思念是 一种很玄的东西 如影 随形 无声又无息
你是我心中 不灭的光 照亮我 前行的方向
茫茫人海中 遇见你 是我 最大的幸运
春去春又来 花谢花又开 只有你 是我不变的爱
生活 像一首 没写完的诗 每一笔 都有 你的样子
我坐在 床前 看着指尖 已经 如烟的流年
全世界 我都可以 放弃 至少还有你 值得我 去珍惜
相爱这件事 没那么容易 每个人 都有 他的脾气
咪咪是个大笨蛋
"""

    # 每日问候
    literature_all = str_all.split("\n")
    greetings_today = random.choice(literature_all)

    return weather, temp, tempn, now_weather, wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset, greetings_today


##===================================================================================
def get_anniversary_day(anniversary, year, today):
    # 获取纪念日的对应月和日
    anniversary_month = int(anniversary.split("-")[1])
    anniversary_day = int(anniversary.split("-")[2])
    # 今年纪念日
    year_date = date(year, anniversary_month, anniversary_day)

    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today < year_date:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = date((year + 1), anniversary_month, anniversary_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]

    return birth_day


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday


    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en


def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, note_ch, note_en,
                 now_weather, wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset,
                 greetings_today):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    
    
    # 获取相识的日子的日期格式
    love_year_1 = int(config["love_date_1"].split("-")[0])
    love_month_1 = int(config["love_date_1"].split("-")[1])
    love_day_1 = int(config["love_date_1"].split("-")[2])
    love_date_1 = date(love_year_1, love_month_1, love_day_1)
    # 获取相识的日期差
    love_days_1 = str(today.__sub__(love_date_1)).split(" ")[0]
    
    # 获取所有生日数据和纪念日数据
    birthdays = {}
    anniversary = {}
    for k, v in config.items():
        if k[0:8] == "birthday":
            birthdays[k] = v
        if k[0:10] == "anniversar":
            anniversary[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week)
#                 "color": get_color()
            },
            "city": {
                "value": city_name
#                 "color": get_color()
            },
            "weather": {
                "value": weather
#                 "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature
#                 "color": get_color()
            },
            "max_temperature": {
                "value": max_temperature
#                 "color": get_color()
            },
            "love_day_1": {
                "value": love_days_1
#                 "color": get_color()
            },
            "love_day": {
                "value": love_days
#                 "color": get_color()
            },
            "note_en": {
                "value": note_en
#                 "color": get_color()
            },
            "note_ch": {
                "value": note_ch
#                 "color": get_color()
            },
            "now_weather": {
                "value": now_weather
#                 "color": get_color()
            },
            "wind_direction": {
                "value": wind_direction
#                 "color": get_color()
            },
            "air_humidity": {
                "value": air_humidity
#                 "color": get_color()
            },
            "ultraviolet_rays": {
                "value": ultraviolet_rays
#                 "color": get_color()
            },
            "air_quality": {
                "value": air_quality
#                 "color": get_color()
            },
            "pm": {
                "value": pm
#                 "color": get_color()
            },
            "sunrise": {
                "value": sunrise
#                 "color": get_color()
            },
            "sunset": {
                "value": sunset
#                 "color": get_color()
            },
            "greetings_today": {
                "value": greetings_today
#                 "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "{}的生日还有{}天".format(value["name"], birth_day)
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data}
        
        
    for key, value in anniversary.items():
        anniversary_day = get_anniversary_day(value["anniversary"], year, today)
        if anniversary_day == 0:
            anniversary_data = "一切不尽言语中，要抱起宝贝转圈圈~要把宝贝亲的晕过去~"
        else:
            anniversary_data = "和宝贝贴贴还有{}天".format(anniversary_day)
        # 将纪念日插入data
        data["data"][key] = {"value": anniversary_data}
        
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

# 获取accessToken
accessToken = get_access_token()
# 接收的用户
users = config["user"]
# 传入省份和市获取天气信息
province, city = config["province"], config["city"]
weather, max_temperature, min_temperature, now_weather, wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset, greetings_today = get_weather(
    province, city)

# 获取词霸每日金句
note_ch, note_en = get_ciba()
# 公众号推送消息
for user in users:
    send_message(user, accessToken, city, weather, max_temperature, min_temperature, note_ch, note_en, now_weather,
                 wind_direction, air_humidity, ultraviolet_rays, air_quality, pm, sunrise, sunset, greetings_today)
os.system("pause")
