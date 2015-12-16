import _mysql
import MySQLdb
import sys

statPercentage=[[['Tottenham', 'Man City', 15.0, 24.6, 60.8], ['Leicester', 'Arsenal', 26.5, 25.4, 48.6], ['Liverpool', 'Aston Villa', 57.1, 26.2, 17.3], ['Man United', 'Sunderland', 75.1, 16.5, 8.49], ['Southampton', 'Swansea', 49.5, 29.3, 22.1], ['Newcastle', 'Chelsea', 12.0, 17.5, 70.6], ['West Brom', 'Everton', 27.8, 31.8, 41.7]], [['Arsenal', 'Man United', 46.7, 27.1, 26.9], ['Aston Villa', 'Stoke', 30.3, 29.8, 40.9], ['Chelsea', 'Southampton', 58.6, 22.6, 19.0], ['Crystal Palace', 'West Brom', 49.7, 29.1, 22.0], ['Everton', 'Liverpool', 54.0, 26.0, 20.5], ['Man City', 'Newcastle', 89.9, 7.73, 2.29], ['Sunderland', 'West Ham', 21.4, 24.5, 54.6], ['Swansea', 'Tottenham', 38.6, 31.3, 31.4]], [['Chelsea', 'Aston Villa', 83.9, 11.1, 4.96], ['Crystal Palace', 'West Ham', 39.2, 25.7, 35.6], ['Everton', 'Man United', 39.4, 27.3, 34.1], ['Southampton', 'Leicester', 58.9, 22.8, 18.5], ['Swansea', 'Stoke', 48.9, 28.2, 23.6], ['Tottenham', 'Liverpool', 50.6, 27.7, 22.3], ['West Brom', 'Sunderland', 50.0, 30.7, 20.3]], [['Arsenal', 'Everton', 50.9, 27.1, 22.6], ['Aston Villa', 'Swansea', 24.8, 30.9, 45.4], ['Leicester', 'Crystal Palace', 42.3, 25.0, 33.1], ['Liverpool', 'Southampton', 31.1, 30.4, 39.7], ['Man United', 'Man City', 19.7, 25.2, 55.6], ['Sunderland', 'Newcastle', 40.5, 29.8, 30.8], ['West Ham', 'Chelsea', 29.4, 22.8, 48.0]], [['Chelsea', 'Liverpool', 72.1, 17.0, 10.9], ['Crystal Palace', 'Man United', 32.0, 26.4, 42.1], ['Everton', 'Sunderland', 69.0, 20.1, 11.1], ['Newcastle', 'Stoke', 32.6, 28.5, 39.8], ['Swansea', 'Arsenal', 29.7, 31.1, 40.4], ['Tottenham', 'Aston Villa', 64.6, 23.1, 12.7], ['West Brom', 'Leicester', 38.7, 29.2, 33.1]], [['Arsenal', 'Tottenham', 52.6, 27.3, 20.8], ['Aston Villa', 'Man City', 5.4, 14.8, 79.9], ['Liverpool', 'Crystal Palace', 40.9, 28.3, 31.6], ['Man United', 'West Brom', 62.5, 23.9, 14.0], ['Stoke', 'Chelsea', 19.6, 21.7, 58.9], ['Sunderland', 'Southampton', 18.9, 27.1, 54.7], ['West Ham', 'Everton', 43.7, 25.8, 31.0]], [['Crystal Palace', 'Sunderland', 62.5, 22.7, 15.0], ['Everton', 'Aston Villa', 68.0, 20.9, 11.4], ['Man City', 'Liverpool', 81.2, 13.7, 5.18], ['Newcastle', 'Leicester', 32.1, 25.8, 42.7], ['Southampton', 'Stoke', 57.6, 25.0, 17.8], ['Tottenham', 'West Ham', 43.8, 26.6, 30.2], ['West Brom', 'Arsenal', 22.0, 31.1, 48.0]]]
tweetPercentage=[['tottenham', 'man_city', 27.8, 17.7, 54.5], ['leicester', 'arsenal', 20.0, 29.6, 50.3], ['liverpool', 'aston_villa', 42.5, 25.2, 32.3], ['man_united', 'sunderland', 58.8, 20.1, 21.1], ['southampton', 'swansea', 36.7, 19.8, 43.5], ['newcastle', 'chelsea', 22.0, 27.4, 50.6], ['west_brom', 'everton', 33.1, 25.6, 41.3], ['arsenal', 'man_united', 42.2, 20.7, 37.1], ['aston_villa', 'stoke', 29.0, 22.4, 48.7], ['chelsea', 'southampton', 62.0, 19.3, 18.7], ['crystal_palace', 'west_brom', 41.9, 21.5, 36.6], ['everton', 'liverpool', 24.0, 25.9, 50.1], ['man_city', 'newcastle', 64.4, 14.8, 20.8], ['sunderland', 'west_ham', 28.8, 32.7, 38.5], ['swansea', 'tottenham', 31.4, 16.8, 51.8], ['chelsea', 'aston_villa', 54.7, 32.0, 13.3], ['crystal_palace', 'west_ham', 31.9, 24.9, 43.2], ['everton', 'man_united', 24.3, 30.8, 44.8], ['southampton', 'leicester', 45.2, 21.1, 33.6], ['swansea', 'stoke', 29.8, 19.9, 50.2], ['tottenham', 'liverpool', 34.3, 21.3, 44.4], ['west_brom', 'sunderland', 50.6, 23.3, 26.1], ['arsenal', 'everton', 47.3, 31.2, 21.5], ['aston_villa', 'swansea', 27.8, 25.9, 46.3], ['leicester', 'crystal_palace', 31.9, 26.4, 41.7], ['liverpool', 'southampton', 45.4, 25.7, 29.0], ['man_united', 'man_city', 38.6, 19.5, 41.9], ['sunderland', 'newcastle', 23.8, 32.0, 44.2], ['west_ham', 'chelsea', 21.7, 33.3, 45.1], ['chelsea', 'liverpool', 47.2, 26.6, 26.2], ['crystal_palace', 'man_united', 28.7, 22.4, 48.9], ['everton', 'sunderland', 33.1, 38.6, 28.4], ['newcastle', 'stoke', 29.2, 27.2, 43.5], ['swansea', 'arsenal', 36.0, 17.3, 46.7], ['tottenham', 'aston_villa', 44.0, 22.7, 33.3], ['west_brom', 'leicester', 32.1, 28.9, 39.0], ['arsenal', 'tottenham', 42.5, 20.8, 36.7], ['aston_villa', 'man_city', 25.1, 22.3, 52.6], ['liverpool', 'crystal_palace', 49.5, 26.9, 23.6], ['man_united', 'west_brom', 55.1, 28.2, 16.7], ['stoke', 'chelsea', 30.0, 24.1, 45.9], ['sunderland', 'southampton', 23.2, 27.6, 49.2], ['west_ham', 'everton', 30.2, 32.3, 37.5], ['crystal_palace', 'sunderland', 34.6, 40.3, 25.1], ['everton', 'aston_villa', 31.6, 24.4, 43.9], ['man_city', 'liverpool', 39.4, 22.5, 38.1], ['newcastle', 'leicester', 30.2, 26.1, 43.7], ['southampton', 'stoke', 43.5, 28.7, 27.8], ['tottenham', 'west_ham', 37.7, 36.4, 25.9], ['west_brom', 'arsenal', 31.0, 22.4, 46.5]]


