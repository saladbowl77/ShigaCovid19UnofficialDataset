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

checkUrl = ""

feed = feedparser.parse(checkUrl, response_headers={"content-type": "text/xml; charset=utf-8"})

print(feed.entries[0])

for rss in feed.entries[::-1]:
    if rss.get('published'):
        print(rss.title,rss.link,rss.published)
    elif rss.get('date'):
        print(rss.title,rss.link,rss.date)