from parser import *
from kappa import *


if __name__ == '__main__':	
	myParser=Parser("joint_probabilities_0.6_100.csv")
	myParser.parse()
	confusionMatrix=myParser.confusionMatrix()
	myParser.printMatrix()
	#myParser.givePercentage()
	cohenKappa=Kappa(confusionMatrix)
	kappaScore=cohenKappa.giveKappa()
	print("Cohen's Kappa score : " +str(kappaScore))


