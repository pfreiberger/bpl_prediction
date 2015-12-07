import os
from os import listdir


class Parser(object):
	"""docstring for Parser"""
	def __init__(self, filename):
		super(Parser, self).__init__()
		self.file=open(filename)
		self.newFile=open("Processed"+filename,"w")

	def pars(self):
		res=""
		for line in self.file:
			if (not "Date" in line) : #First Line 
				line=line.split(",")
				res+=line[1]+","+line[2]+","+str(line[3][0])+","+str(line[3][2])+"\n"
		self.newFile.write(res)
		self.file.close()
		self.newFile.close()


allFiles = filter(os.path.isfile, os.listdir( os.curdir ) )  # files only
for files in allFiles:
	if ("league" in files and not ("Processed") in files):
		print(files)
		myParser=Parser(files)
		myParser.pars()




