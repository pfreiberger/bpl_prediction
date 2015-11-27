import _mysql
import MySQLdb
import sys
from teamStrength import *
from calculateLambda import *

RANGE=3
XMIN=1 
XMAX=RANGE # Training set , we will change it to have the best %
GAMETOANALYZE=38-RANGE+1 


if __name__ == '__main__':	
	try:
		database = MySQLdb.connect('localhost', 'root', 'root', 'EPL'); #login, password, database
		season=[1011,1112,1213,1314,1415]
		for i in range (RANGE,RANGE+1): #Just for testing which value was the best -> 3 is the best but we keep that for next try
			RANGE=i
			finalPercentage=0
			for year in season:
				scorePercentage=0
				successPercentage=0
				while (XMAX != 38): # 37 MatchDay so we can predict the last one of the season ---- GAMETOANALYZE different results
					distrib=PoissonDistrib(database,year,XMIN,XMAX,RANGE)
					distrib.averageGoals()
					distrib.getAttackDefence() # We have the values in the DB
					myLambda=Lambda(year,database,XMIN,XMAX,RANGE)
					result=myLambda.calculateLambda()
					scorePercentage+=result[0]
					successPercentage+=result[1]
					XMIN+=1
					XMAX+=1 # We Will now try to predict the XMAX +1 Game
				print("Final Correctness Prediction for season : "+str(year))
				print("Score Success : "    +str(scorePercentage/GAMETOANALYZE)  +"%")
				print("Prediction Result : "+str(successPercentage/GAMETOANALYZE)+"%")
				XMIN=1
				XMAX=RANGE
				finalPercentage+=successPercentage/GAMETOANALYZE
			final("------------------")
			print("for last matches : "+str(i) + ", Final Percentage for the 5 years is : "+str(finalPercentage/5))


		database.close();
		
		
	except (_mysql.Error):
		
		print ("Mysql error ")
		sys.exit(1)