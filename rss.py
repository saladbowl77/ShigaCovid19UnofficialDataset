import json #標準ライブラリ
import csv #標準ライブラリ
from os.path import join, dirname #標準ライブラリ
from datetime import datetime

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

def tweetNewRss(rss,type):
    if(type == 'published'):
        if rss.published[-3:] == "GMT":
            uploadDate = datetime.strptime(rss.published, '%a, %d %b %Y %H:%M:%S %Z')
        else:
            uploadDate = datetime.strptime(rss.published, '%a, %d %b %Y %H:%M:%S %z')
    elif(type == 'date'):
        uploadDate = datetime.strptime(rss.date, '%Y-%m-%dT%H:%M:%S+09:00')
    else:
        uploadDate = ""
    
    
    #print(rss.title + '\n' + rss.link + '\n サイト更新日 : ' + uploadDate.strftime('%Y/%m/%d %H:%M:%S'))

    api.update_status(rss.title + '\n' + rss.link + '\n サイト更新日 : ' + uploadDate.strftime('%Y/%m/%d %H:%M:%S'))
    

for name in rssArr:
    feed = feedparser.parse(jsonData[name]['url'], response_headers={"content-type": "text/xml; charset=utf-8"})

    first = True
    for rss in feed.entries:
        if rss.get('published'):
            if rss.published > jsonData[name]['last']:
                if jsonData[name]['word']:
                    if jsonData[name]['word'][:4] == "http" and jsonData[name]['word'] in rss.link:
                        tweetNewRss(rss,'published')
                    elif jsonData[name]['word'] in rss.title:
                        tweetNewRss(rss,'published')
                else:
                    tweetNewRss(rss,'published')
            if first:
                jsonData[name]['last'] = rss.published
                first = False
        else:
            print(rss.link, rss.title)
            if rss.date > jsonData[name]['last']:
                if jsonData[name]['word']:
                    if jsonData[name]['word'][:4] == "http" and jsonData[name]['word'] in rss.link:
                        tweetNewRss(rss,'date')
                    elif jsonData[name]['word'] in rss.title:
                        tweetNewRss(rss,'date')
                else:
                    tweetNewRss(rss,'date')
            if first:
                jsonData[name]['last'] = rss.date
                first = False

print(jsonData)

with open(JsonPath, 'w') as f:
    json.dump(jsonData, f, indent=4, ensure_ascii=False)