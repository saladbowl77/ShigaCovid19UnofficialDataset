import json #標準ライブラリ
import csv #標準ライブラリ
from os.path import join, dirname #標準ライブラリ

import feedparser #pip install feedparser
import requests #pip install request

from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy

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

#rssのJson取得
JsonPath = join(dirname(__file__), "datas/rss.json")
with open(JsonPath) as f:
    jsonData = json.load(f)

rssArr = ["pref","pref_news","otsuE","otsuI","kusatu"]

def tweetNewRss(rss):
    print(rss.title)
    print(rss.link)
    # 好きな言葉をツイート
    api.update_status(rss.title + '\n' + rss.link)

for name in rssArr:
    print(jsonData[name])
    print(jsonData[name]['url'])
    print(jsonData[name]['last'])
    print(jsonData[name]['word'])

    first = True
    feed = feedparser.parse(jsonData[name]['url'], response_headers={"content-type": "text/xml; charset=utf-8"})
    for rss in feed.entries:
        if rss.get('published') == None:
            if rss.date > jsonData[name]['last']:
                if jsonData[name]['word']:
                    if jsonData[name]['word'] in rss.title:
                        if first:
                            jsonData[name]['last'] = rss.date
                            first = False
                        tweetNewRss(rss)
                else:
                    if first:
                        jsonData[name]['last'] = rss.date
                        first = False
                    tweetNewRss(rss)
        else:
            if rss.published > jsonData[name]['last']:
                if jsonData[name]['word']:
                    if jsonData[name]['word'] in rss.title:
                        if first:
                            jsonData[name]['last'] = rss.published
                            first = False
                        tweetNewRss(rss)
                else:
                    if first:
                        jsonData[name]['last'] = rss.published
                        first = False
                    tweetNewRss(rss)

with open(JsonPath, 'w') as f:
    json.dump(jsonData, f, indent=4, ensure_ascii=False)
