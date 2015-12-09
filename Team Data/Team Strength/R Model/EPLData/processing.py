import os
from os import listdir


class Parser(object):
	"""Pars the .csv file because we need a different input for our R script."""
	def __init__(self, filename,specialCSV):
		super(Parser, self).__init__()
		self.file=open(filename)
		self.newFile=open("Processed"+filename,"w")
		self.specialCSV=specialCSV

	def pars(self):
		if self.specialCSV==0:
			res=""
			for line in self.file:
				if (not "Date" in line) : #First Line 
					line=line.split(",")
					res+=line[1]+","+line[2]+","+str(line[3][0])+","+str(line[3][2])+"\n"
			self.newFile.write(res)
			self.file.close()
			self.newFile.close()
		else:
			res=""
			for line in self.file:
				if(not"Date" in line):
					line=line.split(",")
					res+=line[2]+","+line[3]+","+str(line[4])+","+str(line[5])+"\n"
			self.newFile.write(res)
			self.file.close()
			self.newFile.close()


allFiles = filter(os.path.isfile, os.listdir( os.curdir ) )  # files only
for files in allFiles:
	if ("league" in files and not ("Processed") in files):
		if ("1415" in files or "1516" in files):
			myParser=Parser(files,1)
			myParser.pars()
		else:
			myParser=Parser(files,0)
			myParser.pars()

		




