from sklearn.ensemble import RandomForestClassifier

from numpy import genfromtxt, savetxt
from joblib import Parallel, delayed
import multiprocessing
import csv
import pandas as pd
import numpy as np

num_cores = multiprocessing.cpu_count()

iterations = 100

team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names = [team_name.lower().replace(" ", "_") for team_name in team_names]

max_elems = [50, 100, 250]

def get_probabilities_bigram(team_name, n):
    try:
        training_set = genfromtxt('trainsets_last/'+team_name+'_train_bigram_last_'+ str(n)+'.csv', dtype='float', delimiter=',', skip_header=1)[1:]    
        class_labels = [x[-1] for x in training_set]
        features = [x[0:-1] for x in training_set]
        test_set = genfromtxt('testsets_last/'+team_name+'_test_bigram_last_'+ str(n)+'.csv', dtype='float', delimiter=',', skip_header=1)[1:]

        rf_result = np.zeros((test.shape[0], 3))
        for i in range(iterations):            
            rfc = RandomForestClassifier(n_estimators=100, n_jobs=4)
            rfc.fit(features, class_labels)
            rf_result = rf_result + rfc.predict_proba(test_set)

        rf_result = rf_result/iterations
        savetxt('results/'+team_name+'_rf_proba_bigram_last_'+ str(n)+'.csv', rf_result, delimiter=',', fmt='%f')
    except:
        print("error: {}, {}".format(team_name, n))



def joint_probabilities(home_team, away_team, matchday, alpha, n):
    home_lose = -1
    draw = -1
    home_win = -1
    try:
        try:
            with open('results/'+home_team+'_rf_proba_bigram_last_'+ str(n)+'.csv') as f:
                home_probs = [[float(elem.strip()) for elem in line.split(",")] for line in f.readlines()]
        except FileNotFoundError:
            print('file does not exist home: {}'.format(home_team))
        try:
            with open('results/'+away_team+'_rf_proba_bigram_last_'+ str(n)+'.csv') as f:
                away_probs = [[float(elem.strip()) for elem in line.split(",")] for line in f.readlines()]
        except FileNotFoundError:
            print('file does not exist away: {}'.format(away_team))
        
        try:
            home_prob = home_probs[matchday-1]
        except IndexError:
            print("IndexError: {}, {}, {}".format(home_team, n, matchday))

        try:
            away_prob = away_probs[matchday-1]
        except IndexError:
            print("IndexError away: {}, {}, {}".format(away_team, n, matchday))
        
        home_win = (alpha * home_prob[2]) + ((1 - alpha) * away_prob[0])
        home_lose = (alpha * home_prob[0]) + ((1 - alpha) * away_prob[2])
        draw = (alpha * home_prob[1]) + ((1 - alpha) * away_prob[1])
    except:
        print("other error")




    return [home_lose, draw, home_win] 

def get_joint_probabilities(filename, n):
    headings = ["date", "home", "away", "homescore", "awayscore", "matchday"]
    matches = pd.read_csv(filename, header=None, names=headings)
    
    alphas = [0.4, 0.5, 0.6, 0.7]
    for alpha in alphas:
        joint_df = pd.DataFrame(columns=["home", "away", "homescore", "awayscore", "matchday", "home_lose", "draw", "home_win"])
        for index, row in matches.iterrows():

            home_team =row['home'].lower().replace(' ', '_')
            away_team = row['away'].lower().replace(' ', '_')
            matchday = row['matchday']-25
            if matchday ==14:
                break
            probs = joint_probabilities(home_team, away_team, matchday, alpha, n)

            joint_df = joint_df.append({"home": home_team, "away": away_team,"homescore": row["homescore"], "awayscore": row["awayscore"], "matchday": matchday+25, "home_lose": probs[0], "draw": probs[1], "home_win":probs[2]}, ignore_index=True)
            #=IF(C2-D2>0;1;IF(C2-D2<0;-1;1))
            #=IF(F2>G2;IF(F2>H2;-1;1);IF(G2>H2;0;1))
        try:
            joint_df.to_csv("joint/joint_probabilities_{}_{}_last.csv".format(alpha, n), index=False)
        except UnicodeEncodeError:
            print("couldn't write word, ecoding error")
    


if __name__=="__main__":
    for n in max_elems:
        Parallel(n_jobs=num_cores)(delayed(get_probabilities_bigram)(team_name, n) for team_name in team_names)
        #Parallel(n_jobs=num_cores)(delayed(get_probabilities_unigram)(team_name, n) for team_name in team_names)
        #get_probabilities('west_brom')
        get_joint_probabilities('championship1415_2.csv', n)

    