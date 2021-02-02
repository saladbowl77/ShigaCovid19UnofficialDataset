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

def tweetNewRss(rss,rssDate):
    tweetText = rss.title + '\n' + rss.link + '\n サイト更新日 : ' + rssDate.strftime('%Y年%m月%d日 %H時%M分')
    print(tweetText)
    api.update_status(tweetText)

#rssのJson取得
JsonPath = join(dirname(__file__), "datas/rss.json")
with open(JsonPath) as f:
    jsonData = json.load(f)

rssArr = ["pref","pref_news","otsuE","otsuI","kusatu","nagahama_emergency","nagahama_news"]

for name in rssArr:
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
                    tweetNewRss(rss,rssDate)
                elif jsonData[name]['word'] in rss.title:
                    tweetNewRss(rss,rssDate)
            else:
                tweetNewRss(rss,rssDate)
    jsonData[name]['last'] = str(rssDate)

print(jsonData)

with open(JsonPath, 'w') as f:
    json.dump(jsonData, f, indent=4, ensure_ascii=False)