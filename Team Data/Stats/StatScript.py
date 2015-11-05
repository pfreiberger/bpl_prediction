import os
from calendar import monthrange
TEAMNUMB=20
path="../Stats/"
"""
FORMAT of the Processed Files :
Date = Match Date (dd/mm/yy)  	
HomeTeam = Home Team            
AwayTeam = Away Team                    
FTHG = Full Time Home Team Goals        
FTAG = Full Time Away Team Goals        
HC = Home Team Corners                  
AC = Away Team Corners
HY = Home Team Yellow Cards
AY = Away Team Yellow Cards
HR = Home Team Red Cards
AR = Away Team Red Cards
B365H = Bet365 home win odds
B365D = Bet365 draw odds
B365A = Bet365 away win odds
BWH = Bet&Win home win odds
BWD = Bet&Win draw odds
BWA = Bet&Win away win odds
MatchDay
"""
listAttrib=["Date","HomeTeam","AwayTeam","FTHG","FTAG","HC","AC","HY","AY","HR","AR",\
			   "B365H","B365D","B365A","BWH","BWD","BWA"]

class Parser(object):
	"""Pars the data for every team and season"""
	def __init__(self, fileName):
		super(Parser, self).__init__()
		self.filename=fileName
		self.file = open(fileName)
		self.textToKeep=""
		self.attribPos=[]

	def getAttribPos(self):
		firstline=self.file.readline()
		counter=0
		firstline=firstline.split(",")
		while (counter < len(firstline)):
			if (firstline[counter] in listAttrib):
				self.attribPos.append(counter)
			counter+=1


	def parse(self):
		line=self.file.readline() # This is the second line
		valueList=line.split(",")
		matchDay=1
		while (line!=""):
			for i in range(10): # One match day = 1 game for a team -> 20 teams = 10 match then it is an other match day
				for posNumber in self.attribPos:
					self.textToKeep+=valueList[posNumber]
					self.textToKeep+="#"
				self.textToKeep+=str(matchDay)
				self.textToKeep+="\n"
				line=self.file.readline()
				valueList=line.split(",")
			matchDay+=1
		self.filesHandler()

	def filesHandler(self):
		myfile= open("Processed"+self.filename,"w")
		myfile.write(self.textToKeep)
		myfile.close()
		self.file.close()


if __name__ == '__main__':	
	counter=1
	for afile in os.listdir(path):
		if ((afile.endswith(".csv")) and not( "Processed" in afile)):
			print("Pre-Processing file number : "+ str(counter))
			myParser=Parser(afile)
			myParser.getAttribPos()
			myParser.parse()
			counter+=1
