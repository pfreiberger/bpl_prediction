# -*- coding: utf-8 -*-

import re
import pymongo
from datetime import datetime
from datetime import date
from pymongo import MongoClient
import nltk


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
collection = db.screen_scraper

db2 = client.cleansed
col2 = db2.pure_2


count = 0
tags_to_keep = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP"]
del_tags = ["http", "\@"]

#relevant_words=['victory','score','loss', 'lose', 'lost', 'great', 'win', 'defeat', 'bad', 'game', 'draw', '3 points', 'predict', 'prediction', 'pred', 'won', 'winning', 'congrats', 'go', 'proud']
bad_words = ['transfer', 'champions', 'uefa', 'nba', 'NBA', 'basketball', 'nfl', 'american', 'phila', 'antonio', 'sanantonio', 'citizens', 'detroit', 'rugby', 'citizen']

team_hashtags = ['#mufc','#mcfc','#arsenal','#cfc','#lfc','#whufc','#lcfc','#efc','#swans','#cpfc','#coys','#watfordfc','#ncfc','#wba','#afcb','#saintsfc','#avfc','#scfc','#nufc','#safc',
'#bpl','#manutd','#blues','#gunners','#chelsea','#reds','#hammers','#thefoxes','#everton','#swanseacity','#eagles','#spurs','#wfc','#norwich','#baggies','#boscombe','#southampton',
'#villa','#stoke','#newcastle','#sunderland','#bplkickoff','#reddevils','#theblues','#upthechels','#thereds','#coyb','#glaziers','#lilywhites','#yellowarmy','#thebaggies','#thecherries',
'#villians','#potters','#magpies','#theblackcats','#fpl','#thereddevils','#thepensioners','#ynwa','#thetoffees','#otbc','#albion','#theclaretandblue','#thetoon','#toffees','#thethrostlesalbion',
'#claretandblue','#theschoolofscience','#lions','#thepeoplesclub','#thelions']

def get_date(tweet):
	try:
		if tweet["timestamp_ms"]:
			return date.fromtimestamp(tweet["timestamp_ms"]//1000)
	except:
		x = 1

	try:
		if tweet["created_at"]:
			return datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
	except:
		x = 1

	try:
		if tweet["timestamp"]:
			return date.fromtimestamp(tweet["timestamp"])
	except:
		x = 1

def get_hashtags(tweet):
	try:
		if tweet["hashtags"]:
			return tweet["hashtags"]
	except:
		x = 1

	try:
		if tweet["entities"]["hashtags"]:
			return [x["text"] for x in tweet["entities"]["hashtags"]]
	except:
		x = 1


def transform(id, text, hashtags, dte):
	words = remove_words(text)
	stemmed_words = stem_words(words)
	hashtags = [x.lower().replace('#', "") for x in hashtags]    
	doc = {"_id": int(id), "words": stemmed_words, "date": dte, "hashtags": hashtags}
	return doc

def remove_words(text):
	tokens = nltk.word_tokenize(text)
	tagged_words = nltk.pos_tag(tokens)
	words = list()
	for word in tagged_words:
		if word[1] in tags_to_keep:
			if "." not in word[0]:
				if word[0] not in del_tags:
					words.append(word[0].lower())

	return words

def stem_words(words):
	res = list()
	for word in words:
		stemmer = nltk.stem.porter.PorterStemmer()
		stem = stemmer.stem(word)
		res.append(stem)
	return res


with open("myfile.txt", "w") as f:
	for tweet in collection.find(no_cursor_timeout=True):
		_id = tweet["_id"]
		if col2.find_one({"_id": int(_id)}):
			continue
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
						
						
						dte = get_date(tweet)
						hashtags = get_hashtags(tweet)
						if not hashtags:
							continue
						text = tweet["text"]
						doc = transform(_id, text, hashtags, dte)
						try:
							col2.insert(doc)
						except:
							print("insertion error")
						

						count+=1

print(count)