__author__ = 'Philipp'

from selenium import webdriver
import time
import datetime
from bs4 import BeautifulSoup as soup
import pymongo


# Season 2014-2015: 16.08.2014 - 24.05.2015
# Season 2015-2016: 10.08.2015 - 22.11.2015

server = pymongo.MongoClient('localhost', 27017)
db = server['TwitterPred']
collection = db['screen_scraper_new']

current_date = datetime.date(2015, 11, 22)
end_date = datetime.date(2015, 8, 1)

browser = webdriver.Firefox()

sample_url = "https://twitter.com/search?q=%23mufc%20lang%3Aen%20since%3A2010-08-18%20until%3A2010-08-25&src=typd"

root_url = "https://twitter.com/search?q=%23"

lang = "%20lang%3Aen"
since = "%20since%3A"
until = "%20until%3A"
date_string = "2010-08-18 2010-08-25"
end_string = "&src=typd"

hashtag_lst = list()

f = open('data/hashtags.txt', 'r')
for line in f:
    hashtag_lst.append(line.strip())

f.close()

while current_date > end_date:
    print(current_date)
    for hashtag in hashtag_lst:
        print(hashtag)

        since_date = str(current_date - datetime.timedelta(1))
        until_date = str(current_date)
        url = root_url + hashtag + lang + since + since_date + until + until_date + end_string
        browser.get(url)
        i = 0
        while i < 15:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i += 1
            time.sleep(0.7)
        data = soup(browser.page_source)

        tweets = data.find_all("li", {"class": "js-stream-item stream-item stream-item expanding-stream-item "})
        for tweet in tweets:
            try:
                _id = tweet['data-item-id']
                timestamp = tweet.find('span', {'class': '_timestamp js-short-timestamp '})['data-time']
                text = tweet.find('p', {'class': "TweetTextSize js-tweet-text tweet-text"}).text
                tmp = tweet.find_all('a', {'class': "twitter-hashtag pretty-link js-nav"})
                hashtags = [h.text for h in tmp]

                doc = {'_id': _id, 'timestamp' : timestamp, 'text': text, 'hashtags': hashtags}
                collection.update({'_id': _id}, doc, upsert=True)
            except:
                continue
    current_date = current_date - datetime.timedelta(1)
    time.sleep(60)
