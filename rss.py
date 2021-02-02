import json #標準ライブラリ
import csv #標準ライブラリ
from os.path import join, dirname #標準ライブラリ
from datetime import datetime, timezone

import feedparser #pip install feedparser
import requests #pip install request

from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy

from dateutil.parser import parse

#環境変数読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

consumer_key = getenv("TWITTER_API_KEY")
consumer_secret= getenv("TWITTER_API_SECRET")
access_key = getenv("TWITTER_ACCESS_TOKEN")
access_secret = getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

def tweetNewRss(rss,rssDate,cityNameEN):
    cityName = {
        "pref":"滋賀県",
        "pref_news":"滋賀県",
        "otsuE":"大津市",
        "otsuI":"大津市",
        "kusatu":"草津市",
        "ritto":"栗東市",
        "yasu":"野洲市",
        "koka":"甲賀市",
        "konan":"湖南市",
        "higashiomi":"東近江市",
        "omihachiman":"近江八幡市",
        "hino":"日野町",
        "hikone":"彦根市",
        "aisho":"愛荘町",
        "toyosato_emergency":"豊郷町",
        "toyosato_news":"豊郷町",
        "koura":"甲良町",
        "taga_emergency":"多賀町",
        "taga_news":"多賀町",
        "maibara":"米原市",
        "nagahama_emergency":"長浜市",
        "nagahama_news":"長浜市",
        "takashima":"高島市"
    }
    tweetText = cityName[cityNameEN] + "からのお知らせ\n" + rss.title + '\n' + rss.link + '\n サイト更新日 : ' + rssDate.strftime('%Y年%m月%d日 %H時%M分')
    print(tweetText)
    #api.update_status(tweetText)

#rssのJson取得
JsonPath = join(dirname(__file__), "datas/rss.json")
with open(JsonPath) as f:
    jsonData = json.load(f)

rssArr = ["pref","pref_news","otsuE","otsuI","kusatu","ritto","yasu","koka","konan","higashiomi","omihachiman","hino","hikone","aisho","toyosato_emergency","toyosato_news","koura","taga_emergency","taga_news","maibara","nagahama_emergency","nagahama_news","takashima"]

for name in rssArr:
    cityJsonPathAll = join(dirname(__file__), "datas/rss/all/" + name +".json")
    cityJsonPathCovid = join(dirname(__file__), "datas/rss/covid/" + name +".json")

    with open(cityJsonPathAll, "r") as json_file:
        cityJsonAll = json.load(json_file)
    with open(cityJsonPathCovid, "r") as json_file:
        cityJsonCovid = json.load(json_file)

    feed = feedparser.parse(jsonData[name]['url'], response_headers={"content-type": "text/xml; charset=utf-8"})
    lastDate = parse(str(jsonData[name]['last']))
    for rss in feed.entries[::-1]:
        if rss.get('published'):
            rssDate = parse(rss.published)
        else:
            rssDate = parse(rss.date)
        if rssDate > lastDate:
            if jsonData[name]['word']:
                if jsonData[name]['word'][:4] == "http" and jsonData[name]['word'] in rss.link:
                    tweetNewRss(rss,rssDate,name)
                    cityJsonCovid.append({"title":rss.title,"link":rss.link,"date":str(rssDate)})
                elif jsonData[name]['word'] in rss.title:
                    tweetNewRss(rss,rssDate,name)
                    cityJsonCovid.append({"title":rss.title,"link":rss.link,"date":str(rssDate)})
            else:
                tweetNewRss(rss,rssDate,name)
                cityJsonCovid.append({"title":rss.title,"link":rss.link,"date":str(rssDate)})
            cityJsonAll.append({"title":rss.title,"link":rss.link,"date":str(rssDate)})
        
    with open(cityJsonPathAll, "w") as f:
        json.dump(cityJsonAll, f, indent=4, ensure_ascii=False)
    with open(cityJsonPathCovid, "w") as f:
        json.dump(cityJsonCovid, f, indent=4, ensure_ascii=False)
    jsonData[name]['last'] = str(rssDate)

print(jsonData)

with open(JsonPath, 'w') as f:
    json.dump(jsonData, f, indent=4, ensure_ascii=False)