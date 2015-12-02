import _mysql
import MySQLdb
import sys
import warnings
import os
warnings.filterwarnings("ignore", "Unknown table.*")

sys.path.append('../Prediction/')
sys.path.append('../DB/')
from calculateLambda import *
from DBCreation import *
from DBInsertion import *
from DBPonderation import *

RANKINGPATH = "../../../Ranking/"
LAMBDAPATH="../TeamStrength/"
GAMESTOADAPT=6 # After the 10-11 season, for every season we will take X Games to adapt our new lambda values 
XMIN=1
XMAX=GAMESTOADAPT


if __name__ == '__main__':	
	try:
		database = MySQLdb.connect('localhost', 'root', 'root', 'EPL2'); #login, password, database
		cursor=database.cursor()
		# Create the DB  ------------- UNCOMMENT TO CREATE DB AGAIN
		#myDB=DBCreation()
		#myDB.create() 
		season=["1011","1112","1213","1314"]
		count=0
		while (count != len(season)-1):
			currentSeason=str(season[count])
			nextSeason=str(season[count+1])
			# Insert values from the 2 seasons to ponderate into DB
			database.query("TRUNCATE TABLE ranking"+currentSeason+";")  # We empty the tables from current season and next season so we can insert the new values
			database.query("TRUNCATE TABLE ranking"+nextSeason+";")
			directory=currentSeason+"-"+nextSeason
			allFiles=os.listdir(RANKINGPATH)
			for files in allFiles:
				if ("Processed" in files):
					season1=currentSeason[0]+currentSeason[1]+"-"+currentSeason[2]+currentSeason[3]
					season2=nextSeason[0]+nextSeason[1]+"-"+nextSeason[2]+nextSeason[3]
					if(season1 in files or season2 in files):
						insertion=DBInsertion(RANKINGPATH+files,"Rank",directory)
						insertion.parse()

			# Make the ponderation between those 2 seasons
			myDB=DBPonderation(database,currentSeason,nextSeason)
			myDB.makePonderation()
			# Make the prediction for the next games
			
			XMIN=GAMESTOADAPT
			XMAX=XMIN
			scorePercentage=0
			successPercentage=0	
			
			while (XMAX != 38): # 37 MatchDay so we can predict the last one of the season
				myLambda=Lambda(nextSeason,database,XMIN,XMAX,0) # Predict Game XMAX+1 -> Next Game
				result=myLambda.calculateLambda() # 0 = we dont want a print
				scorePercentage+=result[0]
				successPercentage+=result[1]
				XMIN+=1
				XMAX+=1 # Predict the Next Game
			print("Final Correctness Prediction for season : "+str(nextSeason))
			print("Score Success : "    +str((scorePercentage*1.0) /(38-GAMESTOADAPT))+"%")
			print("Prediction Result : "+str((successPercentage*1.0) /(38-GAMESTOADAPT))+"%")
			count+=1
		
		database.close();
		
		
	except (_mysql.Error):
		
		print ("Mysql error ")
		sys.exit(1)