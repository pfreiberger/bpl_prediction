import _mysql
import MySQLdb
import sys

class Ranking(object):
	"""docstring for Ranking"""
	def __init__(self, aFile,database):
		super(Ranking, self).__init__()
		self.database = database
		self.file = open(aFile,"r")
		self.ranking=open("Processedepl-15-16.json","w")
		self.allTeams=[]
		self.aTeam=[0,"",0,0,0,0,0,0,0,0] #Rank , Team Name , Played, Wins , Draw, Lost ,GoalsFor, GoalsAgainst, GoalsDiff, Points
		self.allLines=self.file.readlines()
		self.generalRanking=[]
		self.cursor = self.database.cursor()

	def calculateRanking(self):
		self.getTeams()
		for team in self.allTeams:
			self.generalRanking.append(self.getScore(team))
			self.aTeam=[0,"",0,0,0,0,0,0,0,0]
		count=1
		# We need to find the team with the highest number of points
		# Delete it from the list
		# Do It Again
		tmp=self.generalRanking
		rank=1
		while (len(tmp)>0):
			score=0
			diffGoal=-999
			bestRank=""
			for team in tmp:
				if team[9]>score: # Get The best Team
					score=team[9]
					diffGoal=team[8]
					bestRank=team[1] # We keep the name of the best team in the current tmp lst
				elif team[9]==score:
					if (team[8]>diffGoal):
						score=team[9]
						diffGoal=team[8]
						bestRank=team[1] # We keep the name of the best team in the current tmp lst

			# We got the best team in the current tmp lst
			for team in self.generalRanking:
				if (team[1]==bestRank):
					team[0]=rank
					rank+=1
			i=0
			while (i < len(tmp)):
				if (tmp[i][1]==bestRank):
					newlst=[]
					for elem in tmp:
						if elem[1]!=bestRank:
							newlst.append(elem)
					tmp=newlst
					i=99999
				i+=1
		self.sortTeamByRanking()
		self.generateRankingFile()
		self.DBUpdate()

	def sortTeamByRanking(self):
		newlst=[]
		current=1
		while current <=20:
			for team in self.generalRanking:
				if team[0]==current:
					newlst.append(team)
					current+=1
		self.generalRanking=newlst
		
	def generateRankingFile(self):
		for team in self.generalRanking:
			line=""
			count=0
			while count< len(team):
				line+="#"+str(team[count])
				count+=1
			line+="\n"
			self.ranking.write(line)
		self.ranking.close()
		self.file.close()

	def DBUpdate(self):
		for team in self.generalRanking:
			self.cursor.execute ("""
						   UPDATE ranking1516
						   SET Rank=%s, Team=%s, Played=%s , Wins=%s,Draws=%s,Losses=%s,GoalsFor=%s , GoalsAgainst=%s,GoalsDIFF=%s,Points=%s\
						   WHERE Team=%s
						""",(team[0],team[1],team[2],team[3],team[4],team[5],team[6],team[7],team[8],team[9],team[1])) 
		self.database.commit()


	def getTeams(self):
		for i in range(10): # So we can get the 20 teams
			line=self.allLines[i]
			line=line.split("#")
			self.allTeams.append(line[1])
			self.allTeams.append(line[2])

	def getScore(self,aTeam):
		self.aTeam[1]=aTeam
		for line in self.allLines:
			if (not "-1" in line ):
				line=line.split("#")
				if (line[1]==aTeam):
					self.homeScore(line)
				elif (line[2]==aTeam):
					self.awayScore(line)
		self.aTeam[2]=self.aTeam[3]+self.aTeam[4]+self.aTeam[5]
		self.aTeam[8]=self.aTeam[6]-self.aTeam[7]
		return self.aTeam

	def homeScore(self,line):
		if (line[3]>line[4]):
			self.aTeam[3]+=1 # Add a win
			self.aTeam[9]+=3
		elif (line[3]==line[4]):
			self.aTeam[4]+=1 # Add a Draw
			self.aTeam[9]+=1
		else:
			self.aTeam[5]+=1 # Add a Lose
		self.aTeam[6]+=int(line[3]) # We add the goals they scored
		self.aTeam[7]+=int(line[4]) # We add the goals they took

	def awayScore(self,line):
		if (line[4]>line[3]):
			self.aTeam[3]+=1 # Add a win
			self.aTeam[9]+=3
		elif (line[3]==line[4]):
			self.aTeam[4]+=1 # Add a Draw
			self.aTeam[9]+=1
		else:
			self.aTeam[5]+=1 # Add a Lose
		self.aTeam[6]+=int(line[4]) # We add the goals they scored
		self.aTeam[7]+=int(line[3]) # We add the goals they took


if __name__ == '__main__':	
	try:
		database = MySQLdb.connect('localhost', 'root', 'root', 'EPL'); #login, password, database
		myRank=Ranking("ProcessedStats1516.csv",database)
		myRank.calculateRanking()
		database.close();
		
	except (_mysql.Error):
		
		print ("Mysql error ")
		sys.exit(1)
		