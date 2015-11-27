import _mysql
import MySQLdb
import sys
from math import exp

class PoissonDistrib(object):
	"""We will calculate the Attack and Defence Strength for each them. 
		First Step : Determine the average number of goals per team, per home game, per away games.
		Second Step : For every team, find the number of goals scored last season and / by the number of home games.
		Third Step : Divide step2/step1 to get the Attack's Strength of a team
	"""
	def __init__(self, database,season,xmin,xmax):
		super(PoissonDistrib, self).__init__()
		self.database=database
		self.cursor = database.cursor()
		self.averageHome=0 
		self.averageAway=0
		self.FTAG=0 #Used to construct the total averageHome Goals
		self.FTHG=0
		self.homeAttackStrength =[] 
		self.awayAttackStrength =[]
		self.homeDefenceStrength=[]
		self.awayDefenceStrength=[]
		self.teamList=[]
		self.tmp=[] # Will be used so we dont have to copy paste the code for every situation (attack/defenc home/away)
		self.season=season
		self.beta=0 # Overall Constant expressing the average score in a game
		self.betaHome=0 #Home Advantage
		self.xmin=xmin
		self.xmax=xmax # Variables for the window range we want (1->8) then (2->9) etc to recalculate the lambda

	def averageGoals(self):
		"""
		FTHG = Full-Time Home Goals , FTAG = Full-Time Away Goals
		"""
		self.getScores()
		self.averageHome="{0:.6f}".format((self.FTHG/(380))) #380 = 20*19 = number of game in 1 season 
		self.averageAway="{0:.6f}".format((self.FTAG/(380)))
		self.beta="{0:.4f}".format((self.FTHG+self.FTAG)/(2*380))
		self.betaHome="{0:.4f}".format(float(self.averageHome)-float(self.averageAway))
		

	def getScores(self):
		self.cursor.execute( 
		"SELECT SUM(FTHG) , SUM(FTAG) \
		 FROM championship"+str(self.season)+" \
		 WHERE MatchDay BETWEEN "+str(self.xmin)+" AND "+str(self.xmax)
		 )
		FTG1011=self.cursor.fetchall()
		for elem in FTG1011:
			self.FTHG+=elem[0]
			self.FTAG+=elem[1]
		print(self.FTHG)
		print(self.FTAG)
		print("")

	def getTeam(self):
		self.cursor.execute( 
			"SELECT DISTINCT HomeTeam \
		 	FROM championship"+str(self.season)
		 	)
		teams=self.cursor.fetchall()
		for team in teams:
			if team[0] not in self.teamList:
				self.teamList.append(team[0])

	def getAttackDefence(self):
		self.getTeam()
		self.strength("attack","Home",self.averageHome)
		self.tmp=[]
		self.strength("defence","Away",self.averageHome)
		self.tmp=[]
		self.strength("attack","Away",self.averageAway)
		self.tmp=[]
		self.strength("defence","Home",self.averageAway)
		#self.insertIntoDB()


	def strength(self,atkOrDef,homeOrAway,averageHomeOrAway):
		"""
		Calculate the Attack/Defence Strength for each team and insert the in the Database. We need to put those parameters
		So we dont have to copy paste the code for the Away/Home Attack/defence (x4) cases !
		"""
		for team in self.teamList:
			self.teamGoals(team,atkOrDef,homeOrAway) 
		self.calculateStrength(averageHomeOrAway)

	def teamGoals(self,team,atkOrDef,homeOrAway):
		"""
		Find the number of goals for a team home/away attack/defence strength
		"""
		goal=""
		homeAway=""
		choice=0
		if (atkOrDef=="attack" and homeOrAway=="Home"): #Number of goals scored at home by the home team
			goal="FTHG"
			homeAway="HomeTeam"
		elif (atkOrDef=="defence" and homeOrAway=="Away"): # Number of goals taken by the away team 
			goal="FTHG"
			homeAway="AwayTeam"
			choice=1
		elif (atkOrDef=="attack" and homeOrAway=="Away"): #Number of goals scored away by the home team
			goal="FTAG"
			homeAway="AwayTeam"
			choice=2
		elif (atkOrDef=="defence" and homeOrAway=="Home"): 
			goal="FTAG"
			homeAway="HomeTeam"
			choice=3
		else:
			print("ERROR")
		self.appendToList(choice,goal,homeAway,team)

	def appendToList(self,choice,goal,homeAway,team):
		"""
		The tmp list is used to deal with the 4 different lists, also used for not rewriting the same code
		"""
		self.cursor.execute("SELECT SUM("+goal+"), "+homeAway+" FROM championship"+str(self.season)+" WHERE "+homeAway+"=%s ",(team))
		toFetch=str(self.cursor.fetchone()[0])
		if (toFetch=="None"):
			toFetch=0		
		self.tmp.append(team)
		self.tmp.append(int(toFetch))
		if (choice==0):
			self.homeAttackStrength=self.tmp
		elif (choice==1):
			self.awayDefenceStrength=self.tmp
		elif (choice==2):
			self.awayAttackStrength=self.tmp
		elif (choice==3):
			self.homeDefenceStrength=self.tmp

	def calculateStrength(self,averageHomeOrAway):
		"""
		Will do the basic math to get the Attack/Defence Strength, replace the value in the tmp list
		"""
		count=0
		while (count < len(self.tmp)):
			if (count%2==0): # Its a team
				self.tmp[count+1]=(float(self.tmp[count+1])/(19*1.0)) # *1.0 to get our number if a float format
				self.tmp[count+1]="{0:.4f}".format(((self.tmp[count+1])/(float(averageHomeOrAway))))
			count+=1

	def insertIntoDB(self):
		count=0
		while (count < len(self.tmp)):
			if (count%2==0):
				self.cursor.execute ("""
					   UPDATE ranking"""+str(self.season)+"""
					   SET HomeAttack=%s, HomeDefense=%s, AwayAttack=%s, AwayDefense=%s, Beta=%s, BetaHome=%s
					   WHERE Team=%s
					""", (float(self.homeAttackStrength[count+1]),float(self.homeDefenceStrength[count+1]), \
						  float(self.awayAttackStrength[count+1]),float(self.awayDefenceStrength[count+1]), \
						  float(self.beta) , float("{0:.4f}".format(exp(float(self.betaHome)))), self.tmp[count]))
			count+=1
		self.database.commit()


		
if __name__ == '__main__':	
	try:
		database = MySQLdb.connect('localhost', 'root', 'root', 'EPL'); #login, password, database
		#season=[1011,1112,1213,1314,1415]
		season=[1011]
		print("Inserting Team Strength and Defense in the DB...")
		for year in season:
			distrib=PoissonDistrib(database,year)
			distrib.averageGoals()
			distrib.getAttackDefence()
		database.close();
		
		
	except (_mysql.Error):
		
		print ("Mysql error ")
		sys.exit(1)