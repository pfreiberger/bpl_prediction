# -*- coding: utf-8 -*-

import re
import pymongo
from pymongo import MongoClient

#start of the client
client = MongoClient()

# Connection to the database
db = client['cleansed']

team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','Watford','Norwich City','West Brom','Bournemouth','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']

def file_write(team_and_result, collec):
	with open(team.lower()+"_win.txt", "w") as f:
		for tweet in collec.find():
			for word in tweet['words']:
				print(word+" ", file=f)

for team in team_names:
	collection_win = db[team.lower()+'_win']
	collection_lose = db[team.lower()+'_lose']
	collection_draw = db[team.lower()+'_draw']

	file_write(team.lower()+"_win.txt", collection_win)
	file_write(team.lower()+"_lose.txt", collection_lose)
	file_write(team.lower()+"_draw.txt", collection_draw)

