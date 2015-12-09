#script to write the tweets in different file for the word count
# -*- coding: utf-8 -*-

import re
import pymongo
from pymongo import MongoClient

#start of the client
client = MongoClient()

# Connection to the database
db = client['team_results_1516']

#team_names_14_15 = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names_15_16 = ['Norwich','Watford','Bournemouth','Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']


def file_write(team_and_result, collec):
	with open(team_and_result, "w", encoding='utf-8') as f:
		for tweet in collec.find():
			for word in tweet['words']:
				print(word, file=f)


i=0
for team in team_names_15_16:
	collection_win = db[team.lower()+'_win']
	collection_lose = db[team.lower()+'_lose']
	collection_draw = db[team.lower()+'_draw']

	file_write("team_results_1516/"+team.lower()+"_win.txt", collection_win)#write in the file win
	file_write("team_results_1516/"+team.lower()+"_lose.txt", collection_lose)
	file_write("team_results_1516/"+team.lower()+"_draw.txt", collection_draw)

	i += 1
	print(i)

