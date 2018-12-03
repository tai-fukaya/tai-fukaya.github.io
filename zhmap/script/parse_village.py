# -*- coding: utf-8 -*-
# http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

import random
import subprocess
import time
from bs4 import BeautifulSoup

root_host = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
tr_class = "villagetr"
open_file = "data/areaid_level3_zh.csv"
open_file = "data/mistake.2.csv"
output_file = "data/areaid_level4_zh.15.csv"
begin = 38671
begin = 1
end = 43253
# 17, 18

# 1, 337, 642, 2990,
# 4472, 5740, 7330, 8368,
# 10339, 10573, 12141, 13541,
# 15186, 16371,
# 18154, 20005, 22571,
# 24055, 26057, 27835, 29126,
# 29370, 30402, 35049, 36530, 37970,
# 38671, 39990, 41425, 41855, 42120,
# 43253


class ZhInfo(object):
    def __init__(self):
        self.areaid = ""
        self.level = ""
        self.type = ""
        self.url = ""
        self.province = ""
        self.city = ""
        self.county = ""
        self.town = ""
        self.village = ""


def get_url(info):
    res = subprocess.check_output([
        "curl", root_host + info.url, "-m", "30"
    ])

    return BeautifulSoup(res.decode('gbk'), "lxml")


def parse(info, soup):
    trs = soup.find_all("tr", attrs={"class": tr_class})
    lists = []
    print(len(trs))
    # print(soup.text)
    for tr in trs:
        cells = tr.find_all("td")
        # atag = cells[0].find("a")
        areaid = cells[0].text.encode("utf-8")
        href = ""
        # if atag:
        #     href = areaid[:2] + "/" + areaid[2:4] + "/" + atag.get("href")
        name = cells[2].text.encode("utf-8")
        tp = cells[1].text.encode("utf-8")
        lists.append(",".join([
            areaid, "4", str(tp), href, info.province, info.city, info.county, info.town, name
        ]))
        # print(name)
    return lists

with open(open_file, "r") as f:
    data = f.read().split("\n")
    file = open(output_file, "w")
    for idx, d in enumerate(data):
        if idx + 1 < begin or idx >= end:
            continue
        sp = d.split(",")
        if idx % 10 == 0:
            time.sleep(5)
        if len(sp) <= 1:
            continue
        info = ZhInfo()
        info.areaid = sp[0]
        info.level = sp[1]
        info.type = sp[2]
        info.url = sp[3]
        info.province = sp[4]
        info.city = sp[5]
        info.county = sp[6]
        info.town = sp[7]
        print(idx)
        print(info.province)
        print(info.city)
        print(info.county)
        print(info.town)
        if not info.url:
            continue
        csv_data = []
        try:
            soup = get_url(info)
            csv_data = parse(info, soup)
        except Exception as e:
            print(e)
        file.write("\n".join(csv_data))
        file.write("\n")
        time.sleep(.1 + random.random() * 2.)
    print("finish")
    import datetime
    print(datetime.datetime.now())
    file.close()
