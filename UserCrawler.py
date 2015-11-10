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


# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
ckey="u21PLDSa5ZASKl9227hdPHyTe"
csecret="mAcyWJ3gAw9tw0E5drh8tQpUyKsWEm4NXlQRgD605qCqtOa5Zo"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
atoken="2916112097-YLaonPDx7SElq7ISivpfThCmBb6eirflHGUG2MY"
asecret="pQGcax0xDhjZhuZ2ru0Rgnv4u8aYPZ3SSixpV11SlUoO4"


OAUTH_KEYS = dict(consumer_key=ckey, consumer_secret=csecret, access_token_key=atoken, access_token_secret=asecret)
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)



users = col.distinct('user.screen_name')
server2.close()
d = usertweets.distinct('user.screen_name')

print('start')

for u in users:
    try:
        if u in d:
            continue
        # define user to get tweets for. accepts input from user
        print(u)
        user = api.get_user(u)

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



