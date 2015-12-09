import urllib2

matchResults=urllib2.urlopen("https://raw.githubusercontent.com/openfootball/eng-england/master/2015-16/1-premierleague-i.txt").read()# Fetch the results for the new week 
newFile=open("Season1516.txt","w")
newFile.write(matchResults)