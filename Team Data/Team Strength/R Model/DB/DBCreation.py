import _mysql
import sys
import os
STATSPATH = "../../../Stats/"
CURRENTSEASON= "../../../CurrentSeason/"
from DBInsertion import *

class DBCreation(object):
	"""docstring for DBCreation"""
	def __init__(self):
		super(DBCreation, self).__init__()

	def create(self):
		try:
			database = _mysql.connect('localhost', 'root', 'root', 'EPL2'); #login, password, database
			years=["1011","1112","1213","1314","1415","1516"]
			for year in years:
				database.query(
					"CREATE TABLE IF NOT EXISTS ranking"+str(year)+" \
					( \
					Rank		 			int 			NOT NULL	, \
					Team 					varchar(30) 	NOT NULL , \
					Played 					int				NOT NULL , \
					Wins 					int				NOT NULL , \
					Draws		 			int 			NOT NULL , \
					Losses		 			int 			NOT NULL , \
					GoalsFor		 		int 			NOT NULL , \
					GoalsAgainst		 	int 			NOT NULL , \
					GoalsDIFF		 		int 			NOT NULL , \
					Points		 			int 			NOT NULL , \
					Attack 					DECIMAL(5,4) 				 , \
					Defense 				DECIMAL(5,4) 				 , \
					Beta 					DECIMAL(5,4) 				 , \
					BetaHome 				DECIMAL(5,4) 				 , \
					PRIMARY KEY (Team) \
					); \
					"
				);
				database.query(
					"CREATE TABLE IF NOT EXISTS championship"+str(year)+" \
					( \
					id 					int				NOT NULL	AUTO_INCREMENT, \
					GameDate 			datetime 		NOT NULL , \
					HomeTeam 			varchar(30)		NOT NULL , \
					AwayTeam 			varchar(30)		NOT NULL , \
					FTHG		 		int 			NOT NULL , \
					FTAG		 		int 			NOT NULL , \
					HC		 			int 			NOT NULL , \
					AC		 			int 			NOT NULL , \
					HY		 			int 			NOT NULL , \
					AY		 			int 			NOT NULL , \
					HR		 			int 			NOT NULL , \
					AR		 			int 			NOT NULL , \
					B365H 				DECIMAL(3,2) 			NOT NULL , \
					B365D 				DECIMAL(3,2) 			NOT NULL , \
					B365A 				DECIMAL(3,2) 			NOT NULL , \
					BWH 				DECIMAL(3,2) 			NOT NULL , \
					BWD 				DECIMAL(3,2) 			NOT NULL , \
					BWA 				DECIMAL(3,2) 			NOT NULL , \
					MatchDay 			int 			NOT NULL , \
					PRIMARY KEY (id) \
					); \
					"
				);

			allFiles=os.listdir(STATSPATH)
			print("Inserting Stat into the DB, this may take some while ...")
			for files in allFiles:
				if ("Processed" in files):
					print("Processing File :"+str(files))
					insertion=DBInsertion(STATSPATH+files,"Stat","Null")
					insertion.parse()
			allFiles=os.listdir(CURRENTSEASON)
			print("Inserting Latest season into the DB, this may take some while ...")
			for files in allFiles:
				if ("Stats" in files):
					insertion=DBInsertion(CURRENTSEASON+files,"StatCurrent","Null")
					insertion.parse()
			database.close();
			print("Done creating Table")
		except (_mysql.Error):
			print ("Mysql error ")
			sys.exit(1)
		


