from datetime import datetime
from datetime import date
from pymongo import MongoClient

#start of the client
client = MongoClient()

# Connection to the database
db = client.TwitterPred

# Choose the collection
user_tweets = db.UserTweets
screenscraper = db.screen_scraper_new
twitter = db.Twitter

db2 = client.cleansed
pure = db2.pure2


def get_date(tweet):
	try:
		if tweet["timestamp_ms"]:
			d = date.fromtimestamp(tweet["timestamp_ms"]//1000)
	except:
		x = 1

	try:
		if tweet["created_at"]:
			d = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
	except:
		x = 1

	try:
		if tweet["timestamp"]:
			d = date.fromtimestamp(int(tweet["timestamp"]))
	except:
		x = 1

	return datetime.combine(d, datetime.min.time())


def update_dates(col, col2):
	for elem in col.find({"date": None}):
		t = col2.find_one({"_id" : str(elem["_id"])})
		if t is None:
			print(elem["_id"])
		dte = get_date(t)
		col.update(elem, {"$set": {"date": dte}})


print("update screen_scraper")
update_dates(pure, screenscraper)
#print("update Twitter")
#update_dates(pure, twitter)
#print("update UserTweets")
#update_dates(pure, user_tweets)