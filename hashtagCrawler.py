from TwitterAPI import TwitterAPI
import pymongo
import time
import datetime

server = pymongo.MongoClient('localhost', 27017)
db = server['TwitterPred']
collection = db['Twitter']

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
ckey="u21PLDSa5ZASKl9227hdPHyTe"
csecret="mAcyWJ3gAw9tw0E5drh8tQpUyKsWEm4NXlQRgD605qCqtOa5Zo"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
atoken="2916112097-YLaonPDx7SElq7ISivpfThCmBb6eirflHGUG2MY"
asecret="pQGcax0xDhjZhuZ2ru0Rgnv4u8aYPZ3SSixpV11SlUoO4"

api = TwitterAPI(ckey, csecret, atoken, asecret)


tracks = list()

f = open('data/hashtags.txt', 'r')
for line in f:
    tracks.append(line.strip())

track_terms = list()
track_term = ""
j = 0
for track in tracks:
    track_term += str(track) + ","
    j += 1
    if j % 10 == 0:
        track_terms.append(track_term)
        track_term = ""

while True:
    for track_term in track_terms:
        try:
            start = datetime.datetime.now()
            print('request tweets for ' + track_term)
            try:
                r = api.request('statuses/filter', {'track': track_term})
            except:
                print("Error")
                time.sleep(900)

            print('change key and instert')
            i = 0
            for item in r:
                try:
                    item['_id'] = item['id']
                except KeyError as ex:
                    print(ex)
                collection.insert(item, continue_on_error=True)
                i += 1
                if i == 100 or (datetime.datetime.now() - start).seconds > 360:
                    time.sleep(60)
                    break
        except:
            print("Error")
            time.sleep(900)



