# -*- coding: utf-8 -*-
# http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

import subprocess
import time
from bs4 import BeautifulSoup

root_host = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
tr_class = "countytr"
# open_file = "data/areaid_level1_zh.csv"
# output_file = "data/areaid_level2_zh.csv"
open_file = "data/mistake.csv"
output_file = "data/mistake_level2_zh.csv"


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
    print(res)
    return BeautifulSoup(res, "lxml")


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
            href = areaid[:2] + "/" + atag.get("href")
        name = cells[1].text.encode("utf-8")
        # 市辖区	县级市	县	自治县	旗	自治旗	特区	林区
        tp = 0
        if name[-6:] == "特区":
            tp = 7
        elif name[-6:] == "林区":
            tp = 8
        elif name[-3:] == "区":
            tp = 1
        elif name[-3:] == "市":
            tp = 2
        elif name[-9:] == "自治县":
            tp = 4
        elif name[-3:] == "县":
            tp = 3
        elif name[-9:] == "自治旗":
            tp = 6
        elif name[-3:] == "旗":
            tp = 5
        lists.append(",".join([
            areaid, "2", str(tp), href, info.province, info.city, name
        ]))
        # print(name)
    return lists

with open(open_file, "r") as f:
    data = f.read().split("\n")
    # file = open(output_file, "w")
    # print(len(data))
    for idx, d in enumerate(data):
        sp = d.split(",")
        if idx % 10 == 0:
            time.sleep(1)
        if not len(sp):
            continue
        info = ZhInfo()
        info.areaid = sp[0]
        info.level = sp[1]
        info.type = sp[2]
        info.url = sp[3]
        info.province = sp[4]
        info.city = sp[5]
        print(info.province)
        print(info.city)
        soup = get_url(info)
        csv_data = parse(info, soup)
        # file.write("\n".join(csv_data))
        # file.write("\n")
        time.sleep(.1)
        break
    print("finish")
    # file.close()
