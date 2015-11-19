import _mysql
import os
from os import listdir
import time
STATSPATH = "../Stats/"
RANKINGPATH = "../Ranking/"
CURRENTSEASON="../CurrentSeason/"

class DBInsertion(object):
	"""Insert values of the pre-processed files in the database"""
	def __init__(self,aFile,statOrRank):
		super(DBInsertion, self).__init__()
		self.filename=aFile
		self.myfile=open(aFile)
		self.statOrRank=statOrRank

		try:
			self.database = _mysql.connect('localhost', 'root', 'root', 'EPL'); #login, password, database
		except (_mysql.Error):
			print ("Error while opening MySQL ")
			sys.exit(1)

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

	def convertToDateTime(self,date):
		splittedDate=date.split("/")
		finalDate=str(20)+splittedDate[2]+splittedDate[1]+splittedDate[0]
		return finalDate

	def insertCurrentSeason(self,attr): 
		year=self.getYear()
		firstline=firstline="INSERT INTO championship"+year+" (GameDate,HomeTeam,AwayTeam,FTHG,FTAG,MatchDay) VALUES "
		mydate=self.convertToDateTime(attr[0])
		query="(\""+mydate+"\", \""+attr[1]+"\", \""+attr[2]+"\", \""+attr[3]+"\", \""+attr[4]+"\", \""+attr[5]+"\" ); \n"
		finalRequest=firstline+query
		self.database.query(finalRequest)

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
		if len(attr)>1:
			firstline=firstline="INSERT INTO ranking"+year+" (Rank,Team,Played,Wins,Draws,Losses,GoalsFor,GoalsAgainst,GoalsDIFF,Points) VALUES "
			query="(\""+attr[0]+"\",\""+attr[1]+"\", \""+attr[2]+"\", \""+attr[3]+"\", \""+attr[4]+"\", \""+attr[5]+"\", \""+attr[6]+"\", \""+attr[7]+"\", \""+attr[8]+"\", \""+attr[9]+"\" ); \n"
			finalRequest=firstline+query
			self.database.query(finalRequest)

if __name__ == '__main__':	
	start_time = time.time()
	allFiles=os.listdir(RANKINGPATH)
	print("Inserting Ranks into the DB, this may take some while ...")
	for files in allFiles:
		if ("Processed" in files):
			insertion=DBInsertion(RANKINGPATH+files,"Rank")
			insertion.parse()
	print("Done !")

	allFiles=os.listdir(STATSPATH)
	print("Inserting Statistics into the DB, this may take some while ...")
	for files in allFiles:
		if ("Processed" in files):
			insertion=DBInsertion(STATSPATH+files,"Stat")
			insertion.parse()
	print("Done !")
	allFiles=os.listdir(CURRENTSEASON)
	print("Inserting Latest season into the DB, this may take some while ...")
	for files in allFiles:
		if ("epl" in files):
			insertion=DBInsertion(CURRENTSEASON+files,"Rank")
			insertion.parse()
			pass
		elif ("Stats" in files):
			insertion=DBInsertion(CURRENTSEASON+files,"StatCurrent")
			insertion.parse()
		
	print("Done !")

	print("--- %s seconds ---" % (time.time() - start_time))