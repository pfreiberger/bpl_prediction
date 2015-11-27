# -*- coding: utf-8 -*-

import re
import pymongo
from pymongo import MongoClient



def in_array(tweet,array):
	words = tweet.split(" ")
	for word in words:
		if word in array:
			return word

	return False


#start of the client
client = MongoClient()

# Connection to the database
db = client.TwitterPred

# Choose the collection
collection = db.Twitter

db2 = client.cleansed
col2 = db2.pure_2


count = 0

#relevant_words=['victory','score','loss', 'lose', 'lost', 'great', 'win', 'defeat', 'bad', 'game', 'draw', '3 points', 'predict', 'prediction', 'pred', 'won', 'winning', 'congrats', 'go', 'proud']
bad_words = ['transfer', 'champions', 'uefa', 'nba', 'NBA', 'basketball', 'nfl', 'american', 'phila', 'antonio', 'sanantonio', 'citizens', 'detroit', 'rugby', 'citizen']

team_hashtags = ['#mufc','#mcfc','#arsenal','#cfc','#lfc','#whufc','#lcfc','#efc','#swans','#cpfc','#coys','#watfordfc','#ncfc','#wba','#afcb','#saintsfc','#avfc','#scfc','#nufc','#safc',
'#bpl','#manutd','#blues','#gunners','#chelsea','#reds','#hammers','#thefoxes','#everton','#swanseacity','#eagles','#spurs','#wfc','#norwich','#baggies','#boscombe','#southampton',
'#villa','#stoke','#newcastle','#sunderland','#bplkickoff','#reddevils','#theblues','#upthechels','#thereds','#coyb','#glaziers','#lilywhites','#yellowarmy','#thebaggies','#thecherries',
'#villians','#potters','#magpies','#theblackcats','#fpl','#thereddevils','#thepensioners','#ynwa','#thetoffees','#otbc','#albion','#theclaretandblue','#thetoon','#toffees','#thethrostlesalbion',
'#claretandblue','#theschoolofscience','#lions','#thepeoplesclub','#thelions']



with open("myfile.txt", "w") as f:
	for tweet in collection.find():
		hash_one=False
		hash_two=False
		if 'text' in tweet.keys():
			if 'RT' not in tweet['text']:
				if not any(x in tweet['text'].lower() for x in bad_words):
					hash_one = in_array(tweet['text'].lower(), team_hashtags)
					if hash_one != False:
						tmp_team_hashtags = [x for x in team_hashtags if x!=hash_one] 

						hash_two = in_array(tweet['text'].lower() , tmp_team_hashtags)

					if hash_two == False:
						#print(tweet['text'].encode('utf-8'), file=f)
                        col2.insert(tweet)

						count+=1

print(count)