class Average(object):
	"""Average between percentage of Tweets and Stat"""
	def __init__(self, statPercentage,tweetPercentage,db):
		super(Average, self).__init__()
		self.statPercentage = statPercentage
		self.tweetPercentage=tweetPercentage
		self.cursor=db.cursor()
		self.cleanStat=[]
		self.cleanTweet=[]
		self.averageList=[]
		self.outcome=[]
		self.realOutcome=[]

	def clean(self):
		for week in self.statPercentage:
			for game in week:
				tmp=[]
				tmp.append(game[2])
				tmp.append(game[3])
				tmp.append(game[4])
				tmp.append(game[0])
				tmp.append(game[1])
				self.cleanStat.append(tmp)

		for game in self.tweetPercentage:
			tmp=[]
			tmp.append(game[2])
			tmp.append(game[3])
			tmp.append(game[4])
			tmp.append(game[0])
			tmp.append(game[1])
			self.cleanTweet.append(tmp)

	def makeAverage(self):
		i=0
		while i < len(self.cleanStat):
			tmp=[]
			tmp.append((self.cleanStat[i][0]+self.cleanTweet[i][0])/2) # Home_Win Prob
			tmp.append((self.cleanStat[i][1]+self.cleanTweet[i][1])/2) # Draw Prob
			tmp.append((self.cleanStat[i][2]+self.cleanTweet[i][2])/2) # Away_Win Prob
			self.averageList.append(tmp)
			i+=1
		for outcome in self.averageList:
			if outcome[0]>outcome[1] and outcome[0]>outcome[2]: #home win
				self.outcome.append(1)
			elif outcome[1]>outcome[0] and outcome[1]>outcome[2]: #draw
				self.outcome.append(0)
			else:
				self.outcome.append(-1)
		#print(self.outcome)

	def makeComparaison(self):
		for game in self.cleanStat:
			self.getGame(game[3],game[4])
		success=0
		for i in range(len(self.realOutcome)):
			if (self.realOutcome[i]==self.outcome[i]):
				success+=1
		return((success/(len(self.realOutcome)*1.0))*100)

	
	def getGame(self,home,away):
		notToTake=["Bournemouth","Norwich","Watford"]
		if home not in notToTake or away not in notToTake:
			self.cursor.execute ("""
					   SELECT HomeTeam, AwayTeam, FTHG , FTAG
					   FROM championship1516
					   WHERE HomeTeam=%s and AwayTeam=%s
					""", (home,away))
			game=self.cursor.fetchall()
			count=0
			for attrib in game:
				outcome=0
				if (not (attrib[0] in notToTake or attrib[1] in notToTake)):
					if attrib[2]>attrib[3]:
						outcome=1
					elif attrib[2]==attrib[3]:
						outcome=0
					else:
						outcome=-1
					self.realOutcome.append(outcome)
				count+=1
	

try:
	database = MySQLdb.connect('localhost', 'root', 'root', 'EPL2'); #login, password, database
	myAverage=Average(statPercentage,tweetPercentage,database)
	myAverage.clean()
	myAverage.makeAverage()
	result=myAverage.makeComparaison()
	print("For 50 games from the 2015-2016 season, the final correctness is : "+str(result))
	database.close();
			
except (_mysql.Error):
	print ("Mysql error ")
	sys.exit(1)
