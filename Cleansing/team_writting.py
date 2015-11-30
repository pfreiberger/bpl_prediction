# -*- coding: utf-8 -*-

import re
import pymongo
from pymongo import MongoClient

#start of the client
client = MongoClient()

# Connection to the database
db = client['cleansed']

team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','Watford','Norwich City','West Brom','Bournemouth','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']


for team in team_names:
	collection_win = db[team.lower()+'_win']
	collection_lose = db[team.lower()+'_lose']
	collection_draw = db[team.lower()+'_draw']

	with open(team.lower()+"_win.txt", "w") as f1:
		for tweet in collection_win.find():
			for word in tweet['words']:
				print(word+" ", file=f1)

	with open(team.lower()+"_lose.txt", "w") as f2:
		for tweet in collection_lose.find():
			for word in tweet['words']:
				print(word+" ", file=f2)

	with open(team.lower()+"_draw.txt", "w") as f3:
		for tweet in collection_draw.find():
			for word in tweet['words']:
				print(word+" ", file=f3)

