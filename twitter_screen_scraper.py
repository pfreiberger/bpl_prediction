__author__ = 'Philipp'

import urllib.request as urlreq
from bs4 import BeautifulSoup as soup
import time
import pymongo
import sys
import datetime

date = datetime.date()

#first match 14.8. so start wirll be at 10th of august

#structure of a tweet
# <li class="js-stream-item stream-item stream-item expanding-stream-item " data-item-id="656052641840001025"
#                                                     data-item-type="tweet" id="stream-item-tweet-656052641840001025">
#    <div class="content">
#       <small class="time">
#           <a class="tweet-timestamp js-permalink js-nav js-tooltip" title="03.21 - 19. okt. 2015">
#               <span aria-hidden="true" class="_timestamp js-short-timestamp js-relative-timestamp"
#                                            data-long-form="true" data-time="1445250113" data-time-ms="1445250113000">
#                       51 min
#               </span>
#               <span class="u-hiddenVisually" data-aria-label-part="last">
#                   for 51 minutter siden
#               </span>
#           </a>
#       </small>
#       <div class="stream-item-header">
#           <p class="TweetTextSize js-tweet-text tweet-text">
#                <a class="twitter-hashtag pretty-link js-nav" >
#                   <b><strong>HASHTAG</strong></b></a>

server = pymongo.MongoClient('localhost', 27017)
db = server['TwitterPred']
collection = db['screen_scraper']

root = "https://twitter.com/search?f=tweets&vertical=default&q=%23"
searchterm = root + 'mufc'
lang = '%20lang%3Aen'
since = '%20since%3A2010-08-18'
until = '%20until%3A2010-08-25'
end = '&src=typd'

#'https://twitter.com/search?q=%23mufc%20lang%3Aen%20since%3A2010-08-18%20until%3A2010-08-25&src=typd'

def getPaperData(url):
    try:
        data = soup(urlreq.urlopen(url).read())
    except:
        print('error occurred')
        return -1
    time.sleep(2)
    file = open('data/twitter.html', 'w+')
    file.write(data)
    tweets = data.find_all("li", {"class": "js-stream-item stream-item stream-item expanding-stream-item "})
    for tweet in tweets:
        id = tweet['data-item-id']
        timestamp = tweet.find('span', {'class': '_timestamp js-short-timestamp js-relative-timestamp'})['data-time']
        text = tweet.find('p', {'class':"TweetTextSize js-tweet-text tweet-text"}).text
        tmp = tweet.find_all('a', {'class':"twitter-hashtag pretty-link js-nav"})
        hashtags = [h.text for h in tmp]

        doc = {'_id':id, 'timestamp' : timestamp, 'text': text, 'hashtags': hashtags}
        collection.update({'_id':id}, doc, upsert=True)


tracks = list()

f = open('data/hashtags.txt', 'r')
for line in f:
    tracks.append(line.strip())

for track in tracks:
    url = root + 'mufc'
    try:
        err = getPaperData(url)
        if err == -1:
            time.sleep(10)
    except:
        print(url)
        print("Unexpected error:", sys.exc_info()[0])

