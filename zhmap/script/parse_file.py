# -*- coding: utf-8 -*-
# http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

import random
import subprocess
import time
from bs4 import BeautifulSoup

root_host = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
tr_class = "villagetr"
open_file = "data/510681114.html"
output_file = "data/areaid_level4_zh.mistake.csv"


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
    data = f.read()
    file = open(output_file, "w")
    info = ZhInfo()
    info.areaid = "510681114000"
    info.level = 3
    info.type = 2
    info.url = "51/06/81/510681114.html"
    info.province = "四川省"
    info.city = "德阳市"
    info.county = "广汉市"
    info.town = "金鱼镇"
    soup = BeautifulSoup(data.decode('gbk'), "lxml")
    csv_data = parse(info, soup)
    file.write("\n".join(csv_data))
    file.write("\n")
    file.close()
