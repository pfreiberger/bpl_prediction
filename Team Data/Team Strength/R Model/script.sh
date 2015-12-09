#!/bin/bash
#file1="EPLData/Processedpremierleague0910.csv"
file1="EPLData/Processedpremierleague1011.csv"
file2="EPLData/Processedpremierleague1112.csv"
file3="EPLData/Processedpremierleague1213.csv"
file4="EPLData/Processedpremierleague1314.csv"
file5="EPLData/Processedpremierleague1415.csv"
file6="EPLData/Processedpremierleague1516.csv"

#output1="TeamStrength/lambda0910.txt"
output1="TeamStrength/lambda1011.txt"
output2="TeamStrength/lambda1112.txt"
output3="TeamStrength/lambda1213.txt"
output4="TeamStrength/lambda1314.txt"
output5="TeamStrength/lambda1415.txt"
output6="TeamStrength/lambda1516.txt"

pathToScript="Rscript.R"

#Rscript Rscript.R $file1 $output1 38
#Rscript Rscript.R $file2 $output2 6

#Rscript Rscript.R $file2 $output2 38
#Rscript Rscript.R $file3 $output3 6

#Rscript Rscript.R $file3 $output3 38
#Rscript Rscript.R $file4 $output4 6

#Rscript Rscript.R $file4 $output4 38
#Rscript Rscript.R $file5 $output5 6

Rscript Rscript.R $file5 $output5 38
Rscript Rscript.R $file6 $output6 6
