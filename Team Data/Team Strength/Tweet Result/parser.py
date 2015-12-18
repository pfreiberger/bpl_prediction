class Parser(object):
	"""Parse the tweets results file"""
	def __init__(self, filename):
		super(Parser, self).__init__()
		self.filename = open(filename,"r")
		self.finalVec=[]
		self.kappaMatrix=[[0 for i in range(3)] for i in range(3)]
		self.gamePercentage=[]

	def confusionMatrix(self):
		"""
		Kappa Matrix ,  proba[0]=Home Win, proba[1]=Away Win , proba[2]=Draw
			Prediction
			W L D
		W 	- - -   Real
		L   - - -   Sco
		D   - - -   re
		Return a confusion matrix
		"""
		for game in self.finalVec:
			proba=[]
			proba.append(game[4]) # Home win
			proba.append(game[6]) # Away Win
			proba.append(game[5]) # Draw
			if game[2]==1: # If the Home Team Won
				if (proba[0]>proba[1] and proba[0]>proba[2]): #If we predicted a win
					self.kappaMatrix[0][0]+=1 # True Positive , we add 1 on the W-W diagonal
				elif (proba[1]>proba[0] and proba[1]>proba[2]): #If we predicted an away win
					self.kappaMatrix[0][1]+=1
				else: #Draw
					self.kappaMatrix[0][2]+=1
			elif game[2]==0:
				if (proba[0]>proba[1] and proba[0]>proba[2]): #If we predicted a win
					self.kappaMatrix[2][0]+=1 # True Positive , we add 1 on the D-D diagonal
				elif (proba[1]>proba[0] and proba[1]>proba[2]): #If we predicted an away win
					self.kappaMatrix[2][1]+=1
				else: #Draw
					self.kappaMatrix[2][2]+=1
			else: # Away win
				if (proba[0]>proba[1] and proba[0]>proba[2]): #If we predicted a win
					self.kappaMatrix[1][0]+=1 # True Positive , we add 1 on the L-Ldiagonal
				elif (proba[1]>proba[0] and proba[1]>proba[2]): #If we predicted an away win
					self.kappaMatrix[1][1]+=1
				else: #Draw
					self.kappaMatrix[1][2]+=1
		return self.kappaMatrix

	def printMatrix(self):
		print("	Predicted result  ")
		vector=["W","L","D"]
		print(" 	W 	L 	D")
		print("")
		for i in range(3):
			print vector[i],
			for j in range(3):
				print self.kappaMatrix[i][j],
				print "   ",
			print("")

	def givePercentage(self):
		count=0
		toPass=0 # We start predicting after the 6th week = 60 games. But we only took 7 games per week coz we cant predict for 3 teams 
		for game in self.finalVec:
			if toPass>42: # --> 6*7 = 42 then we predict
				tmp=[]
				tmp.append(game[0])
				tmp.append(game[1])
				tmp.append(float("{0:.3}".format(float(game[4])*100)))
				tmp.append(float("{0:.3}".format(float(game[5])*100)))
				tmp.append(float("{0:.3}".format(float(game[6])*100)))
				self.gamePercentage.append(tmp)
			count+=1
			toPass+=1
		print(self.gamePercentage)

	def parse(self):
		"""
		Vector looks like 
		[Home , Away, Outcome(-1,0,1), Predicted outcome, home_win %, draw %, away_win %]
		"""
		lines=self.filename.readlines() # Useless line
		count=0
		for line in lines:
			if not "home" in line: # Line 1
				tmp=[]
				attributes=line.split(",")
				if str(attributes[5]) != "-1":
					tmp.append(attributes[0]) # Home Team
					tmp.append(attributes[1]) # Away Team
					tmp.append(self.giveOutcome(attributes[2],attributes[3])) # Home and Away score
					tmp.append(self.givePredictedOutcome(attributes[7],attributes[6],attributes[5]))
					tmp.append(attributes[7].strip("\n").strip("\r"))
					tmp.append(attributes[6].strip("\r").strip("\n"))
					tmp.append(attributes[5].strip("\r").strip("\n"))
					self.finalVec.append(tmp)
		return self.finalVec


	def giveOutcome(self,homeScore,awayScore):
		outcome=0
		if homeScore>awayScore:
			outcome=1
		elif homeScore==awayScore:
			outcome=0
		else:
			outcome=-1
		return outcome

	def givePredictedOutcome(self,home,draw,away):
		outcome=0
		if home>away and home>draw:
			outcome=1
		elif away>home and away>draw:
			outcome=-1
		else:
			outcome=0
		return outcome
