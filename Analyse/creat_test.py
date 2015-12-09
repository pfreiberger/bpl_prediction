#creating training sets
from collections import OrderedDict
import pandas as pd
import pymongo

from joblib import Parallel, delayed
import multiprocessing

client = pymongo.MongoClient()
db = client['cleansed']

num_cores = multiprocessing.cpu_count()

path = "./testsets/"

team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names = [team_name.lower().replace(" ", "_") for team_name in team_names]
#words = ["arsen", "win", "lose", "draw","jack", "ramesy", "word", "watch", "big", "good", "legend", "love"]

def inc(word_dict, words):
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
    
    return word_dict


def get_df(collection, team_name, words): 
    df = pd.DataFrame(columns=words)
    
    
    i=1
    while(i<=14):
        word_dict = OrderedDict((word, 0) for word in words)
        if collection.find_one({"team": team_name.replace("_", " "), "matchday": i}):
            for tweet in collection.find({"team": team_name.replace("_", " "), "matchday": i}):
                word_dict = inc(word_dict, tweet['words'])           
            df = df.append(word_dict, ignore_index=True)
            
        i+=1
    return df
  
        
def get_test_set(team_name):
    words = get_words(team_name)
    col = db['season15_16']
    df_main = get_df(col, team_name, words)
    df_main.to_csv(path + team_name + "_test.csv", index=False)
    

def get_words(team_name):
    with open("./popular/"+team_name+'_popular.txt', 'r') as f:
        words = f.readlines() 
    words = [word.strip() for word in words]    
    return words 


def create_match_line(collection, home_team, away_team, matchday):
    word_dict = OrderedDict((word, 0) for word in words)
    for tweet in collection.find({"team": home_team.replace("_", " "), "matchday": i}):
        word_dict = inc(word_dict, tweet['words'])
    for tweet in collection.find({"team": away_team.replace("_", " "), "matchday": i}):
        word_dict = inc(word_dict, tweet['words'])

    return word_dict


def create_match_matrix(filename, collection, words):
    headings = ["date", "home", "away", "homescore", "awayscore", "matchday"]

    matches = pd.read_csv(filename, header=None, names=headings)
    
    championship_df = pd.DataFrame() 

    for index, row in matches.iterrows():
        matchdate = datetime.strptime(row['date'], "%Y-%m-%d %H:%M:%S")
        home_team =row['home']
        away_team = row['away']
        matchday = row['matchday']

        row = create_match_line(collection, home_team, away_team, matchday)

        championship_df = championship_df.append(row, ignore_index=True)
        index +=1
        if index%100 ==0:
            print(index)


def bigram_to_key(bigram):
    return "".join(bigram).replace(" ", "").strip()

def get_df_bigram(collection, team_name, words): 
    df = pd.DataFrame(columns=words)   
    
    i=1
    while(i<=14):
        word_dict = OrderedDict((word, 0) for word in words)
        if collection.find_one({"team": team_name.replace("_", " "), "matchday": i}):
            for tweet in collection.find({"team": team_name.replace("_", " "), "matchday": i}):
                bigram_keys =[bigram_to_key(word) for word in get_bigrams(tweet['words'], 2)]
                word_dict = inc(word_dict, bigram_keys)          
            df = df.append(word_dict, ignore_index=True)
            
        i+=1
    return df
  
        
def get_test_set_bigram(team_name):
    words = [bigram_to_key(word) for word in read_popular_bigrams(team_name)]
    col = db['season15_16']
    df_main = get_df(col, team_name, words)
    df_main.to_csv(path + team_name + "_test_bigram.csv", index=False)
    

#returns list of list of bigrams
def read_popular_bigrams(team_name):
    with open("./popular/" +team_name+"_bigrams.txt", 'r') as f:
        words = f.readlines() 
    words = [word.replace("'","").split(",") for word in words]
    return words 
      

if __name__ == "__main__":
    #Parallel(n_jobs=num_cores)(delayed(get_test_set)(team_name) for team_name in team_names) 
    #create_match_matrix("./championship1516.csv")
    #Parallel(n_jobs=num_cores)(delayed(get_test_set_bigram)(team_name) for team_name in team_names)
       

    get_train_set_bigram("arsenal")
    