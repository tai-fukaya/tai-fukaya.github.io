# -*- coding: utf-8 -*-
# http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

import subprocess
import time
from bs4 import BeautifulSoup

root_host = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
tr_class = "towntr"
open_file = "data/areaid_level2_zh.csv"
output_file = "data/done.csv"


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
        "curl", root_host + info.url
    ])
    return BeautifulSoup(res.decode('gbk'), "lxml")


def parse(info, soup):
    trs = soup.find_all("tr", attrs={"class": tr_class})
    lists = []
    print(len(trs))
    # print(soup.text)
    for tr in trs:
        cells = tr.find_all("td")
        atag = cells[0].find("a")
        areaid = cells[0].text.encode("utf-8")
        href = ""
        if atag:
            href = areaid[:2] + "/" + areaid[2:4] + "/" + atag.get("href")
        name = cells[1].text.encode("utf-8")
        # 街道	镇	乡	民族乡	苏木	民族苏木	区公所
        tp = 0
        if name[-15:] == "街道办事处":
            tp = 1
        elif name[-15:] == "地区办事处":
            tp = 3
        elif name[-3:] == "镇":
            tp = 2
        elif name[-9:] == "民族乡":
            tp = 4
        elif name[-3:] == "乡":
            tp = 3
        elif name[-12:] == "民族苏木":
            tp = 6
        elif name[-6:] == "苏木":
            tp = 5
        elif name[-9:] == "区公所":
            tp = 7

        lists.append(",".join([
            areaid, "3", str(tp), href, info.province, info.city, info.county, name
        ]))
        # print(name)
    return lists

with open(open_file, "r") as f:
    data = f.read().split("\n")
    file = open(output_file, "w")
    # print(len(data))
    for idx, d in enumerate(data):
        sp = d.split(",")
        if idx < 2506:
            continue
        if idx % 10 == 0:
            time.sleep(1)
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
        print(idx)
        print(info.province)
        print(info.city)
        print(info.county)
        if not info.url:
            continue
        soup = get_url(info)
        csv_data = parse(info, soup)
        file.write("\n".join(csv_data))
        file.write("\n")
        time.sleep(.1)
    print("finish")
    file.close()
