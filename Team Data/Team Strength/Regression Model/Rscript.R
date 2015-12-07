#!/usr/bin/env Rscript
# Reference : http://www1.maths.leeds.ac.uk/~voss/projects/2010-sports/JamesGardner.pdf
arg <- commandArgs(TRUE)
games<-read.table(arg[1],sep=",",stringsAsFactors=F)

gamesToPredict<-as.numeric(arg[3])*10
homeGoals<-sum(games[3][1:gamesToPredict,]) 
awayGoals<-sum(games[4][1:gamesToPredict,]) 

# Create the Y Matrix
gamesNumber<-gamesToPredict
Y<- matrix(0,2*gamesNumber,1) # Form the Y Matrix containing all the game result
for (i in 1:gamesNumber){
	Y[((2*i)-1)] <- games[i,3]  # Every odd elements (we start at 1) ill be the home score
	Y[(2*i)]     <- games[i,4]  # Every even elements (start at 2) will be the away score
}

betavalue<- ((homeGoals+awayGoals)/(2*(gamesNumber)))

#  Create the R Matrix
teams<- sort(unique(c(games[,1],games[,2])),decreasing=FALSE) # Give all the teams name
teamsLength <-length(teams)
X<- matrix(0,2*gamesNumber,((2*teamsLength)+1)) # rows = 380*2 : columns=40(teams)+1(home advantage)
for (i in 1:gamesNumber){
	M <- which(teams == games[i,1]) # Index for Home Team in the sorted teams vector
	N <- which(teams == games[i,2]) # Index for Away Team

	# To get Attack and Defence strength 
	X[((2*i)-1),M] <- 1 # Home Team playing against Away Team on row
	X[((2*i)-1),N+teamsLength] <- -1 # Away VS Home on row
	X[(2*i),N] <- 1 # Home vs Away on column
	X[(2*i),M+teamsLength] <- -1 # Home vs Away on column
	X[((2*i)-1),((2*teamsLength)+1)] <- 1 # For the Home advantage

}

XX <- X[,-1] # Tountenberg , first column put away (here Arsenal) and replaced by 0 to be the benchmark

# Estimating Beta + Print in a good format
parameters <- glm(formula = Y ~ 0 + XX, family = poisson)
Z <- c(0, coefficients(parameters))
P <- data.frame(row.names=teams, Attack=Z[1:teamsLength], Defence=Z[(teamsLength+1):(2*teamsLength)],beta=betavalue)
write.table(list(teams=P,home=as.numeric(Z[2*teamsLength+1])),arg[2], sep=",")




