import _mysql
import MySQLdb
import sys
from teamStrength import *
from calculateLambda import *
from prediction import *

GAMESTOADAPT=6 # After the 10-11 season, for every season we will take X Games to adapt our new lambda values 
XMIN=1
XMAX=GAMESTOADAPT
CURRENTMATCHDAY=12 # To change every week , represent the match day in the new current season

if __name__ == '__main__':	
	try:
		database = MySQLdb.connect('localhost', 'root', 'root', 'EPL'); #login, password, database
		season=[1011,1112,1213,1314,1415,1516]
		count=0
		while (count < len(season)-1): # We stop after predicting the 2014 2015 season because we dont have the data for after
			if (season!=1415):
				distrib=PoissonDistrib(database,season[count],1,38,38) # We take all games from last season
				distrib.averageGoals()
				distrib.getAttackDefence() # We have the values in the DB
			else:
				distrib=PoissonDistrib(database,season[count],1,CURRENTMATCHDAY,CURRENTMATCHDAY) # We take all current played games
				distrib.averageGoals()
				distrib.getAttackDefence() # We have the values in the DB
		# We Make prediction for the X first games of the current season to predict
			XMIN=1
			XMAX=GAMESTOADAPT
			distrib=PoissonDistrib(database,season[count+1],XMIN,XMAX,GAMESTOADAPT) # We take the first X games of  the next season
			distrib.averageGoals()
			distrib.getAttackDefence() # We have the values in the DB
		# Now We will make the average of last season and the GAMESTOADAPT from the new season
		# Make Ponderation here and put it again in the new DB
			myPonderation=DBPonderation(database,season[count],season[count+1])
			myPonderation.makePonderation()
		# Now we can calculate the prediction correctness we will have
			XMIN=GAMESTOADAPT
			XMAX=XMIN
			scorePercentage=0
			successPercentage=0

			if (season[count]!=1415): #Decomment to get the results of every single year prediction
				
				while (XMAX != 38): # 37 MatchDay so we can predict the last one of the season ---- GAMETOANALYZE different results
					myLambda=Lambda(season[count+1],database,XMIN,XMAX,0) # Predict Game XMAX+1 -> Next Game
					result=myLambda.calculateLambda() # 0 = we dont want a print
					scorePercentage+=result[0]
					successPercentage+=result[1]
					XMIN+=1
					XMAX+=1 # Predict the Next Game
				#print("Final Correctness Prediction for season : "+str(season[count+1]))
				#print("Score Success : "    +str((scorePercentage*1.0) /(38-GAMESTOADAPT))+"%")
				#print("Prediction Result : "+str((successPercentage*1.0) /(38-GAMESTOADAPT))+"%")
				
			else:
				while (XMAX != CURRENTMATCHDAY+1): # Current Match Day +1
					myLambda=Lambda(season[count+1],database,XMIN,XMAX,CURRENTMATCHDAY) # Predict Game XMAX+1 -> Next Gamehost
					result=myLambda.calculateLambda()
					scorePercentage+=result[0]
					successPercentage+=result[1]
					XMIN+=1
					XMAX+=1 # Predict the Next Game
				#print("Final Correctness Prediction for season : "+str(season[count+1]))
				#print("Score Success : "    +str((scorePercentage*1.0) /(CURRENTMATCHDAY-GAMESTOADAPT))+"%")
				#print("Prediction Result : "+str((successPercentage*1.0) /(CURRENTMATCHDAY-GAMESTOADAPT))+"%")
			count+=1

		database.close();
		
		
	except (_mysql.Error):
		
		print ("Mysql error ")
		sys.exit(1)