# Reference : http://psych.unl.edu/psycrs/handcomp/hckappa.PDF

class Kappa(object):
	"""Create the kappa score given a confusion matrix"""
	def __init__(self, matrix):
		super(Kappa, self).__init__()
		self.kappaMatrix = matrix
		self.overalTotal= 0
		self.totalAgreement=0
		self.diagEF=[0 for x in range(3)]
		self.EFChanceSum=0
		self.kappaScore=0

	def giveKappa(self):
		self.overalSum()
		self.overalAgreement()
		self.expectedFrequency()
		self.EFSum()
		self.computeKappa()
		return self.kappaScore

	def overalSum(self): # Step 3 - Compute the overall total
		res=0
		for i in range(3):
			for j in range(3):
				res+=self.kappaMatrix[i][j]
		self.overalTotal=res

	def overalAgreement(self): # Step 4 - Compute the total number of agreements
		res=0
		for i in range(3):
			for j in range(3):
				if (i==j):
					res+=self.kappaMatrix[i][j]
		self.totalAgreement=res

	def expectedFrequency(self): # Step 5 -  Compute the expected frequency for the number of agreements that would have been expected by chance for each coding category.
		for diag in range(3):
			columnSum=0
			rowSum=0
			for i in range(3):
				columnSum+=self.kappaMatrix[diag][i]
				rowSum+=self.kappaMatrix[i][diag]
			self.diagEF[diag]=(columnSum*rowSum)/(self.overalTotal*1.0)

	def EFSum(self): # Step 6 - Compute the sum of the expected frequencies of agreement by chance.
		for elem in self.diagEF:
			self.EFChanceSum+=elem


	def computeKappa(self) :
		self.kappaScore=(self.totalAgreement - self.EFChanceSum)/(self.overalTotal - self.EFChanceSum)








		