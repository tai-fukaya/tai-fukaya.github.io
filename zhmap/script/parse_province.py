# -*- coding: utf-8 -*-
# http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

import subprocess
from bs4 import BeautifulSoup

root_host = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
tr_class = "provincetr"

res = subprocess.check_output([
    "curl",
    root_host + "index.html"
])
soup = BeautifulSoup(res, "lxml")

trs = soup.find_all("tr", attrs={"class": tr_class})
csv_data = []
for tr in trs:
    links = tr.find_all("a")
    for link in links:
        href = link.get("href")
        name = link.text.encode("utf-8")
        # 直辖市,省,自治区,特别行政区
        tp = 0
        if name[-3:] == "市":
            tp = 1
        elif name[-3:] == "省":
            tp = 2
        elif name[-9:] == "自治区":
            tp = 3
        elif name[-15:] == "特别行政区":
            tp = 4

        # id, level, type, url, province
        csv_data.append(",".join([
            href.replace(".html", ""), "0", str(tp), href, name
        ]))

file = open("data/areaid_level0_zh.csv", "w")
file.write("\n".join(csv_data))
file.close()
