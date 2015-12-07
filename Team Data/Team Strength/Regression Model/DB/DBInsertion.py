import _mysql
import MySQLdb
import os
from os import listdir
import time
RANKINGPATH = "../../../Ranking/"
CURRENTSEASON="../../../CurrentSeason/"

class DBInsertion(object):
	"""Insert values of the pre-processed files in the database"""
	def __init__(self,aFile,statOrRank,toLambdaFile):
		super(DBInsertion, self).__init__()
		self.filename=aFile
		self.myfile=open(aFile)
		self.allLambda=[]
		self.statOrRank=statOrRank
		self.lambdaPath="../TeamStrength/"+toLambdaFile+"/"
		try:
			self.database = _mysql.connect('localhost', 'root', 'root', 'EPL2'); #login, password, database
		except (_mysql.Error):
			print ("Error while opening MySQL ")
			sys.exit(1)

	def parsLambdaFile(self,year):
		allFiles=os.listdir(self.lambdaPath)
		for files in allFiles:
			if ("lambda" in files and year in files):
				filename=self.lambdaPath+files
				myfile=open(self.lambdaPath+files)
				year=filename.split(".")
				year=year[2]
				year=str(year[-4])+str(year[-3])+str(year[-2])+str(year[-1])
				line=myfile.readline() # Dont need line #1
				while line != "":
					line=myfile.readline()
					line=line.split(",")
					vec=[]
					if (len(line) >1):
						vec.append(line[0]) # team
						vec.append(line[1]) # attack
						vec.append(line[2]) # defense
						vec.append(line[3]) #beta
						vec.append(line[4].strip("\n")) #betahome
						self.allLambda.append(vec)
					else:
						line=myfile.readline()

	def getYear(self):
		year=self.filename
		if ("Stat" in self.statOrRank):
			year=year[-8:-4]
		else:
			year=year[-10:-5]
			year=year[0]+year[1]+year[3]+year[4] # We have to withdraw the - sign (10-11)
		return year # Return 1011 / 1112 / 1213 or 1314

	def parse(self):
		line=self.myfile.readline()
		while (line !=""):
			line=line.strip("\n")
			attributes=line.split("#")
			if (self.statOrRank=="Stat"):
				self.insertStats(attributes)
			elif(self.statOrRank=="Rank"):
				self.insertRank(attributes)
			else:
				self.insertCurrentSeason(attributes)
			line=self.myfile.readline()
		try:
			self.database.close();
		except (_mysql.Error):
			print ("Error while closing MySQL ")
			sys.exit(1)


	def insertCurrentSeason(self,attr): 
		year=self.getYear()
		firstline=firstline="INSERT INTO championship"+year+" (GameDate,HomeTeam,AwayTeam,FTHG,FTAG,MatchDay) VALUES "
		mydate=self.convertToDateTime(attr[0])
		query="(\""+mydate+"\", \""+attr[1]+"\", \""+attr[2]+"\", \""+attr[3]+"\", \""+attr[4]+"\", \""+attr[5]+"\" ); \n"
		finalRequest=firstline+query
		self.database.query(finalRequest)

	def convertToDateTime(self,date):
		splittedDate=date.split("/")
		finalDate=str(20)+splittedDate[2]+splittedDate[1]+splittedDate[0]
		return finalDate

	def insertStats(self,attr): 
		year=self.getYear()
		firstline=firstline="INSERT INTO championship"+year+" (GameDate,HomeTeam,AwayTeam,FTHG,FTAG,HC,AC,HY,AY,HR,AR,B365H,B365D,B365A,BWH,BWD,BWA,MatchDay) VALUES "
		mydate=self.convertToDateTime(attr[0])
		query="(\""+mydate+"\", \""+attr[1]+"\", \""+attr[2]+"\", \""+attr[3]+"\", \""+attr[4]+"\", \""+attr[5]+"\", \""+attr[6]+"\", \""+attr[7]+"\", \""+attr[8]+"\", \""+attr[9]+"\", \""+attr[10]+"\",\""+attr[11]+"\", \""+attr[12]+"\", \""+attr[13]+"\", \""+attr[14]+"\", \""+attr[15]+"\", \""+attr[16]+"\", \""+attr[17]+"\" ); \n"
		finalRequest=firstline+query
		self.database.query(finalRequest)

	def insertRank(self,attr):
		newlst=[]
		for elem in attr:
			if (elem!=""):
				newlst.append(elem)
		attr=newlst
		year=self.getYear()
		self.allLambda=[]
		self.parsLambdaFile(year)
		if len(attr)>1:
			for team in self.allLambda:
				teamname=team[0]
				teamname=teamname.replace("\"","")
				if teamname==attr[1]:
					firstline=firstline="INSERT INTO ranking"+year+" (Rank,Team,Played,Wins,Draws,Losses,GoalsFor,GoalsAgainst,GoalsDIFF,Points,Attack,Defense,Beta,BetaHome) VALUES "
					query="(\""+attr[0]+"\",\""+attr[1]+"\", \""+attr[2]+"\", \""+attr[3]+"\", \""+attr[4]+"\", \""+attr[5]+"\", \""+attr[6]+"\", \""+attr[7]+"\", \""+attr[8]+"\", \""+attr[9]+"\", \""+team[1]+"\", \""+team[2]+"\", \""+team[3]+"\", \""+team[4]+"\" ); \n"
					finalRequest=firstline+query
					self.database.query(finalRequest)
