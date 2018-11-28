- x:jsonからcsvにする
- 条件に合致したものを大きく表示するように
- 人口の表示
- 民族の表示
- 区画番号の一覧を作る（http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html
- 郵便番号の一覧を作る(https://www.youbianku.com/)
- 行政区画のレベルごとの一覧を作る（https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92

# データ
こんなかんじのデータをつくりたい
名前、レベル、区画区分、所属、行政区画番号、郵便番号、経度、緯度、面積、人口、民族、WikiLink

省、地、県、郷、村
県まではWikipediaから、ほぼ満足できるデータとれそう

直辖市	省	自治区	特别行政区
地级市	地区	自治州	盟
市辖区	县级市	县	自治县	旗	自治旗	特区	林区
街道	镇	乡	民族乡	苏木	民族苏木	区公所

# 行政区画番号
ここベースでとれるけど、郷級以下は、あやしいところもある
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html

行政区画番号、URL、省級、地級、県級、郷級、村級
areaid,url,province,city,county,town,village

たまにパースに失敗こく
```
delete trs;
delete csvs;
var trs = document.getElementsByClassName("countytr");
var csvs = [];
for (let tr of trs) {
    let cells = tr.getElementsByTagName("td");
    let areaid = cells[0].innerText.trim();
    let name = cells[1].innerText.trim();
    let href = "";
    let link = cells[0].getElementsByTagName("a");
    if (link.length) {
        href = link[0].href.replace("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/", "");
    }
    let type = 0;
    let items = [areaid, 2, 0, href, "陕西省", "西安市", name];
    csvs.push(items.join(","));
}
console.log(csvs.join("\n"));
```

## 行政区画変更履歴
http://www.mca.gov.cn/article/sj/xzqh/2018/

# 民族系はここらへん？
https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9C%8B%E6%B0%91%E6%97%8F%E5%88%97%E8%A1%A8
