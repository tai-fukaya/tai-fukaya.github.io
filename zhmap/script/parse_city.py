# -*- coding: utf-8 -*-
# http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

import subprocess
import time
from bs4 import BeautifulSoup

root_host = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
tr_class = "citytr"
open_file = "data/areaid_level0_zh.csv"
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
    return BeautifulSoup(res, "lxml")


def parse(info, soup):
    trs = soup.find_all("tr", attrs={"class": tr_class})
    lists = []
    for tr in trs:
        cells = tr.find_all("td")
        href = cells[0].find("a").get("href")
        areaid = cells[0].text.encode("utf-8")
        name = cells[1].text.encode("utf-8")
        # 地级市	地区	自治州	盟
        tp = 0
        if name[-3:] == "市":
            tp = 1
        elif name[-6:] == "地区":
            tp = 2
        elif name[-3:] == "州":
            tp = 3
        elif name[-3:] == "盟":
            tp = 4
        lists.append(",".join([
            areaid, "1", str(tp), href, info.province, name
        ]))
    return lists

with open(open_file, "r") as f:
    data = f.read().split("\n")
    file = open(output_file, "w")
    for d in data:
        sp = d.split(",")
        if not len(sp):
            continue
        info = ZhInfo()
        info.areaid = sp[0]
        info.level = sp[1]
        info.type = sp[2]
        info.url = sp[3]
        info.province = sp[4]
        print(info.province)
        soup = get_url(info)
        csv_data = parse(info, soup)
        file.write("\n".join(csv_data))
        file.write("\n")
        time.sleep(.1)
    print("finish")
    file.close()
