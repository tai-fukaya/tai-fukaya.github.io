# -*- coding: utf-8 -*-
# assetに入っていたsuccess.jsonのファイルサイズを小さくするスクリプト
import json
import os

csv_data = []
with open("../assets/data/success.json", "r") as f:
    data = json.load(f)
    print(len(data))
    prev_search_id = ""
    prev_area = ""
    prev_lat = 0
    prev_lng = 0
    for d in data:
        place = d.get("place")
        if not place:
            continue
        search_id = d.get("search_id").encode('utf-8')
        op_search_id = search_id
        display_id = d.get("display_id").encode('utf-8')
        ministry = place.get("ministry", "").encode('utf-8')
        province = place.get("province", "").encode('utf-8')
        city = place.get("city", "").encode('utf-8')
        area = ",".join([ministry, province, city])
        lat = int(d.get("lat")*10000000)
        lng = int(d.get("lng")*10000000)

        if prev_area == area:
            ministry = ""
            province = ""
            city = ""
            if prev_search_id[:6] == search_id[:6]:
                op_search_id = search_id[6:]
        prev_area = area
        prev_search_id = search_id

        lat -= prev_lat
        prev_lat += lat
        lng -= prev_lng
        prev_lng += lng

        if display_id[-3:] == "000":
            display_id = ""
        items = [
            op_search_id,
            display_id,
            ministry,
            province,
            city,
            place.get("town", "").encode('utf-8'),
            str(d.get("area_level")),
            str(lat),
            str(lng)
        ]

        csv_data.append(",".join(items))

file = open("../assets/data/data_compressed.csv", "w")
file.write("\n".join(csv_data))
file.close()
