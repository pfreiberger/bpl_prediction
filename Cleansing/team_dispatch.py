import re
import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import csv


#start of the client
client = MongoClient()

# Connection to the database
db = client['cleansed']
db2 = client['team_results_1516']

# Choose the collection
collection = db['season15_16']

#define timedelta
five_days = timedelta(days=5)

#function that insert the tweet in the good collection : win/draw/lose
def insert_tweet(name, score1, score2, tweet):
	if int(score1) > int(score2):
		db2[name+'_win'].insert(tweet)

	elif int(score1) == int(score2):
		db2[name+'_draw'].insert(tweet)

	else:
		db2[name+'_lose'].insert(tweet)


#open file
with open("championship1516.csv") as cfile:
	match_days = csv.reader(cfile, delimiter=",")

	i=0
	for match in match_days:
		dte = datetime.strptime(match[0], '%Y-%m-%d %H:%M:%S') 
		home = match[1].lower()
		away = match[2].lower()
		#take only the tweets with the same matchdate
		#home team
		for tweet in collection.find({"team": home, "matchdate": dte}):
			insert_tweet(home, match[3], match[4], tweet)
		#away team
		for tweet in collection.find({"team": away, "matchdate": dte}):
			insert_tweet(away, match[4], match[3], tweet)

		i += 1
		if i%10 ==0:
			print(i)




