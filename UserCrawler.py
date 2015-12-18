import tweepy
import pymongo
import time
import sys

server1 = pymongo.MongoClient('localhost', 27017)
server2 = pymongo.MongoClient('localhost', 27017)
db1 = server1['TwitterPred']
db2 = server2['TwitterPred']
col = db1['Twitter']
usertweets = db2['UserTweets']

with open(fname) as f:
    content = f.readlines()
    ckey = content[0]
    csecret = content[1]
    atoken = content[2]
    asecret = content[3]


OAUTH_KEYS = dict(consumer_key=ckey, consumer_secret=csecret, access_token_key=atoken, access_token_secret=asecret)
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)



users = col.distinct('user.screen_name')
server2.close()
distinct_list = usertweets.distinct('user.screen_name')

print('start')

for user in users:
    try:
        if user in distinct_list:
            continue
        # define user to get tweets for. accepts input from user
        print(user)
        user = api.get_user(user)

        timeline = user.timeline(count=200)
        #timeline = api.user_timeline(screen_name=user, count=10)

        docs = list()
        for tweet in timeline:
            doc = tweet._json
            doc['_id'] = doc['id']
            docs.append(doc)
        try:
            usertweets.insert(docs, continue_on_error=True)
        except:
            ('insertion Error')

        time.sleep(200)
    except:
        print(sys.exc_info()[0])



