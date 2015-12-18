import time
import pymongo


client = pymongo.MongoClient()
db = client["team_results"]




team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names = [team_name.lower().replace(" ", "_") for team_name in team_names]

for team_name in team_names:
	col_win = db[team_name+"_win"]
	col_lose = db[team_name+"_lose"]
	col_draw = db[team_name+"_draw"]
	try:
		col_win.create_index("words")
		col_lose.create_index("words")
		col_draw.create_index("words")
	except:
		pass

#while True:
#	for name in db.collection_names():		
#		try:			
#			print(db[name].create_index("words"))
#		except:
#			print("couldn't creat index: {}".format(name))
#	time.sleep(600)
