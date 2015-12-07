import time
import pymongo


client = pymongo.MongoClient()
db = client["n-grams"]

while True:
	for name in db.collection_names():		
		try:			
			print(db[name].create_index("words"))
		except:
			print("couldn't creat index: {}".format(name))
	time.sleep(600)
