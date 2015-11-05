import os
from os import listdir
import time
PATH = "../Ranking/"
"""
rank
team
played
wins
draws
losses
goals-for
goals-against
goals-dff
points
"""
class Parser(object):
	"""Pars the Ranking files"""
	def __init__(self, filename):
		super(Parser, self).__init__()
		self.filename=filename
		self.file = open(filename)
		self.textToKeep=""

	def pars(self):
		line=self.file.readline() # First line is useless
		while (line != "") : # End of the data
			attributes=[]
			line=self.file.readline() # Beginning of a set of data {
			for i in range(10): # We want 10 elements
				line=self.file.readline()
				attributes.append(line)
			self.processeAttr(attributes)
			line=self.file.readline() # The end of the data set for a team }
		self.filesHandler()

	def clean(self,elem):
		elem=elem.strip("\n")
		elem=elem.strip("\r")
		elem=elem.strip(" ")
		elem=elem.strip(",")
		elem=elem.strip("\"")
		return elem

	def setName(self,name): # Team names don't have the same format, we will change it here
		if (name=="Manchester United"):
			name="Man United"
		elif (name=="Manchester City"):
			name="Man City"
		elif ("Tottenham" in name):
			name="Tottenham"
		elif ("West Brom" in name):
			name="West Brom"
		elif ("Newcastle" in name):
			name="Newcastle"
		elif ("Stoke" in name):
			name="Stoke"
		elif ("Bolton" in name):
			name="Bolton"
		elif ("Blackburn" in name):
			name="Blackburn"
		elif ("Wigan" in name):
			name="Wigan"
		elif ("Wolve" in name): #Wolverhampton Wanderers
			name="Wolves"
		elif("Birmingham" in name):
			name="Birmingham"
		elif("West Ham" in name):
			name="West Ham"
		elif("Queen" in name):
			name="QPR"
		elif("Swansea" in name):
			name="Swansea"
		elif ("Norwich" in name):
			name="Norwich"
		elif("Cardiff" in name):
			name="Cardiff"
		elif("Hull" in name):
			name="Hull"
		elif("Leicester" in name):
			name="Leicester"
		
		return name


	def processeAttr(self,attrib):
		i=0
		if (attrib[0]!=""):
			while (i < len(attrib)):
				elem=self.clean(attrib[i])
				toAdd=elem.split(":")
				toAdd=toAdd[1] # We want the part after the : 
				if ("\"" in toAdd):
					toAdd=toAdd[1:]
				if ("+" in toAdd):
					toAdd=toAdd[1:]
				if (i==1):
					toAdd=self.setName(toAdd)
				if (i!= len(attrib)-1):
					self.textToKeep=self.textToKeep+toAdd+"#"
				else:
					self.textToKeep+=toAdd
				i+=1
		self.textToKeep+="\n"


	def filesHandler(self):
		myfile= open("Processed"+self.filename,"w")
		myfile.write(self.textToKeep)
		myfile.close()
		self.file.close()
		
		

		
if __name__ == '__main__':	
	allFiles=os.listdir(PATH)
	for files in allFiles:
		if (".json" in files and not "Processed" in files):
			myParser=Parser(files)
			myParser.pars()