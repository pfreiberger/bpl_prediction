class Parser(object):
	"""Parse the outcome file to process the statistics"""
	def __init__(self, aFile):
		super(Parser, self).__init__()
		self.file = open(aFile,"r")
		self.processedFile= open("ProcessedStats1516.csv","w")
		self.finalLine=""
		self.matchday=""
		self.date=""
		self.game=""

	def pars(self):
		lines=self.file.readlines()
		for line in lines:
			if ("Matchday") in line:
				self.matchday=self.getMatchDay(line) 
			elif ("[") in line:
				self.date=self.getDate(line)
			elif ("-" in line):
				self.game=self.getGame(line)
				self.finalLine+=self.date+"#"+self.game+"#"+self.matchday
		self.processedFile.write(self.finalLine)
		self.file.close()
		self.processedFile.close()


	def getGame(self,line):
		lst=line.split(" ") # We split our line
		newlst=[]
		for elem in lst:
			if elem!="":
				newlst.append(elem)
		homeTeam=newlst[0]+newlst[1] # Home Team is alway element 0 and 1, but sometimes the home team is 3 words composed so it has to be ealt with
		for i in range(2,4):
			if ("-" in newlst[i]):  # If there is a - caracter, it means that the game has not been played yet
				if (newlst[i]=="-"): 
					FTHG=-1 # And we put -1 to say this
					FTAG=-1
				else:
					FTHG=newlst[i][0] # Otherwise we take the score
					FTAG=newlst[i][2]
				awayTeam=newlst[i+1]+newlst[i+2].strip("\n") # and the away team name

		homeTeam=self.setName(homeTeam)
		awayTeam=self.setName(awayTeam)
		game=homeTeam+"#"+awayTeam+"#"+str(FTHG)+"#"+str(FTAG)
		return game
			


	def getMatchDay(self,line):
		lst=line.split(" ")
		matchday=lst[1]
		return str(matchday)

	def getDate(self,line):
		date=line.split("[") # We only play on the string to get the date in the format we want
		date=date[1].split("]")
		date=date[0]
		date=date.split(" ")
		date=date[1]
		date=date.split("/")
		day=date[1]
		if int(day) < 10:
			day="0"+str(day)
		finalDate=str(day)+"/"+self.getMonthDate(date[0])+"/"+"15"
		return finalDate

	def getMonthDate(self,month): # We only took the first half of the new season
		value=0
		if month=="Aug":
			value="08"
		elif month=="Sept":
			value="09"
		elif month=="Oct":
			value="10"
		elif month=="Nov":
			value="11"
		elif month=="Dec":
			value="12"
		else:
			value="-1"
		return str(value)

	def setName(self,name): # Team names don't have the same format, we will change it here
		if ("ManchesterUnited"==name):
			name="Man United"
		elif ("Arsenal" in name):
			name="Arsenal"
		elif ("Everton" in name):
			name="Everton"
		elif ("Chelsea" in name):
			name="Chelsea"
		elif ("Liverpool" in name):
			name="Liverpool"
		elif("Southampton" in name):
			name="Southampton"
		elif ("ManchesterCity"==name):
			name="Man City"
		elif ("Tottenham" in name):
			name="Tottenham"
		elif ("West Brom" in name):
			name="West Brom"
		elif ("WestBrom" in name):
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
		elif("WestHam" in name):
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
		elif("CrystalPalace" in name):
			name="Crystal Palace"
		elif("Leicester" in name):
			name="Leicester"
		elif ("AFCBournemouth"==name):
			name="Bournemouth"
		elif ("SunderlandAFC"==name):
			name="Sunderland"
		elif ("Watford" in name):
			name="Watford"
		elif ("AstonVilla" in name):
			name="Aston Villa"
		return name


myParser=Parser("Season1516.txt")
myParser.pars()

		