import _mysql
import MySQLdb
import sys
from math import *
GAMESTOADAPT=6
NEWTEAMLAMBDA=-0.5

class DBPonderation(object):
	"""docstring for DBPonderation"""
	def __init__(self, database,season1,season2):
		super(DBPonderation, self).__init__()
		self.database = database
		self.season1=season1
		self.season2=season2
		self.cursor = database.cursor()
		self.table1Rows=[]
		self.table2Rows=[]
		self.beta=0
		self.betaHome=0

	def makePonderation(self):
		self.table1Rows=self.getRows(self.season1) # Previous Season
		self.table2Rows=self.getRows(self.season2) # Current Season
		for S2Team in self.table2Rows:
			newTeam=True
			for S1Team in self.table1Rows:
				if ( S2Team[0].strip(" ")== S1Team[0].strip(" ")): # If the team in season 2 is also in season 1 , we make the ponderation
					vec=[]
					newTeam=False
					for attrib in range (1 , len(S2Team)):
						term1=(38*exp(float(S1Team[attrib])))/(38+GAMESTOADAPT)
						term2=(GAMESTOADAPT*exp(float(S2Team[attrib])))/(38+GAMESTOADAPT*1.0)
						res=log(term1+term2)
						if (S2Team[0]=="Man United" and attrib==len(S2Team)-1):
							self.betaHome=res
						elif (S2Team[0]=="Man United" and attrib==len(S2Team)-2):
							self.beta=res
						vec.append(res)
					self.updateValue(S2Team[0],vec)
			if (newTeam == True): # IF its a new team in the championship
				vec=[]
				for attrib in range (1 , len(S2Team)):
					term1=(38*exp(NEWTEAMLAMBDA))/(38+GAMESTOADAPT)
					term2=(GAMESTOADAPT*exp(float(S2Team[attrib])))/(38+GAMESTOADAPT*1.0)
					res=log(term1+term2)
					vec.append(res)
				self.updateValue(S2Team[0],vec)
		self.giveSameBeta()
			


	def updateValue(self,team,vec):
		self.cursor.execute ("""
					   UPDATE ranking"""+str(self.season2)+"""
					   SET Attack=%s, Defense=%s, Beta=%s, BetaHome=%s
					   WHERE Team=%s
					""", (float("{0:.4f}".format(float(vec[0]))),float("{0:.4f}".format(float(vec[1]))), \
						  float("{0:.4f}".format(float(vec[2]))),float("{0:.4f}".format(float(vec[3]))), team))
		self.database.commit()

	def giveSameBeta(self):
		"""
		If a new team joins the league, she doesn't has the right Beta score and Beta Home score because we still makes an average
		"""
		for S2Team in self.table2Rows:
			newTeam=True
			for S1Team in self.table1Rows:
				if ( S2Team[0].strip(" ")== S1Team[0].strip(" ")): # If the team in season 2 is also in season 1 , we make the ponderation
					vec=[]
					newTeam=False
			if (newTeam==True):
				self.cursor.execute (
					"""
					   UPDATE ranking"""+str(self.season2)+"""
					   SET Beta=%s, BetaHome=%s
					   WHERE Team=%s
					""", (float("{0:.4f}".format(float(self.beta))),float("{0:.4f}".format(float(self.betaHome))), S2Team[0]))
		self.database.commit()

	def getRows(self,season):
		self.cursor.execute( 
			"SELECT Team, Attack,Defense,Beta,BetaHome \
		 	FROM ranking"+str(season)
		 	)
		rows=self.cursor.fetchall()
		res=[]
		for elem in rows:
			count=0
			tmp=[]
			while (count < len(elem)):
				tmp.append(str(elem[count]))
				count+=1
			res.append(tmp)
		return res